"""
ranking.py - Router para gerenciar rankings
"""

from fastapi import APIRouter, HTTPException
from typing import List
from database import SessionLocal
from models import Player, Match
from logger import get_logger

log = get_logger("ranking_router")

router = APIRouter()

@router.get("/{event_id}", response_model=List[dict])
async def get_ranking(event_id: int):
    """Obter ranking de um evento (ordenado por Elo)"""
    session = SessionLocal()
    try:
        # Buscar jogadores do evento
        players = session.query(Player).filter(Player.event_id == event_id).all()
        
        if not players:
            return []
        
        # Buscar partidas para calcular vitórias
        matches = session.query(Match).filter(Match.event_id == event_id).all()
        
        # Contar vitórias por jogador
        victories = {}
        for player in players:
            victories[player.id] = len([m for m in matches if m.winner_id == player.id])
        
        # Montar ranking
        ranking = [
            {
                "rank": idx + 1,
                "player_id": p.id,
                "name": p.name,
                "elo": round(p.initial_elo, 1),
                "victories": victories.get(p.id, 0),
                "matches": len([m for m in matches if m.player_1_id == p.id or m.player_2_id == p.id])
            }
            for idx, p in enumerate(sorted(players, key=lambda x: x.initial_elo, reverse=True))
        ]
        
        log.info(f"Ranking gerado para evento {event_id}: {len(ranking)} jogadores")
        
        return ranking
    except Exception as e:
        log.error(f"Erro ao obter ranking: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        session.close()
