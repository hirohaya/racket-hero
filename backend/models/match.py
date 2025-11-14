"""Modelo de Partida para Torneios de Ping-Pong."""

from sqlalchemy import Column, Integer, ForeignKey
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
    """
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), index=True)
    player_1_id = Column(Integer, ForeignKey("player.id"), index=True)
    player_2_id = Column(Integer, ForeignKey("player.id"), index=True)
    winner_id = Column(Integer, ForeignKey("player.id"), index=True)
