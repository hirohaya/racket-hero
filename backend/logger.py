import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Criar diretório de logs se não existir
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configurar o logger
logger = logging.getLogger("racket-hero")
logger.setLevel(logging.DEBUG)

# Formato dos logs
log_format = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(log_format)

# Handler para arquivo (rotativo)
file_handler = logging.handlers.RotatingFileHandler(
    filename=LOG_DIR / "app.log",
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_format)

# Adicionar handlers ao logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_logger(name: str = "racket-hero") -> logging.Logger:
    """
    Retorna uma instância do logger
    
    Args:
        name: Nome do módulo/componente
    
    Returns:
        logging.Logger: Logger configurado
    
    Example:
        log = get_logger("users.service")
        log.info("Usuário criado", extra={"user_id": 123})
    """
    return logging.getLogger(name)


# Exemplos de uso:
if __name__ == "__main__":
    log = get_logger("main")
    log.debug("Mensagem de debug")
    log.info("Informação importante")
    log.warning("Aviso sobre algo")
    log.error("Erro ocorreu")
    log.critical("Erro crítico")
