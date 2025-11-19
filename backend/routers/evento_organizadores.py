"""
evento_organizadores.py - Router para gerenciar organizadores de eventos
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Event, EventoOrganizador
from models.usuario import Usuario, TipoUsuario
from utils.permissions import require_permission, require_tipo, Permissao
from logger import get_logger

log = get_logger("evento_organizadores")

router = APIRouter(prefix="/events", tags=["evento_organizadores"])


@router.post("/{event_id}/organizadores", response_model=dict)
async def add_organizador(
    event_id: int,
    organizador_data: dict,  # {"usuario_id": int}
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Adicionar um novo organizador a um evento.
    Apenas organizadores do evento podem adicionar outros organizadores.
    
    Args:
        event_id: ID do evento
        organizador_data: {"usuario_id": int} - ID do usuário a adicionar como organizador
    """
    session = SessionLocal()
    try:
        # Verificar se evento existe
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Verificar se usuário atual é organizador do evento
        current_org = session.query(EventoOrganizador).filter(
            EventoOrganizador.event_id == event_id,
            EventoOrganizador.usuario_id == usuario.id
        ).first()
        
        if not current_org and usuario.tipo not in ['admin', TipoUsuario.ADMIN]:
            raise HTTPException(
                status_code=403,
                detail="Você não é organizador deste evento"
            )
        
        # Verificar se novo organizador existe
        novo_org_id = organizador_data.get("usuario_id")
        novo_org = session.query(Usuario).filter(Usuario.id == novo_org_id).first()
        if not novo_org:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        # Verificar se já é organizador
        já_é_org = session.query(EventoOrganizador).filter(
            EventoOrganizador.event_id == event_id,
            EventoOrganizador.usuario_id == novo_org_id
        ).first()
        
        if já_é_org:
            raise HTTPException(
                status_code=400,
                detail=f"'{novo_org.email}' já é organizador deste evento"
            )
        
        # Adicionar novo organizador
        evento_org = EventoOrganizador(
            event_id=event_id,
            usuario_id=novo_org_id,
            é_criador=0
        )
        session.add(evento_org)
        session.commit()
        
        log.info(f"[{usuario.email}] Organizador '{novo_org.email}' adicionado ao evento '{event.name}'")
        
        return {
            "success": True,
            "message": f"'{novo_org.email}' foi adicionado como organizador",
            "evento_id": event_id,
            "novo_organizador": {
                "id": novo_org.id,
                "email": novo_org.email,
                "nome": novo_org.email.split('@')[0]
            }
        }
    except HTTPException:
        session.close()
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao adicionar organizador: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.get("/{event_id}/organizadores", response_model=List[dict])
async def list_organizadores(
    event_id: int,
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Listar todos os organizadores de um evento.
    """
    session = SessionLocal()
    try:
        # Verificar se evento existe
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Buscar organizadores com join
        organizadores = session.query(EventoOrganizador, Usuario).join(
            Usuario, EventoOrganizador.usuario_id == Usuario.id
        ).filter(
            EventoOrganizador.event_id == event_id
        ).all()
        
        log.info(f"[{usuario.email}] Listando {len(organizadores)} organizadores do evento {event_id}")
        
        result = []
        for evento_org, usr in organizadores:
            result.append({
                "id": usr.id,
                "email": usr.email,
                "é_criador": evento_org.é_criador,
                "adicionado_em": evento_org.criado_em.isoformat() if evento_org.criado_em else None
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Erro ao listar organizadores: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()


@router.delete("/{event_id}/organizadores/{organizador_id}", response_model=dict)
async def remove_organizador(
    event_id: int,
    organizador_id: int,
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Remover um organizador de um evento.
    Apenas organizadores do evento ou admin podem remover.
    Não permite remover o criador original do evento.
    """
    session = SessionLocal()
    try:
        # Verificar se evento existe
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Verificar se usuário atual é organizador do evento
        current_org = session.query(EventoOrganizador).filter(
            EventoOrganizador.event_id == event_id,
            EventoOrganizador.usuario_id == usuario.id
        ).first()
        
        if not current_org and usuario.tipo not in ['admin', TipoUsuario.ADMIN]:
            raise HTTPException(
                status_code=403,
                detail="Você não é organizador deste evento"
            )
        
        # Buscar organizador a ser removido
        org_to_remove = session.query(EventoOrganizador).filter(
            EventoOrganizador.event_id == event_id,
            EventoOrganizador.usuario_id == organizador_id
        ).first()
        
        if not org_to_remove:
            raise HTTPException(status_code=404, detail="Organizador não encontrado neste evento")
        
        # Não permitir remover criador original (é_criador = 1)
        if org_to_remove.é_criador == 1:
            raise HTTPException(
                status_code=400,
                detail="Não é possível remover o criador original do evento"
            )
        
        # Buscar dados do organizador para log
        org_user = session.query(Usuario).filter(Usuario.id == organizador_id).first()
        
        # Remover organizador
        session.delete(org_to_remove)
        session.commit()
        
        log.info(f"[{usuario.email}] Organizador '{org_user.email}' removido do evento '{event.name}'")
        
        return {
            "success": True,
            "message": f"'{org_user.email}' foi removido como organizador",
            "evento_id": event_id,
            "removido": {
                "id": org_user.id,
                "email": org_user.email
            }
        }
    except HTTPException:
        session.close()
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao remover organizador: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
