#!/usr/bin/env python3
"""
test_passo5_linear.py - Linear test without subprocesses
Testa PASSO 5 sequencialmente
"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print("  PASSO 5: TESTES DE PARTIDAS (LINEAR)")
print("="*70 + "\n")

# 1. Register users
print("[1] Registering users...")
try:
    r_org = requests.post(f"{BASE_URL}/api/auth/register", 
        json={"email": "org@t.com", "nome": "Organizador", "senha": "senha123", "tipo": "organizador"},
        timeout=5
    )
    print(f"    Org: {r_org.status_code}")
    
    r_j1 = requests.post(f"{BASE_URL}/api/auth/register",
        json={"email": "j1@t.com", "nome": "Jogador1", "senha": "senha123"},
        timeout=5
    )
    print(f"    J1: {r_j1.status_code}")
    
    r_j2 = requests.post(f"{BASE_URL}/api/auth/register",
        json={"email": "j2@t.com", "nome": "Jogador2", "senha": "senha123"},
        timeout=5
    )
    print(f"    J2: {r_j2.status_code}")
    
    r_j3 = requests.post(f"{BASE_URL}/api/auth/register",
        json={"email": "j3@t.com", "nome": "Jogador3", "senha": "senha123"},
        timeout=5
    )
    print(f"    J3: {r_j3.status_code}")
except Exception as e:
    print(f"[ERROR] Registration failed: {e}")
    exit(1)

# 2. Login
print("\n[2] Logging in...")
try:
    r_org_login = requests.post(f"{BASE_URL}/api/auth/login",
        json={"email": "org@t.com", "senha": "senha123"},
        timeout=5
    )
    token_org = r_org_login.json()["access_token"]
    print(f"    Org token: OK")
    
    r_j1_login = requests.post(f"{BASE_URL}/api/auth/login",
        json={"email": "j1@t.com", "senha": "senha123"},
        timeout=5
    )
    token_j1 = r_j1_login.json()["access_token"]
    print(f"    J1 token: OK")
    
    r_j2_login = requests.post(f"{BASE_URL}/api/auth/login",
        json={"email": "j2@t.com", "senha": "senha123"},
        timeout=5
    )
    token_j2 = r_j2_login.json()["access_token"]
    print(f"    J2 token: OK")
    
    r_j3_login = requests.post(f"{BASE_URL}/api/auth/login",
        json={"email": "j3@t.com", "senha": "senha123"},
        timeout=5
    )
    token_j3 = r_j3_login.json()["access_token"]
    print(f"    J3 token: OK")
except Exception as e:
    print(f"[ERROR] Login failed: {e}")
    exit(1)

# 3. Create event
print("\n[3] Creating event...")
try:
    r_event = requests.post(f"{BASE_URL}/events",
        headers={"Authorization": f"Bearer {token_org}"},
        json={"name": "Torneio Teste", "date": "2025-12-01", "time": "14:00"},
        timeout=5
    )
    if r_event.status_code not in [200, 201]:
        print(f"[ERROR] Event creation failed: {r_event.status_code} - {r_event.text}")
        exit(1)
    event_id = r_event.json()["id"]
    print(f"    Event ID: {event_id}")
except Exception as e:
    print(f"[ERROR] Event creation failed: {e}")
    exit(1)

# 4. Register players
print("\n[4] Registering players to event...")
try:
    p1_id = None
    p2_id = None
    p3_id = None
    
    tokens = [
        ("j1@t.com", token_j1, "p1"),
        ("j2@t.com", token_j2, "p2"),
        ("j3@t.com", token_j3, "p3")
    ]
    
    for email, token, var_name in tokens:
        r = requests.post(f"{BASE_URL}/players/eventos/{event_id}/inscricao",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        if r.status_code in [200, 201]:
            player_id = r.json()["id"]
            if var_name == "p1":
                p1_id = player_id
            elif var_name == "p2":
                p2_id = player_id
            elif var_name == "p3":
                p3_id = player_id
            print(f"    {email}: Player ID {player_id}")
        else:
            print(f"    [ERROR] {email} failed: {r.status_code} - {r.text}")
    
    if not (p1_id and p2_id and p3_id):
        print(f"[ERROR] Not all players registered: p1={p1_id}, p2={p2_id}, p3={p3_id}")
        exit(1)
except Exception as e:
    print(f"[ERROR] Player registration failed: {e}")
    exit(1)

# 5. Create match
print("\n[5] Creating match...")
try:
    r_match = requests.post(f"{BASE_URL}/matches",
        headers={"Authorization": f"Bearer {token_org}"},
        json={
            "event_id": event_id,
            "player_1_id": p1_id,
            "player_2_id": p2_id,
            "winner_id": p1_id
        },
        timeout=5
    )
    if r_match.status_code != 201:
        print(f"[ERROR] Match creation failed: {r_match.status_code} - {r_match.text}")
        exit(1)
    match_data = r_match.json()
    match_id = match_data["id"]
    p1_elo_after_create = match_data.get("player_1_elo")
    p2_elo_after_create = match_data.get("player_2_elo")
    print(f"    Match ID: {match_id}")
    print(f"    P1 Elo: {p1_elo_after_create}, P2 Elo: {p2_elo_after_create}")
except Exception as e:
    print(f"[ERROR] Match creation failed: {e}")
    exit(1)

# 6. List matches
print("\n[6] Listing matches...")
try:
    r_list = requests.get(f"{BASE_URL}/matches/{event_id}",
        timeout=5
    )
    if r_list.status_code == 200:
        matches = r_list.json()
        print(f"    Found {len(matches)} match(es)")
        for m in matches:
            print(f"      Match #{m['id']}: P1(Elo={m.get('player_1_elo')}) vs P2(Elo={m.get('player_2_elo')}), Winner={m.get('winner_id')}")
    else:
        print(f"[ERROR] List failed: {r_list.status_code}")
except Exception as e:
    print(f"[ERROR] List failed: {e}")
    exit(1)

# 7. Update match
print("\n[7] Updating match (change winner to P2)...")
try:
    r_update = requests.put(f"{BASE_URL}/matches/{match_id}",
        headers={"Authorization": f"Bearer {token_org}"},
        json={"winner_id": p2_id},
        timeout=5
    )
    if r_update.status_code != 200:
        print(f"[ERROR] Update failed: {r_update.status_code} - {r_update.text}")
        exit(1)
    updated_data = r_update.json()
    p1_elo_after_update = updated_data.get("player_1_elo")
    p2_elo_after_update = updated_data.get("player_2_elo")
    print(f"    P1 Elo: {p1_elo_after_update}, P2 Elo: {p2_elo_after_update}")
except Exception as e:
    print(f"[ERROR] Update failed: {e}")
    exit(1)

# 8. Delete match
print("\n[8] Deleting match...")
try:
    r_delete = requests.delete(f"{BASE_URL}/matches/{match_id}",
        headers={"Authorization": f"Bearer {token_org}"},
        timeout=5
    )
    if r_delete.status_code != 200:
        print(f"[ERROR] Delete failed: {r_delete.status_code} - {r_delete.text}")
        exit(1)
    print(f"    Match deleted successfully")
except Exception as e:
    print(f"[ERROR] Delete failed: {e}")
    exit(1)

# 9. Verify deletion
print("\n[9] Verifying deletion...")
try:
    r_verify = requests.get(f"{BASE_URL}/matches/{event_id}",
        timeout=5
    )
    if r_verify.status_code == 200:
        matches = r_verify.json()
        if len(matches) == 0:
            print(f"    [OK] No matches found (deleted successfully)")
        else:
            print(f"    [ERROR] Still found {len(matches)} match(es)")
            exit(1)
    else:
        print(f"[ERROR] Verify failed: {r_verify.status_code}")
        exit(1)
except Exception as e:
    print(f"[ERROR] Verify failed: {e}")
    exit(1)

print("\n" + "="*70)
print("  ALL TESTS PASSED!")
print("="*70 + "\n")
