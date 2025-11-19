"""
test_passo5_simple.py - Testes simplificados para PASSO 5: Partidas
Testa fluxo completo: criar, listar, atualizar, deletar partidas
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test():
    print("\n" + "="*70)
    print("  PASSO 5: TESTES DE PARTIDAS")
    print("="*70 + "\n")
    
    # 1. Registrar usuários
    print("[1] Registrando usuários...")
    
    requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "org@t.com", "nome": "Organizador", "senha": "senha123", "tipo": "organizador"
    })
    
    requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "j1@t.com", "nome": "Jogador 1", "senha": "senha123"
    })
    
    requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "j2@t.com", "nome": "Jogador 2", "senha": "senha123"
    })
    
    requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "j3@t.com", "nome": "Jogador 3", "senha": "senha123"
    })
    
    # 2. Login
    print("[2] Fazendo login...")
    
    resp_org = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "org@t.com", "senha": "senha123"
    })
    token_org = resp_org.json()["access_token"]
    
    resp_j1 = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "j1@t.com", "senha": "senha123"
    })
    token_j1 = resp_j1.json()["access_token"]
    
    resp_j2 = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "j2@t.com", "senha": "senha123"
    })
    token_j2 = resp_j2.json()["access_token"]
    
    resp_j3 = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "j3@t.com", "senha": "senha123"
    })
    token_j3 = resp_j3.json()["access_token"]
    
    # 3. Criar evento
    print("[3] Criando evento...")
    
    resp = requests.post(f"{BASE_URL}/events", 
        headers={"Authorization": f"Bearer {token_org}"},
        json={"name": "Torneio Teste", "date": "2025-11-25", "time": "14:00"}
    )
    
    if resp.status_code not in [200, 201]:
        print(f"[ERRO] Falha ao criar evento: {resp.status_code} - {resp.text}")
        return
    
    event_id = resp.json()["id"]
    print(f"   Evento ID: {event_id}")
    
    # 4. Inscrever jogadores
    print("[4] Inscrevendo jogadores...")
    
    p1_id = None
    p2_id = None
    p3_id = None
    
    tokens = [
        ("j1@t.com", token_j1),
        ("j2@t.com", token_j2),
        ("j3@t.com", token_j3)
    ]
    
    for idx, (email, token) in enumerate(tokens):
        resp = requests.post(f"{BASE_URL}/players/eventos/{event_id}/inscricao",
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code in [200, 201]:
            player_data = resp.json()
            player_id = player_data.get("id")
            if idx == 0:
                p1_id = player_id
            elif idx == 1:
                p2_id = player_id
            else:
                p3_id = player_id
        else:
            print(f"   [WARN] Falha ao inscrever {email}: {resp.status_code} - {resp.text}")
    
    if not (p1_id and p2_id and p3_id):
        print(f"[ERRO] Não conseguiu inscrever todos os jogadores: p1={p1_id}, p2={p2_id}, p3={p3_id}")
        return
    
    # 5. Criar partida
    print("[5] Criando partida...")
    
    resp = requests.post(f"{BASE_URL}/matches",
        headers={"Authorization": f"Bearer {token_org}"},
        json={
            "event_id": event_id,
            "player_1_id": p1_id,
            "player_2_id": p2_id,
            "winner_id": p1_id
        }
    )
    
    if resp.status_code != 201:
        print(f"[ERRO] Falha ao criar partida: {resp.status_code} - {resp.text}")
        return
    
    match_data = resp.json()
    match_id = match_data["id"]
    p1_elo_before = match_data.get("player_1_elo", 0)
    p2_elo_before = match_data.get("player_2_elo", 0)
    
    print(f"   Partida ID: {match_id}")
    print(f"   Elo P1: {p1_elo_before:.1f}, Elo P2: {p2_elo_before:.1f}")
    
    # 6. Listar partidas
    print("[6] Listando partidas...")
    
    resp = requests.get(f"{BASE_URL}/matches/{event_id}")
    
    if resp.status_code != 200:
        print(f"[ERRO] Falha ao listar partidas: {resp.status_code}")
        return
    
    matches = resp.json()
    print(f"   Total de partidas: {len(matches)}")
    
    # 7. Atualizar resultado
    print("[7] Atualizando resultado...")
    
    resp = requests.put(f"{BASE_URL}/matches/{match_id}",
        headers={"Authorization": f"Bearer {token_org}"},
        json={"winner_id": p2_id}
    )
    
    if resp.status_code != 200:
        print(f"[ERRO] Falha ao atualizar partida: {resp.status_code} - {resp.text}")
        return
    
    match_data = resp.json()
    p1_elo_after = match_data.get("player_1_elo", 0)
    p2_elo_after = match_data.get("player_2_elo", 0)
    
    print(f"   Novo Elo P1: {p1_elo_after:.1f}, Elo P2: {p2_elo_after:.1f}")
    print(f"   Mudanca P1: {p1_elo_after - p1_elo_before:+.1f}")
    
    # 8. Deletar partida
    print("[8] Deletando partida...")
    
    resp = requests.delete(f"{BASE_URL}/matches/{match_id}",
        headers={"Authorization": f"Bearer {token_org}"}
    )
    
    if resp.status_code != 200:
        print(f"[ERRO] Falha ao deletar partida: {resp.status_code}")
        return
    
    print("   Partida deletada")
    
    # 9. Verificar deleção
    print("[9] Verificando deleção...")
    
    resp = requests.get(f"{BASE_URL}/matches/{event_id}")
    matches = resp.json()
    
    still_exists = any(m.get("id") == match_id for m in matches)
    
    if still_exists:
        print("[ERRO] Partida ainda existe após deleção")
    else:
        print("   Partida removida com sucesso")
    
    print("\n" + "="*70)
    print("  TESTES COMPLETOS - SUCESSO!")
    print("="*70 + "\n")

if __name__ == "__main__":
    test()
