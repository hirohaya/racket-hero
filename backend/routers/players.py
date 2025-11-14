"""
players.py - Router para gerenciar jogadores
"""

from fastapi import APIRouter, HTTPException
from typing import List
from database import SessionLocal
from models import Player
from logger import get_logger

log = get_logger("players_router")

router = APIRouter()

@router.post("", response_model=dict)
async def create_player(player_data: dict):
    """Criar novo jogador"""
    session = SessionLocal()
    try:
        player = Player(
            event_id=player_data["event_id"],
            name=player_data["name"],
            initial_elo=player_data.get("initial_elo", 1600)
        )
        session.add(player)
        session.commit()
        session.refresh(player)
        
        log.info(f"Jogador criado: {player.name} (ID: {player.id}, Elo: {player.initial_elo})")
        
        return {
            "id": player.id,
            "event_id": player.event_id,
            "name": player.name,
            "initial_elo": player.initial_elo
        }
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao criar jogador: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/{event_id}", response_model=List[dict])
async def list_players(event_id: int):
    """Listar jogadores de um evento"""
    session = SessionLocal()
    try:
        players = session.query(Player).filter(Player.event_id == event_id).all()
        
        return [
            {
                "id": p.id,
                "event_id": p.event_id,
                "name": p.name,
                "initial_elo": p.initial_elo
            }
            for p in players
        ]
    except Exception as e:
        log.error(f"Erro ao listar jogadores: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/player/{player_id}", response_model=dict)
async def get_player(player_id: int):
    """Obter jogador por ID"""
    session = SessionLocal()
    try:
        player = session.query(Player).filter(Player.id == player_id).first()
        
        if not player:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        
        return {
            "id": player.id,
            "event_id": player.event_id,
            "name": player.name,
            "initial_elo": player.initial_elo
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Erro ao obter jogador: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
