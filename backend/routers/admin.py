# routers/admin.py - Endpoints administrativos

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backup_manager import backup_endpoint_handler, BackupManager
from database import get_db
from models import Usuario
from logger_production import get_logger

router = APIRouter(prefix="/api/admin", tags=["admin"])
logger = get_logger("admin")

# Dependency para verificar se é admin
async def get_current_admin_user(db: Session = Depends(get_db)):
    """Verificar se usuário é admin (por enquanto, simulado)"""
    # Em produção, implementar autenticação real
    # Por enquanto, apenas log que foi acessado
    logger.info("Admin endpoint acessado")
    return True

@router.post("/backup", status_code=201)
async def manual_backup(admin: bool = Depends(get_current_admin_user)):
    """
    Criar backup manual do banco de dados
    
    **Require**: Admin access
    
    **Response**:
    - `success`: Se o backup foi criado com sucesso
    - `filename`: Nome do arquivo de backup
    - `message`: Mensagem descritiva
    """
    try:
        logger.info("Iniciando backup manual")
        result = backup_endpoint_handler()
        logger.info(f"Backup criado com sucesso: {result.get('filename')}")
        return result
    except Exception as e:
        logger.error(f"Erro ao criar backup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/backups")
async def list_backups(admin: bool = Depends(get_current_admin_user)):
    """
    Listar todos os backups disponíveis
    
    **Require**: Admin access
    
    **Response**:
    - `backups`: Lista de backups com metadados
    """
    try:
        logger.info("Listando backups")
        manager = BackupManager()
        backups = manager.list_backups()
        logger.info(f"Total de backups: {len(backups)}")
        return {"backups": backups, "total": len(backups)}
    except Exception as e:
        logger.error(f"Erro ao listar backups: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/backups/{filename}/restore", status_code=200)
async def restore_backup(filename: str, admin: bool = Depends(get_current_admin_user)):
    """
    Restaurar banco de um backup
    
    **Require**: Admin access
    
    **Parameters**:
    - `filename`: Nome do arquivo de backup a restaurar
    
    **Response**:
    - `success`: Se a restauração foi bem-sucedida
    - `message`: Mensagem descritiva
    - `backup_file_created`: Backup do estado anterior criado
    """
    try:
        logger.info(f"Iniciando restauração de backup: {filename}")
        manager = BackupManager()
        success, msg = manager.restore_backup(filename)
        
        if success:
            logger.info(f"Backup restaurado com sucesso: {filename}")
            return {
                "success": True,
                "message": msg,
                "backup_file_created": f"backup_before_restore_{filename}"
            }
        else:
            logger.warning(f"Falha ao restaurar backup: {msg}")
            raise HTTPException(status_code=400, detail=msg)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao restaurar backup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/backups/{filename}", status_code=200)
async def delete_backup(filename: str, admin: bool = Depends(get_current_admin_user)):
    """
    Deletar um backup
    
    **Require**: Admin access
    
    **Parameters**:
    - `filename`: Nome do arquivo de backup a deletar
    
    **Response**:
    - `success`: Se o backup foi deletado
    - `message`: Mensagem descritiva
    """
    try:
        logger.info(f"Deletando backup: {filename}")
        manager = BackupManager()
        success, msg = manager.delete_backup(filename)
        
        if success:
            logger.info(f"Backup deletado: {filename}")
            return {"success": True, "message": msg}
        else:
            logger.warning(f"Falha ao deletar backup: {msg}")
            raise HTTPException(status_code=400, detail=msg)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar backup: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/system/health")
async def system_health(admin: bool = Depends(get_current_admin_user)):
    """
    Verificar saúde do sistema
    
    **Require**: Admin access
    
    **Response**:
    - `status`: Status geral do sistema
    - `database`: Status do banco de dados
    - `backups`: Último backup criado
    - `logs`: Últimas linhas do log
    """
    import os
    from datetime import datetime
    
    try:
        logger.info("Health check solicitado")
        
        # Verificar banco de dados
        db_file = "racket_hero.db"
        db_exists = os.path.exists(db_file)
        db_size = os.path.getsize(db_file) if db_exists else 0
        
        # Verificar últimos backups
        manager = BackupManager()
        backups = manager.list_backups()
        last_backup = backups[0] if backups else None
        
        # Verificar logs
        log_file = "logs/app.log"
        last_logs = []
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                lines = f.readlines()
                last_logs = lines[-5:] if len(lines) > 5 else lines
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": {
                "exists": db_exists,
                "size_bytes": db_size,
                "size_mb": round(db_size / (1024 * 1024), 2)
            },
            "backups": {
                "total": len(backups),
                "last_backup": last_backup
            },
            "logs": {
                "recent_lines": len(last_logs),
                "content": last_logs[-3:] if last_logs else []
            }
        }
    except Exception as e:
        logger.error(f"Erro no health check: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seed-test-accounts", status_code=201)
async def seed_test_accounts(db: Session = Depends(get_db)):
    """
    Criar contas de teste no banco de dados.
    
    **Endpoints**: Jogador e Organizador
    
    **Response**:
    - `success`: Se as contas foram criadas
    - `message`: Mensagem descritiva
    - `accounts`: Lista de contas criadas
    """
    from models.usuario import TipoUsuario
    from utils.security import hash_password
    
    try:
        logger.info("Iniciando seed de contas de teste")
        
        # Dados das contas de teste
        test_accounts = [
            {
                "email": "jogador@test.com",
                "nome": "Jogador Teste",
                "senha": "Senha123!",
                "tipo": TipoUsuario.JOGADOR
            },
            {
                "email": "organizador@test.com",
                "nome": "Organizador Teste",
                "senha": "Senha123!",
                "tipo": TipoUsuario.ORGANIZADOR
            }
        ]
        
        created_accounts = []
        
        # Criar cada conta
        for account in test_accounts:
            # Verificar se já existe
            usuario_existente = db.query(Usuario).filter(
                Usuario.email == account["email"]
            ).first()
            
            if usuario_existente:
                logger.info(f"Conta já existe: {account['email']} (id: {usuario_existente.id})")
                created_accounts.append({
                    "email": usuario_existente.email,
                    "tipo": usuario_existente.tipo,
                    "status": "already_exists"
                })
                continue
            
            # Criar nova conta
            novo_usuario = Usuario(
                email=account["email"],
                nome=account["nome"],
                senha_hash=hash_password(account["senha"]),
                tipo=account["tipo"],
                ativo=True
            )
            
            db.add(novo_usuario)
            db.commit()
            db.refresh(novo_usuario)
            
            logger.info(f"Conta criada: {novo_usuario.email} (tipo: {novo_usuario.tipo}, id: {novo_usuario.id})")
            created_accounts.append({
                "email": novo_usuario.email,
                "tipo": novo_usuario.tipo,
                "status": "created"
            })
        
        return {
            "success": True,
            "message": f"Seed de contas de teste concluído",
            "accounts": created_accounts
        }
        
    except Exception as e:
        logger.error(f"Erro ao fazer seed de contas: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

