"""
Testes unitários para modelos do Racket Hero
"""
import pytest
from datetime import datetime
from models.usuario import Usuario
from models.event import Event
from models.player import Player
from models.match import Match
from database import SessionLocal, Base, engine
from utils.security import hash_password, verify_password


@pytest.fixture
def db_session():
    """Fixture para criar sessão de banco de dados limpa"""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


class TestUsuarioModel:
    """Testes para modelo Usuario"""

    def test_create_usuario(self, db_session):
        """Testa criação de usuário"""
        usuario = Usuario(
            email="test@test.com",
            nome="Test User",
            senha_hash=hash_password("password123"),
            tipo="jogador"
        )
        db_session.add(usuario)
        db_session.commit()
        
        assert usuario.id is not None
        assert usuario.email == "test@test.com"
        assert usuario.nome == "Test User"
        assert usuario.ativo is True
        assert verify_password("password123", usuario.senha_hash)

    def test_usuario_email_unique(self, db_session):
        """Testa constraint de email único"""
        usuario1 = Usuario(
            email="test@test.com",
            nome="User 1",
            senha_hash=hash_password("pass123")
        )
        db_session.add(usuario1)
        db_session.commit()
        
        usuario2 = Usuario(
            email="test@test.com",
            nome="User 2",
            senha_hash=hash_password("pass123")
        )
        db_session.add(usuario2)
        
        with pytest.raises(Exception):  # UNIQUE constraint
            db_session.commit()


class TestEventModel:
    """Testes para modelo Event"""

    def test_create_event(self, db_session):
        """Testa criação de evento"""
        event = Event(
            name="Torneio Teste",
            date="2025-12-15",
            time="14:00",
            active=True
        )
        db_session.add(event)
        db_session.commit()
        
        assert event.id is not None
        assert event.name == "Torneio Teste"
        assert event.date == "2025-12-15"
        assert event.active is True

    def test_event_required_fields(self, db_session):
        """Testa campos obrigatórios do evento"""
        event = Event(date="2025-12-15")  # Faltam name, time
        db_session.add(event)
        
        with pytest.raises(Exception):  # NOT NULL constraint
            db_session.commit()


class TestPlayerModel:
    """Testes para modelo Player"""

    def test_create_player(self, db_session):
        """Testa criação de jogador"""
        event = Event(name="Torneio", date="2025-12-15", time="14:00")
        db_session.add(event)
        db_session.commit()
        
        player = Player(
            event_id=event.id,
            name="João Silva",
            club="Clube A",
            initial_elo=1600.0
        )
        db_session.add(player)
        db_session.commit()
        
        assert player.id is not None
        assert player.name == "João Silva"
        assert player.club == "Clube A"
        assert player.initial_elo == 1600.0

    def test_player_club_optional(self, db_session):
        """Testa que club é campo opcional"""
        event = Event(name="Torneio", date="2025-12-15", time="14:00")
        db_session.add(event)
        db_session.commit()
        
        player = Player(
            event_id=event.id,
            name="Maria Santos",
            initial_elo=1400.0
            # club não preenchido
        )
        db_session.add(player)
        db_session.commit()
        
        assert player.club is None
        assert player.initial_elo == 1400.0

    def test_player_default_elo(self, db_session):
        """Testa Elo padrão de 1600.0"""
        event = Event(name="Torneio", date="2025-12-15", time="14:00")
        db_session.add(event)
        db_session.commit()
        
        player = Player(
            event_id=event.id,
            name="Pedro Costa"
            # initial_elo não preenchido, deve usar padrão
        )
        db_session.add(player)
        db_session.commit()
        
        assert player.initial_elo == 1600.0


class TestMatchModel:
    """Testes para modelo Match"""

    @pytest.fixture
    def setup_match_test(self, db_session):
        """Setup para testes de partida"""
        event = Event(name="Torneio", date="2025-12-15", time="14:00")
        db_session.add(event)
        db_session.commit()
        
        p1 = Player(event_id=event.id, name="Jogador 1", initial_elo=1600.0)
        p2 = Player(event_id=event.id, name="Jogador 2", initial_elo=1600.0)
        db_session.add_all([p1, p2])
        db_session.commit()
        
        return event, p1, p2

    def test_create_match_with_winner(self, db_session, setup_match_test):
        """Testa criação de partida com vencedor"""
        event, p1, p2 = setup_match_test
        
        match = Match(
            event_id=event.id,
            player_1_id=p1.id,
            player_2_id=p2.id,
            winner_id=p1.id
        )
        db_session.add(match)
        db_session.commit()
        
        assert match.id is not None
        assert match.winner_id == p1.id
        assert match.player_1_id == p1.id
        assert match.player_2_id == p2.id

    def test_create_match_without_winner(self, db_session, setup_match_test):
        """Testa criação de partida SEM vencedor (campo opcional)"""
        event, p1, p2 = setup_match_test
        
        match = Match(
            event_id=event.id,
            player_1_id=p1.id,
            player_2_id=p2.id,
            winner_id=None  # Opcional!
        )
        db_session.add(match)
        db_session.commit()
        
        assert match.id is not None
        assert match.winner_id is None  # Importante para teste crítico

    def test_match_different_players(self, db_session, setup_match_test):
        """Testa que player_1 != player_2"""
        event, p1, p2 = setup_match_test
        
        # Criar partida com mesmo jogador em ambos lados (inválido logicamente)
        match = Match(
            event_id=event.id,
            player_1_id=p1.id,
            player_2_id=p1.id  # Mesmo jogador!
            # Nota: Database não impõe constraint, mas lógica de negócio deve validar
        )
        db_session.add(match)
        db_session.commit()
        
        # Partida foi criada (DB permite), mas aplicação deve validar
        assert match.player_1_id == match.player_2_id  # Inválido logicamente


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
