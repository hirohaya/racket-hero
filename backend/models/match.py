"""Modelo de Partida para Torneios de Ping-Pong."""

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class Match(Base):
    """
    Modelo de Partida - Registra resultado de uma partida.
    
    Attributes:
        id: Primary key
        event_id: ID do evento (FK)
        player_1_id: ID do primeiro jogador (FK)
        player_2_id: ID do segundo jogador (FK)
        winner_id: ID do vencedor (FK)
        created_at: Timestamp de criação (auto-preenchido)
        updated_at: Timestamp de atualização (auto-preenchido)
    """
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), index=True)
    player_1_id = Column(Integer, ForeignKey("player.id"), index=True)
    player_2_id = Column(Integer, ForeignKey("player.id"), index=True)
    winner_id = Column(Integer, ForeignKey("player.id"), index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
