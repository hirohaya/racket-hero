# schemas/matches.py - Pydantic models para partidas

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class MatchCreate(BaseModel):
    """Schema para criar uma partida"""
    event_id: int
    player_1_id: int
    player_2_id: int
    winner_id: Optional[int] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "event_id": 1,
                "player_1_id": 5,
                "player_2_id": 6,
                "winner_id": 5
            }
        }
    )


class MatchUpdate(BaseModel):
    """Schema para atualizar resultado de uma partida"""
    winner_id: Optional[int] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "winner_id": 6
            }
        }
    )


class PlayerInfo(BaseModel):
    """Info do jogador para resposta"""
    id: int
    name: str
    initial_elo: float


class MatchResponse(BaseModel):
    """Schema de resposta para partida com informações dos jogadores"""
    id: int
    event_id: int
    player_1_id: int
    player_2_id: int
    winner_id: Optional[int] = None
    player_1_name: Optional[str] = None
    player_2_name: Optional[str] = None
    winner_name: Optional[str] = None
    player_1_elo: Optional[float] = None
    player_2_elo: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "event_id": 1,
                "player_1_id": 5,
                "player_2_id": 6,
                "winner_id": 5,
                "player_1_name": "jogador1",
                "player_2_name": "jogador2",
                "winner_name": "jogador1",
                "player_1_elo": 1620.5,
                "player_2_elo": 1579.5,
                "created_at": "2025-11-18T15:30:00",
                "updated_at": "2025-11-18T15:30:00"
            }
        }
    )


class MatchList(BaseModel):
    """Schema simples para listar partidas"""
    id: int
    event_id: int
    player_1_name: str
    player_2_name: str
    winner_name: str
    player_1_elo: float
    player_2_elo: float
