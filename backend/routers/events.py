"""
events.py - Router para gerenciar eventos
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Event, EventoOrganizador
from models.usuario import Usuario, TipoUsuario
from models.player import Player
from utils.permissions import require_permission, require_tipo, Permissao
from logger_production import get_logger

log = get_logger("events_router")

router = APIRouter()

@router.post("", response_model=dict, status_code=201)
async def create_event(
    event_data: dict,
    usuario: Usuario = Depends(require_tipo(TipoUsuario.ORGANIZADOR))
):
    """Criar novo evento (requer tipo ORGANIZADOR ou ADMIN)"""
    session = SessionLocal()
    try:
        log.info(f"Criando novo evento: {event_data.get('name')} por usuário {usuario.id}")
        
        event = Event(
            name=event_data["name"],
            date=event_data["date"],
            time=event_data.get("time", "19:00"),
            usuario_id=usuario.id,  # Vincular evento ao organizador que criou
            active=event_data.get("active", True)
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        
        log.info(f"Evento criado com sucesso: ID {event.id} ({event.name})")
        
        # Registrar criador na tabela evento_organizador
        evento_org = EventoOrganizador(
            event_id=event.id,
            usuario_id=usuario.id,
            é_criador=1  # Marcar como criador original
        )
        session.add(evento_org)
        session.commit()
        
        log.info(f"[{usuario.email}] Evento criado: {event.name} (ID: {event.id})")
        
        return {
            "id": event.id,
            "name": event.name,
            "date": event.date,
            "time": event.time,
            "active": event.active
        }
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao criar evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("", response_model=List[dict])
async def list_events(usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))):
    """Listar todos os eventos (requer permissão VER_EVENTOS)"""
    session = SessionLocal()
    try:
        events = session.query(Event).filter(Event.active == True).all()
        
        log.info(f"[{usuario.email}] Listando {len(events)} eventos")
        
        return [
            {
                "id": e.id,
                "name": e.name,
                "date": e.date,
                "time": e.time,
                "active": e.active
            }
            for e in events
        ]
    except Exception as e:
        log.error(f"Erro ao listar eventos: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/meus-eventos", response_model=List[dict])
async def list_my_events(usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))):
    """
    Listar apenas os eventos que pertencem ao usuário.
    
    - Jogadores: Veem apenas eventos onde estão registrados como Player
    - Organizadores: Veem apenas eventos que criaram (usuario_id)
    - Admins: Veem todos os eventos
    
    NOTA: Esta rota DEVE estar antes de /{event_id} para evitar conflito
    """
    session = SessionLocal()
    try:
        # Se é admin, retorna todos os eventos
        if usuario.tipo in ['admin', TipoUsuario.ADMIN]:
            events = session.query(Event).filter(Event.active == True).all()
            log.info(f"[{usuario.email}] Listando todos os {len(events)} eventos (admin)")
        
        # Se é organizador, retorna apenas eventos que criou
        elif usuario.tipo in ['organizador', TipoUsuario.ORGANIZADOR]:
            events = session.query(Event).filter(
                Event.active == True,
                Event.usuario_id == usuario.id
            ).all()
            log.info(f"[{usuario.email}] Listando {len(events)} eventos (organizador)")
        
        # Se é jogador, retorna apenas eventos onde está registrado
        else:
            events = session.query(Event).join(
                Player, Event.id == Player.event_id
            ).filter(
                Event.active == True,
                Player.usuario_id == usuario.id
            ).all()
            log.info(f"[{usuario.email}] Listando {len(events)} eventos (jogador)")
        
        return [
            {
                "id": e.id,
                "name": e.name,
                "date": e.date,
                "time": e.time,
                "active": e.active
            }
            for e in events
        ]
    except Exception as e:
        log.error(f"Erro ao listar eventos: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/{event_id}", response_model=dict)
async def get_event(event_id: int):
    """Obter evento por ID"""
    session = SessionLocal()
    try:
        event = session.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        return {
            "id": event.id,
            "name": event.name,
            "date": event.date,
            "time": event.time,
            "active": event.active
        }
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Erro ao obter evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.put("/{event_id}", response_model=dict)
async def update_event(
    event_id: int,
    event_data: dict,
    usuario: Usuario = Depends(require_tipo(TipoUsuario.ORGANIZADOR))
):
    """Atualizar evento (requer tipo ORGANIZADOR ou ADMIN)"""
    session = SessionLocal()
    try:
        event = session.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Atualizar apenas os campos fornecidos
        if "name" in event_data:
            event.name = event_data["name"]
        if "date" in event_data:
            event.date = event_data["date"]
        if "time" in event_data:
            event.time = event_data["time"]
        if "active" in event_data:
            event.active = event_data["active"]
        
        session.commit()
        session.refresh(event)
        
        log.info(f"[{usuario.email}] Evento atualizado: {event.name} (ID: {event.id})")
        
        return {
            "id": event.id,
            "name": event.name,
            "date": event.date,
            "time": event.time,
            "active": event.active
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao atualizar evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.delete("/{event_id}", response_model=dict)
async def delete_event(
    event_id: int,
    usuario: Usuario = Depends(require_tipo(TipoUsuario.ADMIN))
):
    """Deletar evento (requer tipo ADMIN)"""
    session = SessionLocal()
    try:
        event = session.query(Event).filter(Event.id == event_id).first()
        
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Soft delete: apenas marcar como inativo
        event.active = False
        session.commit()
        
        log.info(f"[{usuario.email}] Evento deletado (soft delete): {event.name} (ID: {event.id})")
        
        return {
            "id": event.id,
            "name": event.name,
            "date": event.date,
            "time": event.time,
            "active": event.active
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao deletar evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

