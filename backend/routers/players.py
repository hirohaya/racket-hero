"""
players.py - Router para gerenciar jogadores
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from database import SessionLocal
from models import Player
from models.usuario import Usuario
from utils.permissions import require_permission, Permissao
from logger import get_logger

log = get_logger("players_router")

router = APIRouter()

@router.post("", response_model=dict, status_code=201)
async def create_player(player_data: dict):
    """Criar novo jogador"""
    session = SessionLocal()
    try:
        player = Player(
            event_id=player_data["event_id"],
            name=player_data["name"],
            club=player_data.get("club"),
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
            "club": player.club,
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
                "club": p.club,
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
            "club": player.club,
            "initial_elo": player.initial_elo
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Erro ao obter jogador: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.post("/eventos/{event_id}/inscricao", response_model=dict)
async def register_user_to_event(
    event_id: int,
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Registrar usuário autenticado como jogador em um evento.
    
    - Requer autenticação
    - Verifica se usuário já está registrado
    - Cria registro de Player com usuario_id
    """
    session = SessionLocal()
    try:
        from models import Event
        
        # Verificar se evento existe e está ativo
        event = session.query(Event).filter(Event.id == event_id, Event.active == True).first()
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Verificar se usuário já está registrado no evento
        existing = session.query(Player).filter(
            Player.event_id == event_id,
            Player.usuario_id == usuario.id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Você já está registrado neste evento")
        
        # Criar registro de Player
        player = Player(
            event_id=event_id,
            usuario_id=usuario.id,
            name=usuario.email.split("@")[0],  # Usar parte antes do @ do email como nome
            initial_elo=1600.0
        )
        session.add(player)
        session.commit()
        session.refresh(player)
        
        log.info(f"[{usuario.email}] Registrou-se no evento {event.name} (ID: {event_id})")
        
        return {
            "id": player.id,
            "event_id": player.event_id,
            "usuario_id": player.usuario_id,
            "name": player.name,
            "club": player.club,
            "initial_elo": player.initial_elo,
            "message": f"Registrado com sucesso no evento '{event.name}'"
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao registrar usuário no evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/eventos/{event_id}/inscritos", response_model=List[dict])
async def list_event_players(event_id: int):
    """
    Listar todos os jogadores (inscritos) de um evento.
    """
    session = SessionLocal()
    try:
        from models import Event
        
        # Verificar se evento existe
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        players = session.query(Player).filter(Player.event_id == event_id).all()
        
        return [
            {
                "id": p.id,
                "event_id": p.event_id,
                "usuario_id": p.usuario_id,
                "name": p.name,
                "club": p.club,
                "initial_elo": p.initial_elo
            }
            for p in players
        ]
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Erro ao listar jogadores do evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.delete("/eventos/{event_id}/inscricao", response_model=dict)
async def unregister_user_from_event(
    event_id: int,
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Remover usuário autenticado como jogador de um evento.
    (Apenas admins podem remover, ou o próprio usuário)
    """
    session = SessionLocal()
    try:
        # Encontrar registro de Player
        player = session.query(Player).filter(
            Player.event_id == event_id,
            Player.usuario_id == usuario.id
        ).first()
        
        if not player:
            raise HTTPException(status_code=404, detail="Você não está registrado neste evento")
        
        player_id = player.id
        session.delete(player)
        session.commit()
        
        log.info(f"[{usuario.email}] Removeu-se do evento {event_id}")
        
        return {
            "message": f"Desregistro realizado com sucesso",
            "player_id": player_id
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao remover usuário do evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()