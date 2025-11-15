#!/usr/bin/env python3
import sqlite3

db_path = r"C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend\racket_hero.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM usuarios")
count = cursor.fetchone()[0]
print(f"[DB] Total de usuários: {count}")

cursor.execute("SELECT id, email, nome FROM usuarios LIMIT 10")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} ({row[2]})")

conn.close()
