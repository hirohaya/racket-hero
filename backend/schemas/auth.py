# schemas/auth.py - Pydantic schemas para autenticação

from pydantic import BaseModel, EmailStr, validator
from typing import Optional

class RegistroRequest(BaseModel):
    """Schema para requisição de registro"""
    email: EmailStr
    nome: str
    senha: str
    
    @validator('nome')
    def nome_minimo(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Nome deve ter no mínimo 3 caracteres')
        return v.strip()
    
    @validator('senha')
    def senha_minima(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "nome": "João Silva",
                "senha": "senha123456"
            }
        }

class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    email: EmailStr
    senha: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "senha": "senha123456"
            }
        }

class TokenResponse(BaseModel):
    """Schema para resposta com tokens"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos
    usuario: dict
    
    class Config:
        schema_extra = {
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

class RefreshTokenRequest(BaseModel):
    """Schema para refresh token"""
    refresh_token: str
    
    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "eyJhbGc..."
            }
        }

class ForgotPasswordRequest(BaseModel):
    """Schema para solicitar reset de senha"""
    email: EmailStr
    
    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com"
            }
        }

class ResetPasswordRequest(BaseModel):
    """Schema para resetar senha"""
    token: str
    nova_senha: str
    
    @validator('nova_senha')
    def senha_minima(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "token": "eyJhbGc...",
                "nova_senha": "novaSenha123456"
            }
        }

class UsuarioResponse(BaseModel):
    """Schema para resposta de usuário"""
    id: int
    email: str
    nome: str
    tipo: str
    ativo: bool
    criado_em: str
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "email": "usuario@example.com",
                "nome": "João Silva",
                "tipo": "usuario",
                "ativo": True,
                "criado_em": "2025-11-14T15:30:00"
            }
        }

class ErrorResponse(BaseModel):
    """Schema para resposta de erro"""
    detail: str
    error_code: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Email já registrado",
                "error_code": "EMAIL_EXISTS"
            }
        }
