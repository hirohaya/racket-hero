# utils/security.py - Utilidades de segurança (JWT, bcrypt)

from datetime import datetime, timedelta, timezone
from typing import Optional
import os
import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel

# Configurações de segurança
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Schemas para tokens
class TokenData(BaseModel):
    """Dados do token JWT"""
    usuario_id: int
    email: str
    tipo: str  # 'usuario' ou 'admin'

class TokenResponse(BaseModel):
    """Resposta com tokens"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # segundos

# Funções de senha com bcrypt direto
def hash_password(password: str) -> str:
    """
    Hash de senha usando bcrypt.
    
    Args:
        password: Senha em texto plano
        
    Returns:
        Hash bcrypt da senha
    """
    # Limitar senha a 72 bytes (limite do bcrypt)
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar senha contra hash.
    
    Args:
        plain_password: Senha em texto plano
        hashed_password: Hash armazenado
        
    Returns:
        True se senha é válida, False caso contrário
    """
    password_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

# Funções de JWT
def create_access_token(usuario_id: int, email: str, tipo: str) -> str:
    """
    Criar token de acesso JWT.
    
    Args:
        usuario_id: ID do usuário
        email: Email do usuário
        tipo: Tipo de usuário ('usuario' ou 'admin')
        
    Returns:
        Token JWT assinado
        
    Exemplo:
        token = create_access_token(1, "user@example.com", "usuario")
    """
    to_encode = {
        "usuario_id": usuario_id,
        "email": email,
        "tipo": tipo,
        "iat": datetime.now(timezone.utc),  # Issued at
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "token_type": "access"
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(usuario_id: int, email: str) -> str:
    """
    Criar token de refresh JWT.
    
    Args:
        usuario_id: ID do usuário
        email: Email do usuário
        
    Returns:
        Token JWT de refresh assinado
    """
    to_encode = {
        "usuario_id": usuario_id,
        "email": email,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        "token_type": "refresh"
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """
    Verificar e decodificar token JWT (access ou refresh).
    
    Args:
        token: Token JWT (pode ser access_token ou refresh_token)
        
    Returns:
        TokenData se válido, None se inválido ou expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: int = payload.get("usuario_id")
        email: str = payload.get("email")
        tipo: str = payload.get("tipo", "usuario")  # Default para refresh tokens que não têm tipo
        
        if usuario_id is None or email is None:
            return None
            
        return TokenData(usuario_id=usuario_id, email=email, tipo=tipo)
    except JWTError:
        return None

def create_reset_password_token(usuario_id: int) -> tuple[str, datetime]:
    """
    Criar token para recuperação de senha (válido por 30 minutos).
    
    Args:
        usuario_id: ID do usuário
        
    Returns:
        Tuple (token, expiration_datetime)
    """
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode = {
        "usuario_id": usuario_id,
        "iat": datetime.now(timezone.utc),
        "exp": expires,
        "token_type": "password_reset"
    }
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token, expires

def verify_reset_token(token: str) -> Optional[int]:
    """
    Verificar token de reset de senha.
    
    Args:
        token: Token de reset
        
    Returns:
        usuario_id se válido, None se inválido ou expirado
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: int = payload.get("usuario_id")
        token_type: str = payload.get("token_type")
        
        if usuario_id is None or token_type != "password_reset":
            return None
            
        return usuario_id
    except JWTError:
        return None
