#!/usr/bin/env python3
import sqlite3
import sys
sys.path.insert(0, r"C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend")

from utils.security import verify_password, hash_password

db_path = r"C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend\racket_hero.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Pegar usuarios
cursor.execute("SELECT id, email, nome, senha_hash FROM usuarios")
for row in cursor.fetchall():
    user_id, email, nome, senha_hash = row
    print(f"\n[Usuário] {nome} ({email})")
    print(f"  Hash: {senha_hash[:50]}...")
    
    # Tentar verificar com a senha de teste
    test_password = "Senha123!"
    try:
        is_valid = verify_password(test_password, senha_hash)
        print(f"  Senha '{test_password}' válida: {is_valid}")
    except Exception as e:
        print(f"  Erro ao verificar senha: {e}")

conn.close()
