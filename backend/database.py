# database.py - Configuração SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Obter URL do banco de dados das variáveis de ambiente
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./racket_hero.db")

# Criar engine
# Para SQLite :memory:, usar StaticPool para garantir mesma conexão
if DATABASE_URL == "sqlite:///:memory:":
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Usar mesmo banco para todas as conexões
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
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
            # Check if organizador already exists
            organizador = db.query(Usuario).filter(
                Usuario.email == "organizador@test.com"
            ).first()
            
            if organizador:
                # Already seeded
                print("[DEBUG] Test data already exists, skipping seed")
                return
            
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
            print("[DEBUG] Creating test data...")
            
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
            
            # Create test Event
            evento = Event(
                name="Torneio Teste",
                date="2025-12-01",
                time="14:00",
                active=True,
                usuario_id=organizador.id
            )
            db.add(evento)
            db.flush()
            print("[DEBUG] Event criado")
            
            # Add jogador to event
            player = Player(
                usuario_id=jogador.id,
                event_id=evento.id,
                elo_rating=1600
            )
            db.add(player)
            print("[DEBUG] Player adicionado")
            
            db.commit()
            print("[OK] Test data seeded successfully")
        finally:
            db.close()
    except Exception as e:
        import traceback
        print(f"[ERROR] Error in auto-seed: {e}")
        traceback.print_exc()
