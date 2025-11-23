# database.py - Configuração SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool, NullPool
import os

# Obter URL do banco de dados das variáveis de ambiente
# Railway fornece DATABASE_URL automaticamente para PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./racket_hero.db")

# Determinar se é PostgreSQL ou SQLite
is_postgres = DATABASE_URL.startswith("postgresql://") or DATABASE_URL.startswith("postgres://")

# Criar engine com configurações apropriadas
if DATABASE_URL == "sqlite:///:memory:":
    # SQLite em memória para testes
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
elif is_postgres:
    # PostgreSQL em produção (Railway)
    # Usar NullPool para evitar problemas de conexão
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        echo=False
    )
else:
    # SQLite local para desenvolvimento
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# Criar session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar base para models
Base = declarative_base()

def get_db():
    """
    Dependency para obter session do banco de dados.
    Usar em rotas FastAPI.
    
    Exemplo:
        @router.get("/items")
        async def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializar banco de dados (criar todas as tabelas)."""
    # Importar models para registrar no Base
    from models.usuario import Usuario  # noqa
    from models.event import Event  # noqa
    from models.player import Player  # noqa
    from models.match import Match  # noqa
    from models.evento_organizador import EventoOrganizador  # noqa
    
    Base.metadata.create_all(bind=engine)
    
    # Seed test data in development/staging environments (if database is empty)
    _seed_test_data_if_empty()


def _seed_test_data_if_empty():
    """Seed test data if database is empty (for dev/staging)."""
    try:
        from models.usuario import Usuario, TipoUsuario
        from models.event import Event
        from models.player import Player
        from utils.security import hash_password
        import os
        
        print("[DEBUG] Auto-seed function called")
        
        db = SessionLocal()
        
        try:
            # Check if test Organizador already exists
            organizador = db.query(Usuario).filter(
                Usuario.email == "organizador@test.com"
            ).first()
            
            if organizador:
                # Already seeded - now check if we need to add additional players
                print("[DEBUG] Test Organizador exists, checking for additional players...")
            else:
                # Get database URL
                db_url = os.getenv("DATABASE_URL", "sqlite:///./racket_hero.db")
                print(f"[DEBUG] DATABASE_URL: {db_url[:50]}...")
                
                # Skip production environments
                # Production typically has postgres + railway or explicit PROD env var
                env = os.getenv("NODE_ENV", os.getenv("ENVIRONMENT", "development")).lower()
                is_production = (env == "production")
                
                print(f"[DEBUG] Environment: {env}, Is Production: {is_production}")
                
                if is_production:
                    print("[DEBUG] Skipping seed in production")
                    return
                
                # Seed test data
                print("[DEBUG] Creating initial test data...")
                
                # Create test Organizador
                organizador = Usuario(
                    email="organizador@test.com",
                    nome="Organizador Teste",
                    senha_hash=hash_password("Senha123!"),
                    tipo=TipoUsuario.ORGANIZADOR,
                    ativo=True
                )
                db.add(organizador)
                db.flush()
                print("[DEBUG] Organizador criado")
                
                # Create test Jogador
                jogador = Usuario(
                    email="jogador@test.com",
                    nome="Jogador Teste",
                    senha_hash=hash_password("Senha123!"),
                    tipo=TipoUsuario.JOGADOR,
                    ativo=True
                )
                db.add(jogador)
                db.flush()
                print("[DEBUG] Jogador criado")
            
            # Ensure test Event exists
            evento = db.query(Event).filter(Event.name == "Torneio Teste").first()
            if not evento:
                print("[DEBUG] Criando Torneio Teste...")
                evento = Event(
                    name="Torneio Teste",
                    date="2025-12-01",
                    time="14:00",
                    active=True,
                    usuario_id=organizador.id if organizador else None
                )
                db.add(evento)
                db.flush()
                print("[DEBUG] Event criado")
            else:
                print("[DEBUG] Torneio Teste já existe")
            
            # Ensure Organizador is linked to Event in evento_organizador table
            if organizador and evento:
                from models.evento_organizador import EventoOrganizador
                
                organizador_link = db.query(EventoOrganizador).filter(
                    EventoOrganizador.event_id == evento.id,
                    EventoOrganizador.usuario_id == organizador.id
                ).first()
                
                if not organizador_link:
                    print("[DEBUG] Adicionando Organizador como gerenciador do evento...")
                    org_link = EventoOrganizador(
                        event_id=evento.id,
                        usuario_id=organizador.id,
                        é_criador=1  # Mark as creator
                    )
                    db.add(org_link)
                    print("[DEBUG] Organizador linkado ao evento")
                else:
                    print("[DEBUG] Organizador já é gerenciador do evento")
            
            # Ensure test jogador is in the event
            if organizador and evento:
                jogador_player = db.query(Player).filter(
                    Player.event_id == evento.id,
                    Player.name == "Jogador Teste"
                ).first()
                
                if not jogador_player:
                    player = Player(
                        usuario_id=organizador.id,  # Use organizador's ID for now
                        event_id=evento.id,
                        name="Jogador Teste",
                        initial_elo=1600
                    )
                    db.add(player)
                    print("[DEBUG] Test Player adicionado")
                else:
                    print("[DEBUG] Test Player já existe")
            
            # Add additional test players for search functionality
            print("[DEBUG] Adicionando jogadores adicionais para teste de busca...")
            
            test_players = [
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
            
            for nome, email in test_players:
                existing_user = db.query(Usuario).filter(Usuario.email == email).first()
                if not existing_user:
                    new_user = Usuario(
                        email=email,
                        nome=nome,
                        senha_hash=hash_password("Senha123!"),
                        tipo=TipoUsuario.JOGADOR,
                        ativo=True
                    )
                    db.add(new_user)
                    db.flush()
                    print(f"[DEBUG] Jogador {nome} criado")
                else:
                    print(f"[DEBUG] Jogador {nome} já existe")
            
            db.commit()
            print("[OK] Test data seeded successfully")
        finally:
            db.close()
    except Exception as e:
        import traceback
        print(f"[ERROR] Error in auto-seed: {e}")
        traceback.print_exc()
