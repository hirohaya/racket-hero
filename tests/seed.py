#!/usr/bin/env python3
"""
seed.py - Script para popular o banco de dados com massa de testes
Cria eventos, jogadores e partidas para testes
"""

import json
import sys
import os
from pathlib import Path

# Rodar do diretório backend
backend_path = Path(__file__).parent.parent / "backend"
os.chdir(backend_path)
sys.path.insert(0, str(backend_path))

from database import SessionLocal, engine, Base
from models import Event, Player, Match
from logger import get_logger

log = get_logger("seed")

def load_json_file(filename):
    """Carrega arquivo JSON da pasta data"""
    data_path = Path(__file__).parent / "data" / filename
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clear_database():
    """Limpa todas as tabelas do banco"""
    log.info("Limpando banco de dados...")
    session = SessionLocal()
    try:
        session.query(Match).delete()
        session.query(Player).delete()
        session.query(Event).delete()
        session.commit()
        log.info("Banco limpado com sucesso")
    except Exception as e:
        log.error(f"Erro ao limpar banco: {e}")
        session.rollback()
    finally:
        session.close()

def seed_events():
    """Cria eventos de teste"""
    log.info("Criando eventos...")
    session = SessionLocal()
    try:
        events_data = load_json_file("events.json")
        
        for event_data in events_data:
            event = Event(
                name=event_data["name"],
                date=event_data["date"],
                time=event_data["time"],
                active=event_data["active"]
            )
            session.add(event)
        
        session.commit()
        log.info(f"{len(events_data)} eventos criados com sucesso")
        return True
    except Exception as e:
        log.error(f"Erro ao criar eventos: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def seed_players():
    """Cria jogadores de teste"""
    log.info("Criando jogadores...")
    session = SessionLocal()
    try:
        players_data = load_json_file("players.json")
        
        for player_data in players_data:
            player = Player(
                event_id=player_data["event_id"],
                name=player_data["name"],
                initial_elo=player_data["initial_elo"]
            )
            session.add(player)
        
        session.commit()
        log.info(f"{len(players_data)} jogadores criados com sucesso")
        return True
    except Exception as e:
        log.error(f"Erro ao criar jogadores: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def seed_matches():
    """Cria partidas de teste"""
    log.info("Criando partidas...")
    session = SessionLocal()
    try:
        matches_data = load_json_file("matches.json")
        
        for match_data in matches_data:
            match = Match(
                event_id=match_data["event_id"],
                player_1_id=match_data["player_1_id"],
                player_2_id=match_data["player_2_id"],
                winner_id=match_data["winner_id"]
            )
            session.add(match)
        
        session.commit()
        log.info(f"{len(matches_data)} partidas criadas com sucesso")
        return True
    except Exception as e:
        log.error(f"Erro ao criar partidas: {e}")
        session.rollback()
        return False
    finally:
        session.close()

def verify_data():
    """Verifica dados inseridos"""
    log.info("Verificando dados inseridos...")
    session = SessionLocal()
    try:
        event_count = session.query(Event).count()
        player_count = session.query(Player).count()
        match_count = session.query(Match).count()
        
        log.info(f"[OK] {event_count} eventos")
        log.info(f"[OK] {player_count} jogadores")
        log.info(f"[OK] {match_count} partidas")
        
        return True
    except Exception as e:
        log.error(f"Erro ao verificar dados: {e}")
        return False
    finally:
        session.close()

def main():
    """Executa o seeding completo"""
    log.info("=" * 60)
    log.info("INICIANDO SEED DO BANCO DE DADOS")
    log.info("=" * 60)
    
    # Limpar banco
    clear_database()
    
    # Popular dados
    success = True
    success = seed_events() and success
    success = seed_players() and success
    success = seed_matches() and success
    
    # Verificar
    if success:
        verify_data()
        log.info("=" * 60)
        log.info("[OK] SEED CONCLUIDO COM SUCESSO!")
        log.info("=" * 60)
    else:
        log.error("[ERROR] Erro durante seed do banco")
        sys.exit(1)

if __name__ == "__main__":
    main()
