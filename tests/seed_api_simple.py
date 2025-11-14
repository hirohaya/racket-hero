#!/usr/bin/env python3
"""
Script para semear dados de teste via API REST.
Usa requests library para fazer chamadas HTTP ao backend.
"""

import json
import requests
import time

BASE_URL = "http://localhost:8000"

def load_test_data(filename):
    """Carrega dados de teste do arquivo JSON."""
    with open(f"tests/data/{filename}", "r", encoding="utf-8") as f:
        return json.load(f)

def seed_events():
    """Semeia eventos no banco."""
    print("[*] Seando eventos...")
    events = load_test_data("events.json")
    
    event_ids = {}
    for event in events:
        response = requests.post(
            f"{BASE_URL}/events",
            json=event,
            timeout=5
        )
        if response.status_code == 200:
            created = response.json()
            event_ids[event["name"]] = created["id"]
            print(f"  [✓] Evento criado: {event['name']} (ID: {created['id']})")
        else:
            print(f"  [✗] Erro ao criar evento '{event['name']}': {response.status_code}")
            print(f"      Response: {response.text}")
    
    return event_ids

def seed_players(event_ids):
    """Semeia jogadores para cada evento."""
    print("[*] Seando jogadores...")
    players = load_test_data("players.json")
    
    player_ids = {}
    for player in players:
        event_name = next((e for e in load_test_data("events.json") if e["id"] == player["event_id"]), None)
        event_id = event_ids.get(event_name["name"]) if event_name else None
        
        if not event_id:
            print(f"  [✗] Evento não encontrado para jogador {player['name']}")
            continue
        
        player_data = {
            "event_id": event_id,
            "name": player["name"],
            "initial_elo": player.get("initial_elo", 1600)
        }
        
        response = requests.post(
            f"{BASE_URL}/players",
            json=player_data,
            timeout=5
        )
        if response.status_code == 200:
            created = response.json()
            player_ids[player["name"]] = created["id"]
            print(f"  [✓] Jogador criado: {player['name']} (ID: {created['id']})")
        else:
            print(f"  [✗] Erro ao criar jogador '{player['name']}': {response.status_code}")
            print(f"      Response: {response.text}")
    
    return player_ids

def seed_matches(player_ids, event_ids):
    """Semeia partidas e calcula Elo."""
    print("[*] Seando partidas e calculando Elo...")
    matches = load_test_data("matches.json")
    events = load_test_data("events.json")
    
    for match in matches:
        event_id = event_ids.get(next((e["name"] for e in events if e["id"] == match["event_id"]), None))
        p1_id = player_ids.get(next((p["name"] for p in load_test_data("players.json") if p["id"] == match["player_1_id"]), None))
        p2_id = player_ids.get(next((p["name"] for p in load_test_data("players.json") if p["id"] == match["player_2_id"]), None))
        winner_id = player_ids.get(next((p["name"] for p in load_test_data("players.json") if p["id"] == match["winner_id"]), None))
        
        if not (event_id and p1_id and p2_id and winner_id):
            print(f"  [✗] IDs não encontrados para partida {match.get('id')}")
            continue
        
        match_data = {
            "event_id": event_id,
            "player_1_id": p1_id,
            "player_2_id": p2_id,
            "winner_id": winner_id
        }
        
        response = requests.post(
            f"{BASE_URL}/matches",
            json=match_data,
            timeout=5
        )
        if response.status_code == 200:
            created = response.json()
            print(f"  [✓] Partida criada: {created['id']} (Vencedor: {winner_id})")
        else:
            print(f"  [✗] Erro ao criar partida: {response.status_code}")
            print(f"      Response: {response.text}")

def main():
    """Função principal."""
    print("=" * 60)
    print("SEED DO BANCO VIA API REST")
    print("=" * 60)
    
    # Tentar conectar ao backend
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("[✓] Backend respondendo em " + BASE_URL)
        else:
            print(f"[✗] Backend retornou status {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"[✗] Não foi possível conectar ao backend em {BASE_URL}")
        print("[INFO] Certifique-se que o backend está rodando")
        return
    
    # Semear dados
    event_ids = seed_events()
    player_ids = seed_players(event_ids)
    seed_matches(player_ids, event_ids)
    
    print("\n" + "=" * 60)
    print("[OK] Seeding concluído!")
    print("=" * 60)

if __name__ == "__main__":
    main()
