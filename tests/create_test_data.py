#!/usr/bin/env python3
"""
create_test_data.py - Cria dados de teste (eventos, jogadores, organizadores)

Este script popula o banco de dados com:
- 5 eventos de teste
- 15 jogadores para os eventos  
- 2 contas de organizadores (além do admin e jogador já existentes)
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adiciona backend ao path para importar modelos
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from database import Base, SessionLocal, init_db
from models.event import Event
from models.player import Player
from models.usuario import Usuario, TipoUsuario
from utils.security import hash_password

# Inicializa banco de dados (cria tabelas se não existirem)
init_db()


def print_header(title):
    """Imprime header formatado"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def clear_test_data():
    """Limpa apenas eventos e jogadores (mantém usuários)"""
    print("[INFO] Limpando eventos e jogadores existentes...")
    db = SessionLocal()
    try:
        # Delete em ordem de dependência
        db.query(Player).delete()
        db.query(Event).delete()
        db.commit()
        print("[OK] Dados de teste removidos")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Erro ao limpar: {e}")
    finally:
        db.close()


def create_organizadores():
    """Cria contas de organizadores para teste"""
    print("\n[INFO] Verificando/criando organizadores...")
    db = SessionLocal()
    
    organizadores = [
        {
            "email": "joao@eventos.com",
            "nome": "João Silva",
            "senha": "Senha123!",
            "tipo": TipoUsuario.ORGANIZADOR,
            "descricao": "Organizador de Campeonatos"
        },
        {
            "email": "maria@eventos.com",
            "nome": "Maria Santos",
            "senha": "Senha123!",
            "tipo": TipoUsuario.ORGANIZADOR,
            "descricao": "Organizadora de Torneios"
        }
    ]
    
    created_count = 0
    for org_data in organizadores:
        existing = db.query(Usuario).filter(Usuario.email == org_data["email"]).first()
        
        if not existing:
            # Cria novo usuário organizador
            usuario = Usuario(
                email=org_data["email"],
                nome=org_data["nome"],
                senha_hash=hash_password(org_data["senha"]),
                tipo=org_data["tipo"]
            )
            db.add(usuario)
            created_count += 1
            print(f"  ✓ {org_data['nome']} ({org_data['tipo'].value})")
        else:
            print(f"  ⊘ {org_data['nome']} já existe")
    
    db.commit()
    db.close()
    
    if created_count > 0:
        print(f"[OK] {created_count} organizador(es) criado(s)")
    return created_count


def create_events():
    """Cria eventos de teste"""
    print("\n[INFO] Criando eventos...")
    db = SessionLocal()
    
    base_date = datetime.now()
    
    events_data = [
        {
            "name": "Campeonato Regional 2025",
            "date": (base_date + timedelta(days=5)).strftime("%Y-%m-%d"),
            "time": "19:00",
            "active": True
        },
        {
            "name": "Torneio Local - Novembro",
            "date": (base_date + timedelta(days=3)).strftime("%Y-%m-%d"),
            "time": "18:30",
            "active": True
        },
        {
            "name": "Casual Friday Night",
            "date": (base_date + timedelta(days=1)).strftime("%Y-%m-%d"),
            "time": "20:00",
            "active": True
        },
        {
            "name": "Campeonato Nacional - Fase Estadual",
            "date": (base_date + timedelta(days=10)).strftime("%Y-%m-%d"),
            "time": "17:00",
            "active": True
        },
        {
            "name": "Treino Semanal",
            "date": base_date.strftime("%Y-%m-%d"),
            "time": "18:00",
            "active": True
        }
    ]
    
    created_events = []
    for event_data in events_data:
        event = Event(
            name=event_data["name"],
            date=event_data["date"],
            time=event_data["time"],
            active=event_data["active"]
        )
        db.add(event)
        db.flush()  # Para obter o ID
        created_events.append(event)
        print(f"  ✓ {event_data['name']} ({event_data['date']} às {event_data['time']})")
    
    db.commit()
    db.close()
    
    print(f"[OK] {len(created_events)} evento(s) criado(s)")
    return created_events


def create_players():
    """Cria jogadores para os eventos"""
    print("\n[INFO] Criando jogadores...")
    db = SessionLocal()
    
    # Recupera eventos
    events = db.query(Event).all()
    
    if not events:
        print("[WARNING] Nenhum evento encontrado. Crie eventos primeiro!")
        db.close()
        return
    
    # Lista de jogadores com ranking inicial
    players_list = [
        ("Pedro Costa", 1800),
        ("Ana Silva", 1750),
        ("Carlos Mendes", 1700),
        ("Lucia Santos", 1850),
        ("Roberto Alves", 1650),
        ("Fernanda Lima", 1900),
        ("Gustavo Rocha", 1720),
        ("Patricia Gomes", 1780),
        ("Felipe Martins", 1680),
        ("Beatriz Oliveira", 1820),
        ("Marcus Vinicius", 1750),
        ("Jennifer Sousa", 1950),
        ("Thiago Costa", 1700),
        ("Mariana Santos", 1800),
        ("Lucas Pereira", 1730)
    ]
    
    total_created = 0
    
    # Distribui jogadores entre eventos
    players_per_event = len(players_list) // len(events)
    
    for idx, event in enumerate(events):
        start_idx = idx * players_per_event
        end_idx = start_idx + players_per_event
        if idx == len(events) - 1:  # Último evento pega os restantes
            end_idx = len(players_list)
        
        event_players = players_list[start_idx:end_idx]
        
        print(f"\n  {event.name}:")
        
        for player_name, initial_elo in event_players:
            player = Player(
                event_id=event.id,
                name=player_name,
                initial_elo=initial_elo
            )
            db.add(player)
            total_created += 1
            print(f"    ✓ {player_name} (ELO: {initial_elo})")
        
        db.flush()
    
    db.commit()
    db.close()
    
    print(f"\n[OK] {total_created} jogador(es) criado(s)")


def verify_data():
    """Verifica dados criados"""
    print("\n[INFO] Verificando dados criados...")
    db = SessionLocal()
    
    event_count = db.query(Event).count()
    player_count = db.query(Player).count()
    organizador_count = db.query(Usuario).filter(
        Usuario.tipo == TipoUsuario.ORGANIZADOR
    ).count()
    
    db.close()
    
    print(f"  📌 Eventos: {event_count}")
    print(f"  👥 Jogadores: {player_count}")
    print(f"  📋 Organizadores: {organizador_count}")


def display_summary():
    """Exibe resumo de testes disponíveis"""
    print_header("DADOS DE TESTE CRIADOS COM SUCESSO!")
    
    print("\n✅ Contas Disponíveis para Teste:")
    print("  Admin:")
    print("    Email: admin@test.com")
    print("    Senha: Senha123!")
    print("\n  Organizador (Novo):")
    print("    Email: joao@eventos.com")
    print("    Senha: Senha123!")
    print("\n  Organizador (Novo):")
    print("    Email: maria@eventos.com")
    print("    Senha: Senha123!")
    print("\n  Jogador:")
    print("    Email: jogador@test.com")
    print("    Senha: Senha123!")
    
    print("\n✅ Dados Criados:")
    db = SessionLocal()
    
    event_count = db.query(Event).count()
    player_count = db.query(Player).count()
    
    db.close()
    
    print(f"  • {event_count} eventos")
    print(f"  • {player_count} jogadores")
    print(f"  • 2 contas de organizadores")
    
    print("\n📝 Próximas Etapas:")
    print("  1. Inicie o backend: cd backend && python main.py")
    print("  2. Inicie o frontend: cd frontend && npm start")
    print("  3. Acesse http://localhost:3000")
    print("  4. Faça login com uma das contas acima")
    print("  5. Navegue para 'Eventos' para ver os dados criados")


def main():
    """Executa criação completa de dados de teste"""
    print_header("CRIADOR DE DADOS DE TESTE")
    
    try:
        # 1. Limpa dados anteriores
        clear_test_data()
        
        # 2. Cria organizadores
        create_organizadores()
        
        # 3. Cria eventos
        create_events()
        
        # 4. Cria jogadores
        create_players()
        
        # 5. Verifica dados
        verify_data()
        
        # 6. Exibe resumo
        display_summary()
        
        print("\n" + "=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Erro durante criação de dados: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
