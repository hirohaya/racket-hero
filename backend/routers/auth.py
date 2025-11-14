# routers/auth.py - Endpoints de autenticação

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import os

from database import get_db
from models.usuario import Usuario
from schemas.auth import (
    RegistroRequest, LoginRequest, TokenResponse, RefreshTokenRequest,
    ForgotPasswordRequest, ResetPasswordRequest, UsuarioResponse, ErrorResponse
)
from utils.security import (
    hash_password, verify_password, create_access_token, create_refresh_token,
    verify_token, create_reset_password_token, verify_reset_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter()

# ============================================================================
# POST /auth/register - Registrar novo usuário
# ============================================================================
@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}}
)
async def register(
    request: RegistroRequest,
    db: Session = Depends(get_db)
):
    """
    Registrar novo usuário.
    
    **Validações:**
    - Email deve ser único
    - Senha mínimo 8 caracteres
    - Nome mínimo 3 caracteres
    
    **Response:** TokenResponse com access_token e refresh_token
    """
    # Verificar se email já existe
    usuario_existente = db.query(Usuario).filter(Usuario.email == request.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado",
            headers={"error_code": "EMAIL_EXISTS"}
        )
    
    # Criar novo usuário
    novo_usuario = Usuario(
        email=request.email,
        nome=request.nome,
        senha_hash=hash_password(request.senha),
        tipo="usuario",
        ativo=True
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    # Criar tokens
    access_token = create_access_token(novo_usuario.id, novo_usuario.email, novo_usuario.tipo)
    refresh_token = create_refresh_token(novo_usuario.id, novo_usuario.email)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        usuario={
            "id": novo_usuario.id,
            "email": novo_usuario.email,
            "nome": novo_usuario.nome,
            "tipo": novo_usuario.tipo
        }
    )

# ============================================================================
# POST /auth/login - Login de usuário
# ============================================================================
@router.post(
    "/login",
    response_model=TokenResponse,
    responses={401: {"model": ErrorResponse}}
)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login de usuário.
    
    **Validações:**
    - Email deve existir
    - Senha deve ser correta
    
    **Response:** TokenResponse com access_token e refresh_token
    """
    # Buscar usuário por email
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"error_code": "INVALID_CREDENTIALS"}
        )
    
    # Verificar senha
    if not verify_password(request.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"error_code": "INVALID_CREDENTIALS"}
        )
    
    # Verificar se usuário está ativo
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
            headers={"error_code": "USER_INACTIVE"}
        )
    
    # Criar tokens
    access_token = create_access_token(usuario.id, usuario.email, usuario.tipo)
    refresh_token = create_refresh_token(usuario.id, usuario.email)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        usuario={
            "id": usuario.id,
            "email": usuario.email,
            "nome": usuario.nome,
            "tipo": usuario.tipo
        }
    )

# ============================================================================
# POST /auth/refresh - Refresh access token
# ============================================================================
@router.post(
    "/refresh",
    response_model=TokenResponse,
    responses={401: {"model": ErrorResponse}}
)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Renovar access token usando refresh token.
    
    **Validações:**
    - Refresh token deve ser válido
    - Usuário deve existir e estar ativo
    
    **Response:** TokenResponse com novo access_token
    """
    # Verificar refresh token
    token_data = verify_token(request.refresh_token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
            headers={"error_code": "INVALID_TOKEN"}
        )
    
    # Buscar usuário
    usuario = db.query(Usuario).filter(Usuario.id == token_data.usuario_id).first()
    
    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo",
            headers={"error_code": "USER_NOT_FOUND"}
        )
    
    # Criar novo access token
    access_token = create_access_token(usuario.id, usuario.email, usuario.tipo)
    new_refresh_token = create_refresh_token(usuario.id, usuario.email)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        usuario={
            "id": usuario.id,
            "email": usuario.email,
            "nome": usuario.nome,
            "tipo": usuario.tipo
        }
    )

# ============================================================================
# POST /auth/forgot-password - Solicitar reset de senha
# ============================================================================
@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    responses={404: {"model": ErrorResponse}}
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Solicitar reset de senha.
    
    Envia email com token para resetar senha (válido por 30 minutos).
    
    **Validações:**
    - Email deve existir
    
    **Response:** {"message": "Email enviado com instruções de reset"}
    """
    # Buscar usuário
    usuario = db.query(Usuario).filter(Usuario.email == request.email).first()
    
    if not usuario:
        # Não revelamos se email existe ou não (segurança)
        return {"message": "Se o email existe, você receberá instruções de reset"}
    
    # Criar token de reset
    reset_token, expires_at = create_reset_password_token(usuario.id)
    
    # Salvar token no banco
    usuario.reset_token = reset_token
    usuario.reset_token_expires = expires_at
    db.commit()
    
    # TODO: Enviar email com token
    # send_reset_password_email(usuario.email, reset_token)
    
    return {
        "message": "Se o email existe, você receberá instruções de reset",
        "token": reset_token  # Apenas para testes (remover em produção)
    }

# ============================================================================
# POST /auth/reset-password - Resetar senha
# ============================================================================
@router.post(
    "/reset-password",
    response_model=TokenResponse,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Resetar senha usando token válido.
    
    **Validações:**
    - Token deve ser válido e não expirado
    - Nova senha deve ter mínimo 8 caracteres
    
    **Response:** TokenResponse com novo access_token
    """
    # Verificar token
    usuario_id = verify_reset_token(request.token)
    
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"error_code": "INVALID_TOKEN"}
        )
    
    # Buscar usuário
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"error_code": "USER_NOT_FOUND"}
        )
    
    # Atualizar senha
    usuario.senha_hash = hash_password(request.nova_senha)
    usuario.reset_token = None
    usuario.reset_token_expires = None
    db.commit()
    db.refresh(usuario)
    
    # Criar tokens
    access_token = create_access_token(usuario.id, usuario.email, usuario.tipo)
    refresh_token = create_refresh_token(usuario.id, usuario.email)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        usuario={
            "id": usuario.id,
            "email": usuario.email,
            "nome": usuario.nome,
            "tipo": usuario.tipo
        }
    )

# ============================================================================
# GET /auth/me - Obter dados do usuário autenticado
# ============================================================================
@router.get(
    "/me",
    response_model=UsuarioResponse,
    responses={401: {"model": ErrorResponse}}
)
async def get_current_user(
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """
    Obter dados do usuário autenticado.
    
    **Requisitos:**
    - Header Authorization: "Bearer <access_token>"
    
    **Response:** UsuarioResponse com dados do usuário
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido",
            headers={"error_code": "NO_TOKEN"}
        )
    
    token = authorization.replace("Bearer ", "")
    token_data = verify_token(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"error_code": "INVALID_TOKEN"}
        )
    
    usuario = db.query(Usuario).filter(Usuario.id == token_data.usuario_id).first()
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
            headers={"error_code": "USER_NOT_FOUND"}
        )
    
    return UsuarioResponse(
        id=usuario.id,
        email=usuario.email,
        nome=usuario.nome,
        tipo=usuario.tipo,
        ativo=usuario.ativo,
        criado_em=usuario.criado_em.isoformat()
    )
