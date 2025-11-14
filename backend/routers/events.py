"""
events.py - Router para gerenciar eventos
"""

from fastapi import APIRouter, HTTPException
from typing import List
from database import SessionLocal
from models import Event
from logger import get_logger

log = get_logger("events_router")

router = APIRouter()

@router.post("", response_model=dict)
async def create_event(event_data: dict):
    """Criar novo evento"""
    session = SessionLocal()
    try:
        event = Event(
            name=event_data["name"],
            date=event_data["date"],
            time=event_data.get("time", "19:00"),
            active=event_data.get("active", True)
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        
        log.info(f"Evento criado: {event.name} (ID: {event.id})")
        
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
async def list_events():
    """Listar todos os eventos"""
    session = SessionLocal()
    try:
        events = session.query(Event).filter(Event.active == True).all()
        
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
