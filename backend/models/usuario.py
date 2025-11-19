# models/usuario.py - Modelo de Usuário

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from database import Base
from datetime import datetime
from enum import Enum

class TipoUsuario(str, Enum):
    """Tipos de usuários no sistema"""
    JOGADOR = "jogador"          # Jogador de torneios
    ORGANIZADOR = "organizador"  # Organizador de eventos
    ADMIN = "admin"              # Administrador do sistema

class Usuario(Base):
    """
    Modelo de usuário para autenticação.
    
    Campos:
    - id: Identificador único (auto-incrementado)
    - email: Email único do usuário (obrigatório)
    - nome: Nome completo (obrigatório)
    - senha_hash: Hash bcrypt da senha (obrigatório)
    - tipo: Tipo de usuário: 'jogador', 'organizador', 'admin' (padrão: 'jogador')
    - ativo: Flag de usuário ativo (padrão: True)
    - reset_token: Token para recuperação de senha (30min válido)
    - reset_token_expires: Expiração do token de reset
    - criado_em: Timestamp de criação (auto-preenchido)
    - atualizado_em: Timestamp de atualização (auto-preenchido)
    
    Permissões por tipo:
    - JOGADOR: Pode ver eventos, participar de torneios, ver rankings
    - ORGANIZADOR: Pode criar/editar eventos, gerenciar partidas, ver relatórios
    - ADMIN: Acesso total ao sistema (gerencia usuários, eventos, tudo)
    """
    
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(String(50), default=TipoUsuario.JOGADOR, nullable=False)  # jogador, organizador, admin
    ativo = Column(Boolean, default=True, nullable=False)
    reset_token = Column(String(255), nullable=True, unique=True)
    reset_token_expires = Column(DateTime, nullable=True)
    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, email={self.email}, nome={self.nome}, tipo={self.tipo})>"
    
    def is_admin(self) -> bool:
        """Verificar se é administrador"""
        return self.tipo == TipoUsuario.ADMIN
    
    def is_organizador(self) -> bool:
        """Verificar se é organizador ou admin"""
        return self.tipo in [TipoUsuario.ORGANIZADOR, TipoUsuario.ADMIN]
    
    def is_jogador(self) -> bool:
        """Verificar se é jogador (todos têm permissão de jogador)"""
        return self.tipo in [TipoUsuario.JOGADOR, TipoUsuario.ORGANIZADOR, TipoUsuario.ADMIN]
