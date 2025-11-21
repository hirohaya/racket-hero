#!/usr/bin/env python3
"""
Seed script para adicionar dados de teste ao Railway dev
Executado apenas UMA VEZ na primeira inicialização
Inclui: usuários de teste, eventos, e mapeamentos organizador-evento
"""

import sys
import os
from pathlib import Path
from datetime import datetime

backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from database import SessionLocal, engine, Base
from models import Usuario, Event, Player, EventoOrganizador

SEED_FLAG_FILE = Path(__file__).parent / ".seed_initialized"

def seed_dev_data():
    """Adiciona dados de teste ao banco de dados de dev"""
    
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("🌱 SEED DEV - Adicionando dados de teste")
        print("="*70)
        
        # ===== USUÁRIOS DE TESTE =====
        print("\n📋 Adicionando Organizadores...")
        
        organizadores = [
            {
                "nome": "Carlos Souza",
                "email": "carlos@example.com",
                "tipo": "organizador",
            },
            {
                "nome": "Fernanda Lima",
                "email": "fernanda@example.com",
                "tipo": "organizador",
            }
        ]
        
        org_id = None
        for org_data in organizadores:
            existing = session.query(Usuario).filter(Usuario.email == org_data["email"]).first()
            if not existing:
                org = Usuario(
                    nome=org_data["nome"],
                    email=org_data["email"],
                    senha_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",
                    tipo=org_data["tipo"],
                    ativo=True
                )
                session.add(org)
                session.commit()
                session.refresh(org)
                org_id = org.id
                print(f"  ✅ {org_data['nome']} (ID: {org.id})")
            else:
                org_id = existing.id
                print(f"  ⏭️  {org_data['nome']} (ID: {existing.id})")
        
        print("\n🎯 Adicionando 10 Jogadores...")
        
        jogadores = [
            ("João Silva", "joao.silva@example.com"),
            ("Maria Santos", "maria.santos@example.com"),
            ("Pedro Oliveira", "pedro.oliveira@example.com"),
            ("Ana Costa", "ana.costa@example.com"),
            ("Lucas Ferreira", "lucas.ferreira@example.com"),
            ("Patricia Alves", "patricia.alves@example.com"),
            ("Roberto Gomes", "roberto.gomes@example.com"),
            ("Juliana Rocha", "juliana.rocha@example.com"),
            ("Bruno Martins", "bruno.martins@example.com"),
            ("Camila Ribeiro", "camila.ribeiro@example.com"),
        ]
        
        jogador_ids = []
        for nome, email in jogadores:
            existing = session.query(Usuario).filter(Usuario.email == email).first()
            if not existing:
                jog = Usuario(
                    nome=nome,
                    email=email,
                    senha_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5YmMxSUmGEJiq",
                    tipo="jogador",
                    ativo=True
                )
                session.add(jog)
                session.commit()
                session.refresh(jog)
                jogador_ids.append(jog.id)
                print(f"  ✅ {nome} (ID: {jog.id})")
            else:
                jogador_ids.append(existing.id)
                print(f"  ⏭️  {nome} (ID: {existing.id})")
        
        # ===== CRIAR EVENTO DE TESTE =====
        print("\n📅 Criando Evento de Teste...")
        
        event_exists = session.query(Event).filter(Event.name == "Torneio Teste").first()
        event_id = None
        
        if not event_exists:
            event = Event(
                name="Torneio Teste",
                date="2025-12-01",
                time="14:00",
                active=True
            )
            session.add(event)
            session.commit()
            session.refresh(event)
            event_id = event.id
            print(f"  ✅ Evento criado: Torneio Teste (ID: {event_id})")
        else:
            event_id = event_exists.id
            print(f"  ⏭️  Evento já existe: Torneio Teste (ID: {event_id})")
        
        # ===== MAPEAR ORGANIZADOR AO EVENTO =====
        print("\n🔐 Mapeando Organizador ao Evento...")
        
        if org_id and event_id:
            existing_map = session.query(EventoOrganizador).filter(
                EventoOrganizador.event_id == event_id,
                EventoOrganizador.usuario_id == org_id
            ).first()
            
            if not existing_map:
                org_map = EventoOrganizador(
                    event_id=event_id,
                    usuario_id=org_id,
                    é_criador=1
                )
                session.add(org_map)
                session.commit()
                print(f"  ✅ Organizador ID {org_id} mapeado ao Evento ID {event_id}")
            else:
                print(f"  ⏭️  Mapeamento já existe")
        
        # ===== ADICIONAR JOGADORES AO EVENTO =====
        print("\n⚽ Adicionando Jogadores ao Evento...")
        
        for jog_id, (nome, email) in zip(jogador_ids, jogadores):
            existing_player = session.query(Player).filter(
                Player.event_id == event_id,
                Player.usuario_id == jog_id
            ).first()
            
            if not existing_player and jog_id:
                player = Player(
                    event_id=event_id,
                    usuario_id=jog_id,
                    name=nome,
                    initial_elo=1600.0
                )
                session.add(player)
                session.commit()
                print(f"  ✅ {nome} adicionado como Player")
            else:
                print(f"  ⏭️  {nome} já é Player do evento")
        
        # ===== RELATÓRIO FINAL =====
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL")
        print("="*70)
        
        total_users = session.query(Usuario).count()
        total_orgs = session.query(Usuario).filter(Usuario.tipo == "organizador").count()
        total_jogs = session.query(Usuario).filter(Usuario.tipo == "jogador").count()
        total_events = session.query(Event).count()
        total_players = session.query(Player).count()
        total_org_maps = session.query(EventoOrganizador).count()
        
        print(f"\n  👥 Usuários: {total_users} ({total_orgs} org + {total_jogs} jog)")
        print(f"  📅 Eventos: {total_events}")
        print(f"  ⚽ Players: {total_players}")
        print(f"  🔐 Organizador-Evento Maps: {total_org_maps}")
        print("\n✅ Seed completado com sucesso!")
        print("="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro no seed: {str(e)}")
        import traceback
        traceback.print_exc()
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    # Verificar se seed já foi executado
    if SEED_FLAG_FILE.exists():
        print("\n" + "="*70)
        print("⏭️  Seed já foi executado anteriormente. Pulando...")
        print("="*70 + "\n")
        sys.exit(0)
    
    # Executar seed
    if seed_dev_data():
        # Criar arquivo de flag para não executar seed novamente
        SEED_FLAG_FILE.touch()
        print("\n✅ Flag criada: seed não será executado novamente neste container")
    else:
        print("\n❌ Seed falhou")
        sys.exit(1)
