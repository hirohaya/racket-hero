import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Configurar variável de ambiente ANTES de qualquer import
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Importar models para registrar
from models.usuario import Usuario  # noqa
from models.event import Event  # noqa
from models.player import Player  # noqa
from models.match import Match  # noqa

# Agora importar database e main
from database import Base, get_db, init_db
from main import app
import database


@pytest.fixture(scope="function")
def test_db():
    """Cria um banco de dados de teste limpo para cada teste"""
    # Usar o engine global que foi criado com :memory:
    engine = database.engine
    
    # Criar todas as tabelas usando Base metadata
    Base.metadata.create_all(bind=engine)
    
    # Criar session factory
    TestingSessionLocal = sessionmaker(
        autocommit=False, 
        autoflush=False, 
        bind=engine,
        expire_on_commit=False
    )
    
    # Override da dependency get_db
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Aplicar override
    app.dependency_overrides[get_db] = override_get_db
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_db):
    """Retorna TestClient com banco de dados de teste"""
    return TestClient(app)





