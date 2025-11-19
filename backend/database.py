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
