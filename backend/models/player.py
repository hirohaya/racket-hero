"""Modelo de Jogador para Eventos de Ping-Pong."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Player(Base):
    """
    Modelo de Jogador - Jogador registrado em um evento.
    
    Attributes:
        id: Primary key
        event_id: ID do evento (FK)
        name: Nome do jogador
        initial_elo: Rating Elo inicial
    """
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), index=True)
    name = Column(String, index=True)
    initial_elo = Column(Float, default=1600.0)
