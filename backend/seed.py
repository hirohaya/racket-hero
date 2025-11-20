"""
Script para popular dados de teste no banco de dados
Cria contas de teste e dados iniciais
"""
from database import SessionLocal
from models import Usuario, Event, Player, Match
from datetime import datetime, timedelta
from passlib.context import CryptContext
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    """Popula o banco com dados de teste"""
    db = SessionLocal()
    
    try:
        # Verificar se usuários já existem
        organizer = db.query(Usuario).filter(Usuario.email == "organizador@test.com").first()
        player = db.query(Usuario).filter(Usuario.email == "jogador@test.com").first()
        
        if not organizer:
            print("[OK] Criando usuário organizador...")
            organizer = Usuario(
                nome="Organizador Test",
                email="organizador@test.com",
                senha=pwd_context.hash("Senha123!"),
                eh_organizador=True
            )
            db.add(organizer)
            db.flush()
        else:
            print("[SKIP] Organizador já existe")
        
        if not player:
            print("[OK] Criando usuário jogador...")
            player = Usuario(
                nome="Jogador Test",
                email="jogador@test.com",
                senha=pwd_context.hash("Senha123!"),
                eh_organizador=False
            )
            db.add(player)
            db.flush()
        else:
            print("[SKIP] Jogador já existe")
        
        # Criar evento padrão se não existir
        event = db.query(Event).filter(Event.name == "Torneio Teste").first()
        if not event:
            print("[OK] Criando evento de teste...")
            event = Event(
                name="Torneio Teste",
                date="2025-11-25",
                time="14:00",
                active=True
            )
            db.add(event)
            db.flush()
        else:
            print("[SKIP] Evento de teste já existe")
        
        # Adicionar jogadores ao evento
        event_player = db.query(Player).filter(
            Player.event_id == event.id,
            Player.usuario_id == player.id
        ).first()
        
        if not event_player:
            print("[OK] Adicionando jogador ao evento...")
            event_player = Player(
                event_id=event.id,
                usuario_id=player.id,
                name=player.nome,
                initial_elo=1600,
                club="Test Club"
            )
            db.add(event_player)
            db.flush()
        else:
            print("[SKIP] Jogador já está no evento")
        
        # Commit de todas as mudanças
        db.commit()
        print("\n[OK] Database seeding completo!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Erro ao popular banco: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("[INFO] Iniciando seed do banco de dados...\n")
    success = seed_database()
    sys.exit(0 if success else 1)
