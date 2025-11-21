#!/usr/bin/env python3
"""
Script de diagnóstico para verificar dados no banco de dados
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório backend ao path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from database import SessionLocal
from models import Usuario, Event, Player, EventoOrganizador

def diagnose():
    """Diagnostica o estado do banco de dados"""
    session = SessionLocal()
    
    try:
        print("\n" + "="*70)
        print("📊 DIAGNÓSTICO DO BANCO DE DADOS")
        print("="*70)
        
        # ===== USUÁRIOS =====
        print("\n👥 USUÁRIOS CADASTRADOS:")
        print("-" * 70)
        usuarios = session.query(Usuario).all()
        for u in usuarios:
            print(f"  ID: {u.id:3d} | Nome: {u.nome:30s} | Email: {u.email:30s} | Tipo: {u.tipo:12s}")
        print(f"Total: {len(usuarios)} usuários")
        
        # ===== EVENTOS =====
        print("\n📅 EVENTOS CADASTRADOS:")
        print("-" * 70)
        events = session.query(Event).all()
        for e in events:
            print(f"  ID: {e.id:3d} | Nome: {e.name:40s} | Data: {e.date:15s} | Ativo: {e.active}")
        print(f"Total: {len(events)} eventos")
        
        # ===== JOGADORES =====
        print("\n⚽ JOGADORES CADASTRADOS:")
        print("-" * 70)
        players = session.query(Player).all()
        for p in players:
            usuario_ref = f"(Usuario ID: {p.usuario_id})" if p.usuario_id else "(Manual)"
            print(f"  ID: {p.id:3d} | Evento: {p.event_id:3d} | Nome: {p.name:30s} | Elo: {p.initial_elo:7.1f} {usuario_ref}")
        print(f"Total: {len(players)} jogadores")
        
        # ===== ORGANIZADORES POR EVENTO =====
        print("\n🔐 ORGANIZADORES POR EVENTO:")
        print("-" * 70)
        org_mappings = session.query(EventoOrganizador).all()
        for om in org_mappings:
            event = session.query(Event).filter(Event.id == om.event_id).first()
            usuario = session.query(Usuario).filter(Usuario.id == om.usuario_id).first()
            event_name = event.name if event else "EVENTO NÃO ENCONTRADO"
            user_name = usuario.nome if usuario else "USUÁRIO NÃO ENCONTRADO"
            print(f"  Evento ID: {om.event_id:3d} ({event_name:40s}) | Organizador ID: {om.usuario_id:3d} ({user_name})")
        print(f"Total: {len(org_mappings)} mapeamentos")
        
        # ===== ANÁLISE DE PROBLEMAS =====
        print("\n⚠️  ANÁLISE DE PROBLEMAS:")
        print("-" * 70)
        
        # Verificar se há eventos sem organizador
        events_without_org = []
        for e in events:
            org_count = session.query(EventoOrganizador).filter(EventoOrganizador.event_id == e.id).count()
            if org_count == 0:
                events_without_org.append(e)
        
        if events_without_org:
            print(f"  ⚠️  {len(events_without_org)} evento(s) SEM organizador atribuído:")
            for e in events_without_org:
                print(f"      - '{e.name}' (ID: {e.id})")
        else:
            print("  ✅ Todos os eventos têm organizadores atribuídos")
        
        # Verificar se há jogadores orfãos (usuario_id inválido)
        orphan_players = []
        for p in players:
            if p.usuario_id:
                user = session.query(Usuario).filter(Usuario.id == p.usuario_id).first()
                if not user:
                    orphan_players.append(p)
        
        if orphan_players:
            print(f"  ⚠️  {len(orphan_players)} jogador(es) com usuario_id inválido")
        else:
            print("  ✅ Todos os jogadores têm usuario_id válido ou nenhum usuario_id")
        
        # Verificar se há jogadores duplicados em um evento
        from sqlalchemy import func
        duplicates = session.query(
            Player.event_id,
            Player.name,
            func.count('*').label('count')
        ).group_by(Player.event_id, Player.name).having(func.count('*') > 1).all()
        
        if duplicates:
            print(f"  ⚠️  {len(duplicates)} nome(s) de jogador(es) duplicado(s) no mesmo evento:")
            for d in duplicates:
                print(f"      - Evento {d.event_id}: '{d.name}' ({d.count}x)")
        else:
            print("  ✅ Sem jogadores duplicados em eventos")
        
        print("\n" + "="*70)
        
    except Exception as e:
        print(f"\n❌ Erro ao diagnosticar: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    diagnose()
