#!/usr/bin/env python3
# scripts/init_railway_db.py
# Script para inicializar banco de dados no Railway

import os
import sys
import logging
from pathlib import Path

# Adicionar o diretório backend ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from database import init_db, engine
from sqlalchemy import inspect

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("init_railway_db")

def check_database():
    """Verifica se o banco foi inicializado corretamente"""
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        log.info(f"✅ Banco de dados conectado com sucesso")
        log.info(f"   Tabelas encontradas: {tables if tables else 'nenhuma'}")
        
        if tables:
            log.info("✅ Banco de dados inicializado com todas as tabelas")
        else:
            log.warning("⚠️  Banco vazio - executando init_db()")
            init_db()
            
            # Verificar novamente
            tables = inspector.get_table_names()
            log.info(f"✅ Tabelas criadas: {tables}")
        
        return True
    except Exception as e:
        log.error(f"❌ Erro ao verificar banco de dados: {e}")
        return False

def main():
    """Função principal"""
    log.info("🚀 Iniciando Railway Database Setup")
    log.info(f"   Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    log.info(f"   Database URL: {os.getenv('DATABASE_URL', 'sqlite:///./racket_hero.db')}")
    
    try:
        # Inicializar banco de dados
        init_db()
        log.info("✅ init_db() executado com sucesso")
        
        # Verificar
        if check_database():
            log.info("✅ ✅ ✅ Railway Database Setup COMPLETO!")
            return 0
        else:
            log.error("❌ Falha no setup do banco de dados")
            return 1
            
    except Exception as e:
        log.error(f"❌ Erro durante setup: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
