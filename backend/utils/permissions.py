# utils/permissions.py - Sistema de Permissões

from enum import Enum
from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario, TipoUsuario
from utils.security import verify_token
from logger import get_logger

log = get_logger("permissions")

class Permissao(str, Enum):
    """Permissões disponíveis no sistema"""
    # Eventos
    VER_EVENTOS = "ver_eventos"
    CRIAR_EVENTO = "criar_evento"
    EDITAR_EVENTO = "editar_evento"
    DELETAR_EVENTO = "deletar_evento"
    
    # Partidas
    VER_PARTIDAS = "ver_partidas"
    CRIAR_PARTIDA = "criar_partida"
    EDITAR_PARTIDA = "editar_partida"
    DELETAR_PARTIDA = "deletar_partida"
    
    # Ranking
    VER_RANKING = "ver_ranking"
    
    # Usuários
    VER_USUARIOS = "ver_usuarios"
    EDITAR_USUARIO = "editar_usuario"
    DELETAR_USUARIO = "deletar_usuario"
    
    # Relatórios
    VER_RELATORIOS = "ver_relatorios"


# Matriz de permissões por tipo de usuário
PERMISSOES_POR_TIPO = {
    TipoUsuario.JOGADOR: {
        Permissao.VER_EVENTOS,
        Permissao.VER_PARTIDAS,
        Permissao.VER_RANKING,
    },
    TipoUsuario.ORGANIZADOR: {
        Permissao.VER_EVENTOS,
        Permissao.CRIAR_EVENTO,
        Permissao.EDITAR_EVENTO,
        Permissao.VER_PARTIDAS,
        Permissao.CRIAR_PARTIDA,
        Permissao.EDITAR_PARTIDA,
        Permissao.VER_RANKING,
        Permissao.VER_RELATORIOS,
    },
    TipoUsuario.ADMIN: {
        # Admin tem todas as permissões
        Permissao.VER_EVENTOS,
        Permissao.CRIAR_EVENTO,
        Permissao.EDITAR_EVENTO,
        Permissao.DELETAR_EVENTO,
        Permissao.VER_PARTIDAS,
        Permissao.CRIAR_PARTIDA,
        Permissao.EDITAR_PARTIDA,
        Permissao.DELETAR_PARTIDA,
        Permissao.VER_RANKING,
        Permissao.VER_USUARIOS,
        Permissao.EDITAR_USUARIO,
        Permissao.DELETAR_USUARIO,
        Permissao.VER_RELATORIOS,
    }
}


def obter_permissoes(tipo_usuario: TipoUsuario) -> set:
    """
    Obter permissões de um tipo de usuário.
    
    Suporta tipos legados:
    - "usuario" → JOGADOR (permissions)
    - "organizador" → ORGANIZADOR (permissions)
    - "admin" → ADMIN (all permissions)
    """
    # Se for string (tipo legado), converter para tipo enum equivalente
    if isinstance(tipo_usuario, str):
        tipo_map = {
            "usuario": TipoUsuario.JOGADOR,
            "organizador": TipoUsuario.ORGANIZADOR,
            "admin": TipoUsuario.ADMIN
        }
        tipo_usuario = tipo_map.get(tipo_usuario, TipoUsuario.JOGADOR)
    
    return PERMISSOES_POR_TIPO.get(tipo_usuario, set())


def tem_permissao(usuario: Usuario, permissao: Permissao) -> bool:
    """Verificar se um usuário tem uma permissão"""
    if not usuario.ativo:
        return False
    permissoes = obter_permissoes(usuario.tipo)
    return permissao in permissoes


async def get_usuario_autenticado(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Dependency para obter o usuário autenticado a partir do token.
    
    Lança HTTPException 401 se:
    - Token não fornecido
    - Token inválido ou expirado
    - Usuário não encontrado
    - Usuário inativo
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
    
    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
            headers={"error_code": "USER_INACTIVE"}
        )
    
    return usuario


def require_permission(permissao: Permissao):
    """
    Decorator para exigir uma permissão específica.
    
    Exemplo:
        @router.get("/eventos")
        async def listar_eventos(usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))):
            return eventos
    """
    async def verificar_permissao(
        usuario: Usuario = Depends(get_usuario_autenticado)
    ) -> Usuario:
        if not tem_permissao(usuario, permissao):
            log.warning(f"Acesso negado para usuário {usuario.email}: permissão {permissao.value} necessária")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permissão necessária: {permissao.value}",
                headers={"error_code": "PERMISSION_DENIED"}
            )
        return usuario
    
    return verificar_permissao


def require_tipo(tipo_minimo: TipoUsuario):
    """
    Decorator para exigir um tipo de usuário mínimo.
    
    Hierarquia: JOGADOR < ORGANIZADOR < ADMIN
    
    Mapeamento de tipos legados:
    - "usuario" → JOGADOR
    - "organizador" → ORGANIZADOR
    - "admin" → ADMIN
    
    Exemplo:
        @router.post("/eventos")
        async def criar_evento(usuario: Usuario = Depends(require_tipo(TipoUsuario.ORGANIZADOR))):
            return evento
    """
    async def verificar_tipo(
        usuario: Usuario = Depends(get_usuario_autenticado)
    ) -> Usuario:
        hierarquia = {
            TipoUsuario.JOGADOR: 0,
            TipoUsuario.ORGANIZADOR: 1,
            TipoUsuario.ADMIN: 2,
            # Mapeamento de tipos legados (pré-enum)
            "usuario": 0,
            "organizador": 1,
            "admin": 2
        }
        
        nivel_usuario = hierarquia.get(usuario.tipo, -1)
        nivel_minimo = hierarquia.get(tipo_minimo, 0)
        
        if nivel_usuario < nivel_minimo:
            log.warning(f"Acesso negado para usuário {usuario.email}: tipo {tipo_minimo.value} necessário (tipo atual: {usuario.tipo})")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Tipo de usuário necessário: {tipo_minimo.value}",
                headers={"error_code": "INSUFFICIENT_ROLE"}
            )
        return usuario
    
    return verificar_tipo
