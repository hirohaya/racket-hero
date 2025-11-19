"""
Sistema de backup automático para banco de dados SQLite
Implementa backup diário com retenção de backups antigos
"""

import os
import shutil
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import logging
import json
from typing import List, Tuple


logger = logging.getLogger('racket_hero.backup')


class BackupManager:
    """Gerenciar backups do banco de dados"""
    
    def __init__(
        self,
        db_path: str = 'racket_hero.db',
        backup_dir: str = 'backups',
        retention_days: int = 30,
        max_backups: int = 10
    ):
        """
        Inicializar gerenciador de backups
        
        Args:
            db_path: Caminho do banco de dados
            backup_dir: Diretório para armazenar backups
            retention_days: Manter backups por X dias
            max_backups: Número máximo de backups a manter
        """
        self.db_path = db_path
        self.backup_dir = Path(backup_dir)
        self.retention_days = retention_days
        self.max_backups = max_backups
        
        # Criar diretório de backups
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"BackupManager inicializado: {backup_dir}")
    
    def create_backup(self, tag: str = None) -> Tuple[bool, str]:
        """
        Criar backup do banco de dados
        
        Args:
            tag: Tag opcional para identificar o backup
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            # Gerar nome do arquivo
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            tag_str = f'_{tag}' if tag else ''
            backup_filename = f'backup_{timestamp}{tag_str}.db'
            backup_path = self.backup_dir / backup_filename
            
            # Verificar se arquivo de banco existe
            if not Path(self.db_path).exists():
                msg = f"Arquivo de banco de dados não encontrado: {self.db_path}"
                logger.error(msg)
                return False, msg
            
            # Criar backup usando sqlite3
            connection = sqlite3.connect(self.db_path)
            
            # Modo de backup seguro
            backup_connection = sqlite3.connect(str(backup_path))
            with backup_connection:
                connection.backup(backup_connection)
            
            backup_connection.close()
            connection.close()
            
            # Registrar metadados
            self._save_backup_metadata(backup_path)
            
            # Limpar backups antigos
            self._cleanup_old_backups()
            
            msg = f"Backup criado com sucesso: {backup_filename}"
            logger.info(msg)
            return True, msg
        
        except Exception as e:
            msg = f"Erro ao criar backup: {str(e)}"
            logger.error(msg)
            return False, msg
    
    def restore_backup(self, backup_filename: str) -> Tuple[bool, str]:
        """
        Restaurar banco de dados de um backup
        
        Args:
            backup_filename: Nome do arquivo de backup
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            backup_path = self.backup_dir / backup_filename
            
            if not backup_path.exists():
                msg = f"Arquivo de backup não encontrado: {backup_filename}"
                logger.error(msg)
                return False, msg
            
            # Criar backup do DB atual antes de restaurar
            current_backup = self.backup_dir / f'pre_restore_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            if Path(self.db_path).exists():
                shutil.copy(self.db_path, current_backup)
                logger.info(f"Backup pré-restauração criado: {current_backup.name}")
            
            # Restaurar
            shutil.copy(backup_path, self.db_path)
            
            msg = f"Banco restaurado com sucesso de: {backup_filename}"
            logger.info(msg)
            return True, msg
        
        except Exception as e:
            msg = f"Erro ao restaurar backup: {str(e)}"
            logger.error(msg)
            return False, msg
    
    def list_backups(self) -> List[dict]:
        """
        Listar todos os backups disponíveis
        
        Returns:
            Lista de dicionários com informações dos backups
        """
        backups = []
        
        for backup_file in sorted(self.backup_dir.glob('backup_*.db'), reverse=True):
            metadata_file = backup_file.with_suffix('.json')
            
            info = {
                'filename': backup_file.name,
                'size': backup_file.stat().st_size,
                'created': datetime.fromtimestamp(
                    backup_file.stat().st_mtime
                ).isoformat(),
                'size_mb': round(backup_file.stat().st_size / (1024 * 1024), 2)
            }
            
            # Carregar metadados se existir
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                        info.update(metadata)
                except:
                    pass
            
            backups.append(info)
        
        return backups
    
    def delete_backup(self, backup_filename: str) -> Tuple[bool, str]:
        """
        Deletar um backup específico
        
        Args:
            backup_filename: Nome do arquivo de backup
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        try:
            backup_path = self.backup_dir / backup_filename
            
            if not backup_path.exists():
                msg = f"Arquivo de backup não encontrado: {backup_filename}"
                logger.warning(msg)
                return False, msg
            
            backup_path.unlink()
            
            # Deletar metadados também
            metadata_file = backup_path.with_suffix('.json')
            if metadata_file.exists():
                metadata_file.unlink()
            
            msg = f"Backup deletado: {backup_filename}"
            logger.info(msg)
            return True, msg
        
        except Exception as e:
            msg = f"Erro ao deletar backup: {str(e)}"
            logger.error(msg)
            return False, msg
    
    def _save_backup_metadata(self, backup_path: Path):
        """Salvar metadados do backup em JSON"""
        try:
            metadata = {
                'created': datetime.now().isoformat(),
                'size': backup_path.stat().st_size,
                'db_path': self.db_path,
                'retention_until': (
                    datetime.now() + timedelta(days=self.retention_days)
                ).isoformat()
            }
            
            metadata_file = backup_path.with_suffix('.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            logger.warning(f"Erro ao salvar metadados: {str(e)}")
    
    def _cleanup_old_backups(self):
        """Remover backups antigos baseado em retenção e limite máximo"""
        backups = list(self.backup_dir.glob('backup_*.db'))
        
        # Remover por data de retenção
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)
        for backup_file in backups:
            modified_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
            if modified_time < cutoff_date:
                try:
                    backup_file.unlink()
                    metadata_file = backup_file.with_suffix('.json')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    logger.info(f"Backup antigo deletado: {backup_file.name}")
                except Exception as e:
                    logger.warning(f"Erro ao deletar backup antigo: {str(e)}")
        
        # Remover se exceder máximo
        remaining_backups = sorted(
            self.backup_dir.glob('backup_*.db'),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if len(remaining_backups) > self.max_backups:
            for old_backup in remaining_backups[self.max_backups:]:
                try:
                    old_backup.unlink()
                    metadata_file = old_backup.with_suffix('.json')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    logger.info(f"Backup excedente deletado: {old_backup.name}")
                except Exception as e:
                    logger.warning(f"Erro ao deletar backup excedente: {str(e)}")


# Funções auxiliares para uso em FastAPI
def create_daily_backup():
    """Função para ser executada diariamente (ex: via cron ou scheduler)"""
    manager = BackupManager()
    success, msg = manager.create_backup(tag='daily')
    logger.info(f"Backup diário: {msg}")
    return success


def backup_endpoint_handler(request_body: dict = None) -> dict:
    """
    Handler para endpoint de backup manual
    
    Exemplo de uso em FastAPI:
        @router.post("/backup")
        async def manual_backup():
            return backup_endpoint_handler()
    """
    manager = BackupManager()
    
    # Criar backup
    success, msg = manager.create_backup(tag='manual')
    
    if success:
        return {
            'success': True,
            'message': msg,
            'backups': manager.list_backups()[:5]  # Últimos 5
        }
    else:
        return {
            'success': False,
            'message': msg,
            'error': True
        }


# Exemplo de integração com APScheduler
def schedule_daily_backups():
    """
    Agendar backups diários
    
    Adicionar ao main.py:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(schedule_daily_backups, 'cron', hour=3, minute=0)
        scheduler.start()
    """
    manager = BackupManager()
    success, msg = manager.create_backup(tag='scheduled')
    logger.info(f"Backup agendado executado: {msg} (Sucesso: {success})")


if __name__ == '__main__':
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Teste
    manager = BackupManager()
    
    # Criar backup
    success, msg = manager.create_backup(tag='test')
    print(f"Criar backup: {msg}")
    
    # Listar backups
    print("\nBackups disponíveis:")
    for backup in manager.list_backups():
        print(f"  - {backup['filename']} ({backup['size_mb']} MB)")
