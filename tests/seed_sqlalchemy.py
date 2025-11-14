#!/usr/bin/env python3
"""Script para semear dados de teste diretamente no banco com SQLAlchemy."""

import json
import os
import sys

# Adicionar backend ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import SessionLocal, init_db
from models.event import Event
from models.player import Player
from models.match import Match

def load_test_data(filename):
    """Carrega dados de teste do arquivo JSON."""
    filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def seed_events(db):
    """Semeia eventos no banco."""
    print("[*] Seando eventos...")
    events_data = load_test_data('events.json')
    
    event_map = {}
    for event_data in events_data:
        event = Event(
            name=event_data['name'],
            date=event_data['date'],
            time=event_data.get('time', '19:00'),
            active=event_data.get('active', True)
        )
        db.add(event)
        db.flush()
        event_map[event_data['name']] = event.id
        print(f"  [OK] {event.name} (ID: {event.id})")
    
    db.commit()
    return event_map

def seed_players(db, event_map):
    """Semeia jogadores para cada evento."""
    print("[*] Seando jogadores...")
    events_data = load_test_data('events.json')
    players_data = load_test_data('players.json')
    
    event_index_to_id = {}
    for i, orig_event in enumerate(events_data, start=1):
        event_index_to_id[i] = event_map.get(orig_event['name'])
    
    player_map = {}
    for i, player_data in enumerate(players_data, start=1):
        new_event_id = event_index_to_id.get(player_data['event_id'])
        if not new_event_id:
            print(f"  [!] Evento não encontrado para {player_data['name']}")
            continue
        
        player = Player(
            event_id=new_event_id,
            name=player_data['name'],
            initial_elo=player_data.get('initial_elo', 1600.0)
        )
        db.add(player)
        db.flush()
        player_map[i] = player.id
        print(f"  [OK] {player.name} (ID: {player.id}, Elo: {player.initial_elo})")
    
    db.commit()
    return player_map

def seed_matches(db, event_map, player_map):
    """Semeia partidas e calcula Elo."""
    print("[*] Seando partidas com Elo...")
    events_data = load_test_data('events.json')
    matches_data = load_test_data('matches.json')
    
    event_index_to_id = {}
    for i, orig_event in enumerate(events_data, start=1):
        event_index_to_id[i] = event_map.get(orig_event['name'])
    
    K_FACTOR = 32
    
    for match_data in matches_data:
        new_event_id = event_index_to_id.get(match_data['event_id'])
        new_p1_id = player_map.get(match_data['player_1_id'])
        new_p2_id = player_map.get(match_data['player_2_id'])
        new_winner_id = player_map.get(match_data['winner_id'])
        
        if not all([new_event_id, new_p1_id, new_p2_id, new_winner_id]):
            print(f"  [!] IDs incompletos para partida")
            continue
        
        match = Match(
            event_id=new_event_id,
            player_1_id=new_p1_id,
            player_2_id=new_p2_id,
            winner_id=new_winner_id
        )
        db.add(match)
        db.flush()
        
        player_1 = db.query(Player).get(new_p1_id)
        player_2 = db.query(Player).get(new_p2_id)
        
        is_p1_winner = new_winner_id == new_p1_id
        winner_elo = player_1.initial_elo if is_p1_winner else player_2.initial_elo
        loser_elo = player_2.initial_elo if is_p1_winner else player_1.initial_elo
        
        expected_winner = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
        elo_change = K_FACTOR * (1 - expected_winner)
        
        if is_p1_winner:
            player_1.initial_elo += elo_change
            player_2.initial_elo -= elo_change
            winner_name = player_1.name
        else:
            player_1.initial_elo -= elo_change
            player_2.initial_elo += elo_change
            winner_name = player_2.name
        
        print(f"  [OK] Partida {match.id}: {player_1.name} vs {player_2.name} | Vencedor: {winner_name}")
    
    db.commit()

def main():
    """Função principal."""
    print("=" * 70)
    print("SEED DO BANCO")
    print("=" * 70)
    
    print("[*] Inicializando banco de dados...")
    init_db()
    print("[OK] Banco inicializado\n")
    
    db = SessionLocal()
    
    try:
        event_map = seed_events(db)
        player_map = seed_players(db, event_map)
        seed_matches(db, event_map, player_map)
        
        print("\n" + "=" * 70)
        print("[OK] SEEDING CONCLUIDO COM SUCESSO!")
        print(f"[INFO] {len(event_map)} eventos criados")
        print(f"[INFO] {len(player_map)} jogadores criados")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
