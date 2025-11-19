"""
Logging configurado para produção - Racket Hero
Implementa logging centralizado com níveis DEBUG, INFO, WARNING, ERROR
"""

import logging
import logging.handlers
import os
from datetime import datetime, timezone
import json
from pathlib import Path


class JSONFormatter(logging.Formatter):
    """Formatter que converte logs em JSON para facilitar parsing"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Adicionar exceção se houver
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(
    log_level=logging.INFO,
    log_dir='logs',
    console_output=True,
    file_output=True,
    json_format=True
):
    """
    Configurar logging para produção
    
    Args:
        log_level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Diretório para arquivos de log
        console_output: Se True, saída para console
        file_output: Se True, saída para arquivo
        json_format: Se True, formatar logs como JSON
    
    Returns:
        logger: Logger configurado
    """
    
    # Criar diretório de logs se não existir
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Criar logger principal
    logger = logging.getLogger('racket_hero')
    logger.setLevel(log_level)
    
    # Remover handlers existentes (evitar duplicação)
    logger.handlers.clear()
    
    # Formatter
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    # Handler para console
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Handler para arquivo (rotação diária)
    if file_output:
        # Arquivo geral
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_path / 'app.log',
            maxBytes=10485760,  # 10 MB
            backupCount=10,  # Manter 10 backups
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Arquivo de erros
        error_handler = logging.FileHandler(
            filename=log_path / 'errors.log',
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)
        
        # Arquivo de acesso (APIs)
        access_handler = logging.FileHandler(
            filename=log_path / 'access.log',
            encoding='utf-8'
        )
        access_handler.setLevel(logging.INFO)
        access_handler.setFormatter(formatter)
        api_logger = logging.getLogger('racket_hero.api')
        api_logger.addHandler(access_handler)
    
    return logger


# Logger global
log = setup_logging(
    log_level=logging.DEBUG if os.getenv('DEBUG', 'False') == 'True' else logging.INFO,
    log_dir=os.getenv('LOG_DIR', 'logs'),
    console_output=True,
    file_output=True,
    json_format=True
)


# Loggers específicos
def get_logger(name):
    """Obter logger específico por módulo"""
    return logging.getLogger(f'racket_hero.{name}')


# Exemplo de uso em routers
class LoggingMiddleware:
    """Middleware para logar requisições e respostas"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        
        api_logger = get_logger('api')
        
        # Informações da requisição
        method = scope['method']
        path = scope['path']
        client_ip = scope.get('client', ('unknown', 0))[0]
        
        api_logger.info(f"Incoming request: {method} {path} from {client_ip}")
        
        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                status = message['status']
                api_logger.info(f"Response: {status} for {method} {path}")
            await send(message)
        
        await self.app(scope, receive, send_wrapper)


# Exemplo de logs em diferentes níveis
def example_logging():
    """Exemplo de como usar logging em diferentes níveis"""
    logger = get_logger('example')
    
    try:
        logger.debug("Esta é uma mensagem de DEBUG")
        logger.info("Esta é uma mensagem de INFO")
        logger.warning("Esta é uma mensagem de WARNING")
        logger.error("Esta é uma mensagem de ERROR")
        
        # Simular erro
        x = 1 / 0
    except Exception as e:
        logger.exception("Ocorreu uma exceção")


if __name__ == '__main__':
    example_logging()
