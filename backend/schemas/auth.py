# schemas/auth.py - Pydantic schemas para autenticação

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional

class RegistroRequest(BaseModel):
    """Schema para requisição de registro"""
    email: EmailStr
    nome: str
    senha: str
    tipo: Optional[str] = "usuario"  # Padrão: usuario (jogador), pode ser "organizador"
    
    @field_validator('nome')
    @classmethod
    def nome_minimo(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Nome deve ter no mínimo 3 caracteres')
        return v.strip()
    
    @field_validator('senha')
    @classmethod
    def senha_minima(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@example.com",
                "nome": "João Silva",
                "senha": "senha123456",
                "tipo": "usuario"
            }
        }
    )

class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    email: EmailStr
    senha: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@example.com",
                "senha": "senha123456"
            }
        }
    )

class TokenResponse(BaseModel):
    """Schema para resposta com tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos
    usuario: dict
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGc...",
                "refresh_token": "eyJhbGc...",
                "token_type": "bearer",
                "expires_in": 900,
                "usuario": {
                    "id": 1,
                    "email": "usuario@example.com",
                    "nome": "João Silva",
                    "tipo": "usuario"
                }
            }
        }
    )

class RefreshTokenRequest(BaseModel):
    """Schema para refresh token"""
    refresh_token: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGc..."
            }
        }
    )

class ForgotPasswordRequest(BaseModel):
    """Schema para solicitar reset de senha"""
    email: EmailStr
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "usuario@example.com"
            }
        }
    )

class ResetPasswordRequest(BaseModel):
    """Schema para resetar senha"""
    token: str
    nova_senha: str
    
    @field_validator('nova_senha')
    @classmethod
    def senha_minima(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "token": "eyJhbGc...",
                "nova_senha": "novaSenha123456"
            }
        }
    )

class UsuarioResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: int
    email: str
    nome: str
    tipo: str
    ativo: bool
    criado_em: str
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "usuario@example.com",
                "nome": "João Silva",
                "tipo": "usuario",
                "ativo": True,
                "criado_em": "2025-11-14T15:30:00"
            }
        }
    )

class ErrorResponse(BaseModel):
    """Schema para resposta de erro"""
    detail: str
    error_code: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Email já registrado",
                "error_code": "EMAIL_EXISTS"
            }
        }
    )
