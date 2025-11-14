#!/usr/bin/env python3
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'pingchampions.db')
print(f"[INFO] Verificando banco em: {db_path}")
print(f"[INFO] Banco existe: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    print(f"[INFO] Tabelas no banco: {tables}")
    conn.close()
