"""
Testes de API para routers do Racket Hero
"""
import pytest
from models.usuario import Usuario
from models.event import Event
from models.player import Player
from models.match import Match
from utils.security import hash_password


@pytest.fixture
def test_admin_token(test_db, client):
    """Fixture para obter token de admin"""
    # Fazer login ou registrar
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@test.com", "senha": "Senha123!"}
    )
    
    # Se login falhar, primeiro registrar como admin
    if response.status_code != 200:
        client.post(
            "/api/auth/register",
            json={
                "email": "admin@test.com",
                "nome": "Admin",
                "senha": "Senha123!",
                "tipo": "admin"
            }
        )
        response = client.post(
            "/api/auth/login",
            json={"email": "admin@test.com", "senha": "Senha123!"}
        )
    
    return response.json().get("access_token")


class TestAuthRouter:
    """Testes para autenticação"""

    def test_register_user(self, client):
        """Testa criação de novo usuário"""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "novo@test.com",
                "nome": "Novo Usuário",
                "senha": "Senha123!",
                "tipo": "usuario"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data

    def test_register_duplicate_email(self, client):
        """Testa que email duplicado é rejeitado"""
        # Primeiro registro
        client.post(
            "/api/auth/register",
            json={
                "email": "teste@test.com",
                "nome": "User 1",
                "senha": "Senha123!",
                "tipo": "usuario"
            }
        )
        
        # Tentativa de registrar mesmo email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "teste@test.com",
                "nome": "User 2",
                "senha": "Senha123!",
                "tipo": "usuario"
            }
        )
        assert response.status_code == 400  # Email já existe

    def test_login_success(self, client):
        """Testa login bem-sucedido"""
        # Registrar primeiro
        client.post(
            "/api/auth/register",
            json={
                "email": "login@test.com",
                "nome": "Test",
                "senha": "Senha123!",
                "tipo": "usuario"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={"email": "login@test.com", "senha": "Senha123!"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client):
        """Testa login com senha errada"""
        client.post(
            "/api/auth/register",
            json={
                "email": "teste@test.com",
                "nome": "Test",
                "senha": "SenhaCorreta123!",
                "tipo": "usuario"
            }
        )
        
        response = client.post(
            "/api/auth/login",
            json={"email": "teste@test.com", "senha": "SenhaErrada123!"}
        )
        assert response.status_code == 401  # Senha incorreta


class TestEventRouter:
    """Testes para gerenciamento de eventos"""

    def test_create_event(self, client, test_admin_token):
        """Testa criação de evento"""
        response = client.post(
            "/api/events",
            json={
                "name": "Torneio Teste",
                "date": "2025-12-20",
                "time": "14:00",
                "active": True
            },
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "Torneio Teste"

    def test_list_events(self, client, test_admin_token):
        """Testa listagem de eventos"""
        # Criar evento primeiro
        client.post(
            "/api/events",
            json={
                "name": "Torneio 1",
                "date": "2025-12-20",
                "time": "14:00"
            },
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        
        # Listar
        response = client.get(
            "/api/events",
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_get_event_by_id(self, client, test_admin_token):
        """Testa obter evento por ID"""
        # Criar evento
        create_response = client.post(
            "/api/events",
            json={
                "name": "Torneio Teste",
                "date": "2025-12-20",
                "time": "14:00"
            },
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        event_id = create_response.json()["id"]
        
        # Obter
        response = client.get(
            f"/api/events/{event_id}",
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Torneio Teste"


class TestPlayerRouter:
    """Testes para gerenciamento de jogadores"""

    def test_create_player(self, client, test_admin_token):
        """Testa criação de jogador em um evento"""
        # Criar evento primeiro
        event_response = client.post(
            "/api/events",
            json={
                "name": "Torneio",
                "date": "2025-12-20",
                "time": "14:00"
            },
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        event_id = event_response.json()["id"]
        
        # Criar jogador
        response = client.post(
            "/api/players",
            json={
                "event_id": event_id,
                "name": "João Silva",
                "club": "Clube A",
                "initial_elo": 1600.0
            },
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        assert response.status_code == 201
        assert response.json()["name"] == "João Silva"
        assert response.json()["club"] == "Clube A"

    def test_list_event_players(self, client, test_admin_token):
        """Testa listagem de jogadores de um evento"""
        # Criar evento
        event_response = client.post(
            "/api/events",
            json={"name": "Torneio", "date": "2025-12-20", "time": "14:00"},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        event_id = event_response.json()["id"]
        
        # Criar jogadores
        for i in range(3):
            client.post(
                "/api/players",
                json={
                    "event_id": event_id,
                    "name": f"Jogador {i+1}",
                    "initial_elo": 1600.0
                },
                headers={"Authorization": f"Bearer {test_admin_token}"}
            )
        
        # Listar
        response = client.get(
            f"/api/players/eventos/{event_id}/inscritos",
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        assert response.status_code == 200
        assert len(response.json()) == 3


class TestMatchRouter:
    """Testes para gerenciamento de partidas"""

    @pytest.fixture
    def setup_match_test(self, client, test_admin_token):
        """Setup para testes de partida"""
        # Criar evento
        event_response = client.post(
            "/api/events",
            json={"name": "Torneio", "date": "2025-12-20", "time": "14:00"},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        event_id = event_response.json()["id"]
        
        # Criar jogadores
        p1_response = client.post(
            "/api/players",
            json={"event_id": event_id, "name": "Jogador 1", "initial_elo": 1600.0},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        p1_id = p1_response.json()["id"]
        
        p2_response = client.post(
            "/api/players",
            json={"event_id": event_id, "name": "Jogador 2", "initial_elo": 1600.0},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        p2_id = p2_response.json()["id"]
        
        return test_admin_token, event_id, p1_id, p2_id

    def test_create_match_with_winner(self, client, setup_match_test):
        """Testa criar partida COM vencedor"""
        token, event_id, p1_id, p2_id = setup_match_test
        
        response = client.post(
            "/api/matches",
            json={
                "event_id": event_id,
                "player_1_id": p1_id,
                "player_2_id": p2_id,
                "winner_id": p1_id
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["winner_id"] == p1_id

    def test_create_match_without_winner(self, client, setup_match_test):
        """Testa criar partida SEM vencedor (CRÍTICO)"""
        token, event_id, p1_id, p2_id = setup_match_test
        
        response = client.post(
            "/api/matches",
            json={
                "event_id": event_id,
                "player_1_id": p1_id,
                "player_2_id": p2_id,
                "winner_id": None  # Campo opcional
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 201
        assert response.json()["winner_id"] is None

    def test_update_match_add_winner(self, client, setup_match_test):
        """Testa editar partida para adicionar vencedor"""
        token, event_id, p1_id, p2_id = setup_match_test
        
        # Criar partida sem vencedor
        create_response = client.post(
            "/api/matches",
            json={
                "event_id": event_id,
                "player_1_id": p1_id,
                "player_2_id": p2_id,
                "winner_id": None
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        match_id = create_response.json()["id"]
        
        # Editar para adicionar vencedor
        response = client.put(
            f"/api/matches/{match_id}",
            json={"winner_id": p1_id},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["winner_id"] == p1_id


class TestRankingRouter:
    """Testes para ranking/Elo"""

    def test_get_ranking(self, client, test_admin_token):
        """Testa obter ranking de um evento"""
        # Criar evento
        event_response = client.post(
            "/api/events",
            json={"name": "Torneio", "date": "2025-12-20", "time": "14:00"},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        event_id = event_response.json()["id"]
        
        # Criar jogadores
        p1_response = client.post(
            "/api/players",
            json={"event_id": event_id, "name": "Jogador 1", "initial_elo": 1600.0},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        p1_id = p1_response.json()["id"]
        
        p2_response = client.post(
            "/api/players",
            json={"event_id": event_id, "name": "Jogador 2", "initial_elo": 1600.0},
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        p2_id = p2_response.json()["id"]
        
        # Criar partida com vencedor
        client.post(
            "/api/matches",
            json={
                "event_id": event_id,
                "player_1_id": p1_id,
                "player_2_id": p2_id,
                "winner_id": p1_id
            },
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        
        # Obter ranking
        response = client.get(
            f"/api/ranking/eventos/{event_id}/ranking",
            headers={"Authorization": f"Bearer {test_admin_token}"}
        )
        assert response.status_code == 200
        ranking = response.json()
        assert len(ranking) == 2
        # Verificar que jogador 1 tem Elo maior
        assert ranking[0]["elo"] > ranking[1]["elo"]
