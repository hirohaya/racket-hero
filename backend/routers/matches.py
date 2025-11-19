"""
matches.py - Router para gerenciar partidas
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Match, Player, Event
from models.usuario import Usuario
from utils.permissions import require_permission, Permissao
from schemas.matches import MatchCreate, MatchUpdate, MatchResponse
from logger_production import get_logger

log = get_logger("matches_router")

# Função de cálculo de Elo
def calculate_elo_change(winner_elo: float, loser_elo: float, k_factor: int = 32) -> float:
    """
    Calcula mudança de Elo após partida.
    K-factor padrão de 32 para jogadores normais.
    
    Fórmula: change = K * (1 - expected_score)
    expected_score = 1 / (1 + 10^((loser_elo - winner_elo)/400))
    """
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    elo_change = k_factor * (1 - expected_winner)
    return elo_change

router = APIRouter()

@router.post("", response_model=MatchResponse, status_code=status.HTTP_201_CREATED)
async def create_match(
    match_data: MatchCreate,
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Criar nova partida e atualizar Elo dos jogadores.
    
    Requer autenticação e acesso a eventos.
    Jogadores devem estar inscritos no mesmo evento.
    Vencedor deve ser um dos dois jogadores.
    """
    session = SessionLocal()
    try:
        log.info(f"Criando partida: P1={match_data.player_1_id}, P2={match_data.player_2_id}, Winner={match_data.winner_id}")
        
        # Validar evento existe
        event = session.query(Event).filter(Event.id == match_data.event_id).first()
        if not event:
            log.warning(f"Partida falhou: evento {match_data.event_id} não encontrado")
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        # Validar jogadores
        p1 = session.query(Player).filter(Player.id == match_data.player_1_id).first()
        p2 = session.query(Player).filter(Player.id == match_data.player_2_id).first()
        
        if not p1 or not p2:
            log.warning(f"Partida falhou: jogador P1={match_data.player_1_id} ou P2={match_data.player_2_id} não encontrado")
            raise HTTPException(status_code=404, detail="Um ou ambos jogadores não encontrados")
        
        # Validar que jogadores estão inscritos no mesmo evento
        if p1.event_id != p2.event_id or p1.event_id != match_data.event_id:
            log.warning(f"Partida falhou: jogadores em eventos diferentes")
            raise HTTPException(
                status_code=400, 
                detail="Jogadores devem estar inscritos no mesmo evento"
            )
        
        # Validar vencedor APENAS se foi informado
        if match_data.winner_id is not None:
            if match_data.winner_id not in [match_data.player_1_id, match_data.player_2_id]:
                log.warning(f"Partida falhou: vencedor {match_data.winner_id} não é um dos jogadores")
                raise HTTPException(
                    status_code=400,
                    detail="Vencedor deve ser um dos dois jogadores"
                )
        
        # Criar partida
        match = Match(
            event_id=match_data.event_id,
            player_1_id=match_data.player_1_id,
            player_2_id=match_data.player_2_id,
            winner_id=match_data.winner_id
        )
        
        log.info(f"Partida criada com ID={match.id}, winner_id={match.winner_id}")
        
        # Calcular mudanças de Elo APENAS se winner_id foi informado
        if match_data.winner_id is not None:
            if match_data.winner_id == match_data.player_1_id:
                # Player 1 venceu
                elo_change = calculate_elo_change(p1.initial_elo, p2.initial_elo)
                p1.initial_elo += elo_change
                p2.initial_elo -= elo_change
                winner_name = p1.name
            else:
                # Player 2 venceu
                elo_change = calculate_elo_change(p2.initial_elo, p1.initial_elo)
                p2.initial_elo += elo_change
                p1.initial_elo -= elo_change
                winner_name = p2.name
        else:
            # Sem vencedor definido
            winner_name = None
        
        # Salvar alterações
        session.add(match)
        session.commit()
        session.refresh(match)
        
        log.info(f"DEBUG: Após commit/refresh, winner_id={match.winner_id}")
        
        session.refresh(p1)
        session.refresh(p2)
        
        log.info(f"[{usuario.email}] Partida criada: {p1.name} vs {p2.name}, Vencedor: {winner_name}")
        log.info(f"Novo Elo - {p1.name}: {p1.initial_elo:.1f}, {p2.name}: {p2.initial_elo:.1f}")
        
        return MatchResponse(
            id=match.id,
            event_id=match.event_id,
            player_1_id=match.player_1_id,
            player_2_id=match.player_2_id,
            winner_id=match.winner_id,
            player_1_name=p1.name,
            player_2_name=p2.name,
            winner_name=winner_name,
            player_1_elo=p1.initial_elo,
            player_2_elo=p2.initial_elo,
            created_at=match.created_at,
            updated_at=match.updated_at
        )
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao criar partida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/{event_id}", response_model=List[MatchResponse])
async def list_matches(event_id: int):
    """
    Listar partidas de um evento (público).
    
    Retorna lista de partidas com IDs e nomes dos jogadores.
    """
    session = SessionLocal()
    try:
        # Validar evento existe
        event = session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Evento não encontrado")
        
        matches = session.query(Match).filter(Match.event_id == event_id).all()
        
        result = []
        for m in matches:
            p1 = session.query(Player).filter(Player.id == m.player_1_id).first()
            p2 = session.query(Player).filter(Player.id == m.player_2_id).first()
            
            winner = session.query(Player).filter(Player.id == m.winner_id).first() if m.winner_id else None
            
            result.append(MatchResponse(
                id=m.id,
                event_id=m.event_id,
                player_1_id=m.player_1_id,
                player_2_id=m.player_2_id,
                winner_id=m.winner_id,
                player_1_name=p1.name if p1 else "Desconhecido",
                player_2_name=p2.name if p2 else "Desconhecido",
                winner_name=winner.name if winner else None,
                player_1_elo=p1.initial_elo if p1 else 0,
                player_2_elo=p2.initial_elo if p2 else 0,
                created_at=m.created_at,
                updated_at=m.updated_at
            ))
        
        log.info(f"Listadas {len(result)} partidas do evento {event_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Erro ao listar partidas: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.put("/{match_id}", response_model=MatchResponse)
async def update_match(
    match_id: int,
    match_data: MatchUpdate,
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """
    Atualizar resultado de uma partida.
    
    Permite alterar o vencedor e recalcula Elo.
    """
    session = SessionLocal()
    try:
        # Validar partida existe
        match = session.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="Partida não encontrada")
        
        # Validar novo vencedor é um dos dois jogadores (APENAS se foi informado)
        if match_data.winner_id is not None:
            if match_data.winner_id not in [match.player_1_id, match.player_2_id]:
                raise HTTPException(
                    status_code=400,
                    detail="Vencedor deve ser um dos dois jogadores"
                )
        
        # Obter jogadores
        p1 = session.query(Player).filter(Player.id == match.player_1_id).first()
        p2 = session.query(Player).filter(Player.id == match.player_2_id).first()
        
        # Reverter Elo anterior (se havia vencedor)
        if match.winner_id is not None:
            if match.winner_id == match.player_1_id:
                elo_change_old = calculate_elo_change(p1.initial_elo, p2.initial_elo)
                p1.initial_elo -= elo_change_old
                p2.initial_elo += elo_change_old
            else:
                elo_change_old = calculate_elo_change(p2.initial_elo, p1.initial_elo)
                p2.initial_elo -= elo_change_old
                p1.initial_elo += elo_change_old
        
        # Aplicar novo Elo (se novo vencedor foi informado)
        winner_name = None
        if match_data.winner_id is not None:
            if match_data.winner_id == match.player_1_id:
                elo_change_new = calculate_elo_change(p1.initial_elo, p2.initial_elo)
                p1.initial_elo += elo_change_new
                p2.initial_elo -= elo_change_new
                winner_name = p1.name
            else:
                elo_change_new = calculate_elo_change(p2.initial_elo, p1.initial_elo)
                p2.initial_elo += elo_change_new
                p1.initial_elo -= elo_change_new
                winner_name = p2.name
        
        # Atualizar partida
        match.winner_id = match_data.winner_id
        
        session.commit()
        session.refresh(match)
        session.refresh(p1)
        session.refresh(p2)
        
        log.info(f"[{usuario.email}] Partida {match_id} atualizada. Novo vencedor: {winner_name}")
        log.info(f"Novo Elo - {p1.name}: {p1.initial_elo:.1f}, {p2.name}: {p2.initial_elo:.1f}")
        
        return MatchResponse(
            id=match.id,
            event_id=match.event_id,
            player_1_id=match.player_1_id,
            player_2_id=match.player_2_id,
            winner_id=match.winner_id,
            player_1_name=p1.name,
            player_2_name=p2.name,
            winner_name=winner_name,
            player_1_elo=p1.initial_elo,
            player_2_elo=p2.initial_elo,
            created_at=match.created_at,
            updated_at=match.updated_at
        )
        
        # Obter jogadores
        p1 = session.query(Player).filter(Player.id == match.player_1_id).first()
        p2 = session.query(Player).filter(Player.id == match.player_2_id).first()
        
        # Reverter Elo APENAS se winner_id não é NULL
        if match.winner_id is not None:
            if match.winner_id == match.player_1_id:
                elo_change = calculate_elo_change(p1.initial_elo, p2.initial_elo)
                p1.initial_elo -= elo_change
                p2.initial_elo += elo_change
            else:
                elo_change = calculate_elo_change(p2.initial_elo, p1.initial_elo)
                p2.initial_elo -= elo_change
                p1.initial_elo += elo_change
        
        # Deletar partida
        session.delete(match)
        session.commit()
        
        log.info(f"[{usuario.email}] Partida {match_id} deletada. Elo revertido.")
        log.info(f"Novo Elo - {p1.name}: {p1.initial_elo:.1f}, {p2.name}: {p2.initial_elo:.1f}")
        
        return {
            "mensagem": "Partida deletada com sucesso",
            "match_id": match_id
        }
        
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao deletar partida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
