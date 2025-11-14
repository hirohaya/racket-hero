"""Modelo de Evento para Torneios."""

from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Event(Base):
    """
    Modelo de Evento - Representa um torneio/evento de ping-pong.
    
    Attributes:
        id: Primary key
        name: Nome do evento
        date: Data no formato YYYY-MM-DD
        time: Hora no formato HH:MM
        active: Flag para soft delete
    """
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(String)  # YYYY-MM-DD format
    time = Column(String)  # HH:MM format
    active = Column(Boolean, default=True)
