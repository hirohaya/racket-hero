# routers/seed.py - Seed data endpoint for development/testing

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.usuario import Usuario
from models.event import Event
from models.player import Player
from utils.security import hash_password
from datetime import datetime
from logger_production import get_logger

router = APIRouter()
logger = get_logger("seed")

SEED_EXECUTED_FILE = "/tmp/racket_hero_seed_executed"

@router.post("/seed", tags=["Development"], include_in_schema=False)
async def seed_data(db: Session = Depends(get_db)):
    """
    Seed database with test data (DEVELOPMENT ONLY)
    
    This endpoint should only work in development/staging environments.
    It creates test usuarios, eventos, and player associations.
    
    Can only be executed once per deployment.
    """
    import os
    
    # Check if seed was already executed
    if os.path.exists(SEED_EXECUTED_FILE):
        logger.warning("Seed data already executed in this deployment")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seed data has already been executed in this deployment"
        )
    
    try:
        logger.info("Starting seed data initialization...")
        
        # Check if data already exists
        existing_organizador = db.query(Usuario).filter(
            Usuario.email == "organizador@test.com"
        ).first()
        
        if existing_organizador:
            logger.info("Test data already exists in database")
            # Create marker file to prevent re-execution
            os.makedirs(os.path.dirname(SEED_EXECUTED_FILE), exist_ok=True)
            open(SEED_EXECUTED_FILE, 'a').close()
            
            return {
                "message": "Test data already exists",
                "status": "skipped",
                "data": {
                    "organizador": {
                        "email": existing_organizador.email,
                        "nome": existing_organizador.nome
                    }
                }
            }
        
        # Create Organizador usuario
        organizador = Usuario(
            email="organizador@test.com",
            nome="Organizador Teste",
            senha_hash=hash_password("Senha123!"),
            tipo="organizador",
            ativo=True
        )
        db.add(organizador)
        db.flush()  # Get ID without commit
        
        logger.info(f"[OK] Organizador criado: {organizador.email}")
        
        # Create Jogador usuario
        jogador = Usuario(
            email="jogador@test.com",
            nome="Jogador Teste",
            senha_hash=hash_password("Senha123!"),
            tipo="usuario",
            ativo=True
        )
        db.add(jogador)
        db.flush()
        
        logger.info(f"[OK] Jogador criado: {jogador.email}")
        
        # Create test evento
        evento = Event(
            name="Torneio Teste",
            date="2025-12-01",
            time="14:00",
            active=True,
            usuario_id=organizador.id
        )
        db.add(evento)
        db.flush()
        
        logger.info(f"[OK] Evento criado: {evento.nome}")
        
        # Add jogador to evento
        player = Player(
            usuario_id=jogador.id,
            event_id=evento.id,
            name="Jogador Teste",
            initial_elo=1600
        )
        db.add(player)
        
        logger.info(f"[OK] Jogador adicionado ao evento")
        
        # Commit all changes
        db.commit()
        
        logger.info("[OK] Database seeding completo!")
        
        # Create marker file to prevent re-execution
        os.makedirs(os.path.dirname(SEED_EXECUTED_FILE), exist_ok=True)
        open(SEED_EXECUTED_FILE, 'a').close()
        
        return {
            "message": "Seed data created successfully",
            "status": "success",
            "data": {
                "organizador": {
                    "email": organizador.email,
                    "nome": organizador.nome,
                    "id": organizador.id
                },
                "jogador": {
                    "email": jogador.email,
                    "nome": jogador.nome,
                    "id": jogador.id
                },
                "evento": {
                    "nome": evento.nome,
                    "data": evento.data,
                    "hora": evento.hora,
                    "id": evento.id
                }
            }
        }
    
    except Exception as e:
        logger.error(f"Error during seed: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Seed data creation failed: {str(e)}"
        )
