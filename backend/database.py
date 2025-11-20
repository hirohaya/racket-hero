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
        
        db = SessionLocal()
        
        # Check if organizador already exists
        organizador = db.query(Usuario).filter(
            Usuario.email == "organizador@test.com"
        ).first()
        
        if organizador:
            # Already seeded
            db.close()
            return
        
        # Only seed if DATABASE_URL indicates dev/staging (not production)
        db_url = os.getenv("DATABASE_URL", "sqlite:///./racket_hero.db")
        is_prod = "postgres" in db_url and "railway" in db_url
        
        # Also check if ENVIRONMENT is explicitly set to production
        env = os.getenv("ENVIRONMENT", "").lower()
        is_prod = is_prod or (env == "production")
        
        if is_prod:
            # Don't seed in production
            db.close()
            return
        
        try:
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
            
            # Add jogador to event
            player = Player(
                usuario_id=jogador.id,
                event_id=evento.id,
                elo_rating=1600
            )
            db.add(player)
            
            db.commit()
            print("[OK] Test data seeded successfully")
        except Exception as e:
            db.rollback()
            print(f"[WARNING] Failed to seed test data: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"[WARNING] Error in auto-seed: {e}")
