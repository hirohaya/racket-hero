#!/usr/bin/env python
# migrate_create_tables.py - Script para criar tabelas no PostgreSQL

import os
import sys
from pathlib import Path

# Adicionar backend ao path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Importar database
from backend.database import engine, Base
from backend.models.usuario import Usuario
from backend.models.event import Event
from backend.models.player import Player
from backend.models.match import Match
from backend.models.evento_organizador import EventoOrganizador

def create_tables():
    """Criar todas as tabelas no banco de dados"""
    print("[INFO] Criando tabelas no banco de dados...")
    
    try:
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("[OK] Todas as tabelas foram criadas com sucesso!")
        
        # Verificar quais tabelas foram criadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"\n[INFO] Tabelas criadas ({len(tables)}):")
        for table in tables:
            print(f"  ✓ {table}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("[INFO] Script de migração - Criar tabelas")
    print(f"[INFO] DATABASE_URL: {os.getenv('DATABASE_URL', 'não definida')[:50]}...")
    print()
    
    success = create_tables()
    
    if success:
        print("\n[SUCCESS] Migração concluída!")
        sys.exit(0)
    else:
        print("\n[ERROR] Migração falhou!")
        sys.exit(1)
