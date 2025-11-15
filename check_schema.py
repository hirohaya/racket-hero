#!/usr/bin/env python3
import sqlite3

db_path = r"C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend\racket_hero.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Listar tabelas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tabelas:")
for table in tables:
    print(f"  - {table[0]}")

# Verificar estrutura de usuarios
print("\nEstrutura da tabela 'usuarios':")
cursor.execute("PRAGMA table_info(usuarios)")
for col in cursor.fetchall():
    print(f"  {col[1]}: {col[2]}")

conn.close()
