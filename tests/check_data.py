#!/usr/bin/env python3
import sqlite3
import sys

db_path = r"C:\Users\hiros\OneDrive\Documents\projetos\racket-hero\backend\racket_hero.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Contar registros
cursor.execute("SELECT COUNT(*) FROM event")
events_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM player")
players_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM match")
matches_count = cursor.fetchone()[0]

print(f"[DB STATUS]")
print(f"  Eventos: {events_count}")
print(f"  Jogadores: {players_count}")
print(f"  Partidas: {matches_count}")

if events_count > 0:
    cursor.execute("SELECT id, name, date FROM event ORDER BY id")
    for row in cursor.fetchall():
        print(f"    - Evento {row[0]}: {row[1]} ({row[2]})")

conn.close()
