"""
matches.py - Router para gerenciar partidas
"""

from fastapi import APIRouter, HTTPException
from typing import List
from database import SessionLocal
from models import Match, Player
from logger import get_logger

log = get_logger("matches_router")

# Função simples de cálculo de Elo
def calculate_elo_change(winner_elo: float, loser_elo: float, k_factor: int = 32) -> float:
    """
    Calcula mudança de Elo após partida
    K-factor padrão de 32 para jogadores normais
    """
    expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    elo_change = k_factor * (1 - expected_winner)
    return elo_change

router = APIRouter()

@router.post("", response_model=dict)
async def create_match(match_data: dict):
    """Criar nova partida e atualizar Elo dos jogadores"""
    session = SessionLocal()
    try:
        # Validar jogadores
        p1 = session.query(Player).filter(Player.id == match_data["player_1_id"]).first()
        p2 = session.query(Player).filter(Player.id == match_data["player_2_id"]).first()
        
        if not p1 or not p2:
            raise HTTPException(status_code=404, detail="Jogador não encontrado")
        
        if p1.event_id != p2.event_id:
            raise HTTPException(status_code=400, detail="Jogadores devem ser do mesmo evento")
        
        # Criar partida
        match = Match(
            event_id=match_data["event_id"],
            player_1_id=match_data["player_1_id"],
            player_2_id=match_data["player_2_id"],
            winner_id=match_data["winner_id"]
        )
        
        # Calcular novo Elo (simplificado - apenas para vencedor)
        if match_data["winner_id"] == match_data["player_1_id"]:
            elo_change = calculate_elo_change(p1.initial_elo, p2.initial_elo)
            p1.initial_elo += elo_change
            p2.initial_elo -= elo_change
            winner_name = p1.name
        else:
            elo_change = calculate_elo_change(p2.initial_elo, p1.initial_elo)
            p2.initial_elo += elo_change
            p1.initial_elo -= elo_change
            winner_name = p2.name
        
        session.add(match)
        session.commit()
        session.refresh(match)
        
        log.info(f"Partida criada: {p1.name} vs {p2.name}, Vencedor: {winner_name}")
        log.info(f"Novo Elo - {p1.name}: {p1.initial_elo:.0f}, {p2.name}: {p2.initial_elo:.0f}")
        
        return {
            "id": match.id,
            "event_id": match.event_id,
            "player_1_id": match.player_1_id,
            "player_2_id": match.player_2_id,
            "winner_id": match.winner_id
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        log.error(f"Erro ao criar partida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()

@router.get("/{event_id}", response_model=List[dict])
async def list_matches(event_id: int):
    """Listar partidas de um evento"""
    session = SessionLocal()
    try:
        matches = session.query(Match).filter(Match.event_id == event_id).all()
        
        return [
            {
                "id": m.id,
                "event_id": m.event_id,
                "player_1_id": m.player_1_id,
                "player_2_id": m.player_2_id,
                "winner_id": m.winner_id
            }
            for m in matches
        ]
    except Exception as e:
        log.error(f"Erro ao listar partidas: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
