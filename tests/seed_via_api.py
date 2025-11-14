#!/usr/bin/env python3
"""
seed_via_api.py - Popula banco através de chamadas HTTP à API
Alternativa para evitar problemas de import direto
"""

import json
import requests
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

def load_json_file(filename):
    """Carrega arquivo JSON da pasta tests/data"""
    data_path = Path(__file__).parent / "data" / filename
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clear_database():
    """Limpa dados criados anteriormente (opcional)"""
    print("[INFO] Banco será limpo pela próxima execução da seed...")

def seed_events():
    """Cria eventos via API"""
    print("[INFO] Criando eventos...")
    events_data = load_json_file("events.json")
    created_events = {}
    
    for idx, event_data in enumerate(events_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/events",
                json=event_data,
                timeout=5
            )
            if response.status_code == 200:
                event = response.json()
                created_events[event_data["name"]] = event["id"]
                print(f"  [OK] Evento {idx}: {event_data['name']} (ID: {event['id']})")
            else:
                print(f"  [ERROR] Falha ao criar evento: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] Erro ao criar evento: {e}")
    
    return created_events

def seed_players():
    """Cria jogadores via API"""
    print("[INFO] Criando jogadores...")
    players_data = load_json_file("players.json")
    created_players = {}
    
    for idx, player_data in enumerate(players_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/players",
                json=player_data,
                timeout=5
            )
            if response.status_code == 200:
                player = response.json()
                key = f"{player_data['name']}_e{player_data['event_id']}"
                created_players[key] = player["id"]
                print(f"  [OK] Jogador {idx}: {player_data['name']} (ID: {player['id']})")
            else:
                print(f"  [ERROR] Falha ao criar jogador: {response.status_code}")
        except Exception as e:
            print(f"  [ERROR] Erro ao criar jogador: {e}")
    
    return created_players

def seed_matches():
    """Cria partidas via API"""
    print("[INFO] Criando partidas...")
    matches_data = load_json_file("matches.json")
    created_matches = {}
    
    for idx, match_data in enumerate(matches_data, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/matches",
                json=match_data,
                timeout=5
            )
            if response.status_code == 200:
                match = response.json()
                created_matches[f"match_{idx}"] = match["id"]
                p1 = match_data["player_1_id"]
                p2 = match_data["player_2_id"]
                winner = "P1" if match_data["winner_id"] == p1 else "P2"
                print(f"  [OK] Partida {idx}: J{p1} vs J{p2} - Vencedor: {winner}")
            else:
                print(f"  [ERROR] Falha ao criar partida: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"  [ERROR] Erro ao criar partida: {e}")
    
    return created_matches

def verify_data():
    """Verifica dados inseridos via API"""
    print("[INFO] Verificando dados inseridos...")
    try:
        # Check events
        response = requests.get(f"{BASE_URL}/events", timeout=5)
        if response.status_code == 200:
            events = response.json()
            print(f"  [OK] {len(events)} eventos")
        
        # Check first event's players
        if events:
            event_id = events[0]["id"]
            response = requests.get(f"{BASE_URL}/players/{event_id}", timeout=5)
            if response.status_code == 200:
                players = response.json()
                print(f"  [OK] {len(players)} jogadores no primeiro evento")
        
        print("[OK] Dados verificados com sucesso!")
        return True
    except Exception as e:
        print(f"  [ERROR] Erro ao verificar dados: {e}")
        return False

def check_api_ready():
    """Verifica se a API está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/events", timeout=2)
        return response.status_code < 500
    except:
        return False

def main():
    """Executa o seeding completo"""
    print("=" * 60)
    print("SEED DO BANCO DE DADOS VIA API")
    print("=" * 60)
    
    # Verificar se API está rodando
    print("[INFO] Verificando se API está disponível...")
    if not check_api_ready():
        print("[ERROR] API nao encontrada em http://localhost:8000")
        print("[INFO] Execute os servidores com: ./scripts/start-all-new.ps1")
        return False
    
    print("[OK] API disponivel!")
    
    # Popular dados
    try:
        seed_events()
        time.sleep(1)
        
        seed_players()
        time.sleep(1)
        
        seed_matches()
        time.sleep(1)
        
        # Verificar
        if verify_data():
            print("=" * 60)
            print("[OK] SEED CONCLUIDO COM SUCESSO!")
            print("=" * 60)
            print("\nProximos passos:")
            print("  1. Acesse http://localhost:3000")
            print("  2. Veja os dados nos eventos, jogadores e rankings")
            print("  3. Teste criar novas partidas")
            return True
    except Exception as e:
        print(f"[ERROR] Erro durante seed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
