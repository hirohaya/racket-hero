#!/usr/bin/env python3
import sqlite3
import os

db_path = r"C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\racket_hero.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM event")
events_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM player")
players_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM match")
matches_count = cursor.fetchone()[0]

print(f"[RAIZ] racket_hero.db")
print(f"  Eventos: {events_count}")
print(f"  Jogadores: {players_count}")
print(f"  Partidas: {matches_count}")

if events_count > 0:
    cursor.execute("SELECT id, name FROM event ORDER BY id DESC LIMIT 3")
    for row in cursor.fetchall():
        print(f"    - {row[1]}")

conn.close()
