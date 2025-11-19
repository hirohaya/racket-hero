"""Modelo de Jogador para Eventos de Ping-Pong."""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Player(Base):
    """
    Modelo de Jogador - Jogador registrado em um evento.
    
    Attributes:
        id: Primary key
        event_id: ID do evento (FK)
        usuario_id: ID do usuário (FK) - Link para usuario que se registrou
        name: Nome do jogador
        club: Clube do jogador (opcional)
        initial_elo: Rating Elo inicial
    """
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=True)
    name = Column(String, index=True)
    club = Column(String, nullable=True)
    initial_elo = Column(Float, default=1600.0)

