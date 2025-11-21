"""Modelo de Evento para Torneios."""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Event(Base):
    """
    Modelo de Evento - Representa um torneio/evento de ping-pong.
    
    Attributes:
        id: Primary key
        name: Nome do evento
        date: Data no formato YYYY-MM-DD
        time: Hora no formato HH:MM
        usuario_id: ID do usuário (organizador) que criou o evento
        active: Flag para soft delete
    """
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    date = Column(String, nullable=False)  # YYYY-MM-DD format
    time = Column(String, nullable=False)  # HH:MM format
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=True)
    active = Column(Boolean, default=True)
