"""Modelo de associação Evento-Organizador (Many-to-Many)."""

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from database import Base


class EventoOrganizador(Base):
    """
    Modelo de associação muitos-para-muitos entre Eventos e Organizadores.
    
    Permite que um evento tenha múltiplos organizadores.
    
    Attributes:
        id: Primary key
        event_id: ID do evento (FK para event)
        usuario_id: ID do usuário/organizador (FK para usuarios)
        criado_em: Timestamp de quando o organizador foi adicionado
        é_criador: Flag indicando se foi o criador original do evento
    """
    __tablename__ = "evento_organizador"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("event.id"), index=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=False)
    criado_em = Column(DateTime, default=func.now())
    é_criador = Column(Integer, default=0)  # 1 = foi o criador, 0 = adicionado depois
