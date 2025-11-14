#!/usr/bin/env python3
"""
seed_direct.py - Popula banco diretamente sem usar FastAPI
Solução alternativa para evitar problemas de dependências
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = "racket_hero.db"

def load_json_file(filename):
    """Carrega arquivo JSON da pasta tests/data"""
    data_path = Path(__file__).parent / "data" / filename
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clear_database():
    """Limpa tabelas existentes"""
    print("[INFO] Limpando banco de dados...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM match")
        cursor.execute("DELETE FROM player")
        cursor.execute("DELETE FROM event")
        conn.commit()
        conn.close()
        print("[OK] Banco limpado")
    except Exception as e:
        print(f"[WARNING] Erro ao limpar: {e}")

def seed_events():
    """Cria eventos"""
    print("[INFO] Criando eventos...")
    events_data = load_json_file("events.json")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for event_data in events_data:
        cursor.execute(
            "INSERT INTO event (name, date, time, active) VALUES (?, ?, ?, ?)",
            (event_data["name"], event_data["date"], event_data.get("time", "19:00"), 1 if event_data.get("active", True) else 0)
        )
    
    conn.commit()
    conn.close()
    print(f"[OK] {len(events_data)} eventos criados")

def seed_players():
    """Cria jogadores"""
    print("[INFO] Criando jogadores...")
    players_data = load_json_file("players.json")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for player_data in players_data:
        cursor.execute(
            "INSERT INTO player (event_id, name, initial_elo) VALUES (?, ?, ?)",
            (player_data["event_id"], player_data["name"], player_data.get("initial_elo", 1600))
        )
    
    conn.commit()
    conn.close()
    print(f"[OK] {len(players_data)} jogadores criados")

def seed_matches():
    """Cria partidas"""
    print("[INFO] Criando partidas...")
    matches_data = load_json_file("matches.json")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for match_data in matches_data:
        cursor.execute(
            "INSERT INTO match (event_id, player_1_id, player_2_id, winner_id) VALUES (?, ?, ?, ?)",
            (match_data["event_id"], match_data["player_1_id"], match_data["player_2_id"], match_data["winner_id"])
        )
    
    conn.commit()
    conn.close()
    print(f"[OK] {len(matches_data)} partidas criadas")

def verify_data():
    """Verifica dados inseridos"""
    print("[INFO] Verificando dados...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM event")
    event_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM player")
    player_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM match")
    match_count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"[OK] {event_count} eventos")
    print(f"[OK] {player_count} jogadores")
    print(f"[OK] {match_count} partidas")

def main():
    """Executa seeding completo"""
    print("=" * 60)
    print("SEED DO BANCO VIA SQL DIRETO")
    print("=" * 60)
    
    try:
        clear_database()
        seed_events()
        seed_players()
        seed_matches()
        verify_data()
        
        print("=" * 60)
        print("[OK] SEED CONCLUIDO COM SUCESSO!")
        print("=" * 60)
        print("\nProximos passos:")
        print("  1. Acesse http://localhost:3000")
        print("  2. Veja os eventos criados")
        print("  3. Verifique jogadores e rankings")
        return True
    except Exception as e:
        print(f"[ERROR] Erro durante seed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
