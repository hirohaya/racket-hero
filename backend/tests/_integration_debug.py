import subprocess
import time
import requests
import json

BASE_URL = "http://localhost:8000"

# Start backend
print("[*] Starting backend...")
proc = subprocess.Popen(
    ["python", "start_backend.py"],
    cwd=r"c:\Users\hiros\OneDrive\Documents\projetos\racket-hero",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
time.sleep(3)

try:
    # Register org
    print("[1] Register organizador...")
    r = requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "org@t.com", "nome": "Org", "senha": "123", "tipo": "organizador"
    })
    print(f"    Status: {r.status_code}")
    
    # Register player
    print("[2] Register jogador...")
    r = requests.post(f"{BASE_URL}/api/auth/register", json={
        "email": "j1@t.com", "nome": "J1", "senha": "123"
    })
    print(f"    Status: {r.status_code}")
    
    # Login org
    print("[3] Login org...")
    r = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "org@t.com", "senha": "123"
    })
    token_org = r.json()["access_token"]
    print(f"    Status: {r.status_code}, Token OK")
    
    # Create event
    print("[4] Create event...")
    r = requests.post(f"{BASE_URL}/events",
        headers={"Authorization": f"Bearer {token_org}"},
        json={"name": "Test", "date": "2025-12-01", "time": "14:00"}
    )
    event_id = r.json()["id"]
    print(f"    Status: {r.status_code}, Event ID: {event_id}")
    
    # Login player
    print("[5] Login jogador...")
    r = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": "j1@t.com", "senha": "123"
    })
    token_j1 = r.json()["access_token"]
    print(f"    Status: {r.status_code}, Token OK")
    
    # Register player to event
    print("[6] Register player to event...")
    r = requests.post(f"{BASE_URL}/players/eventos/{event_id}/inscricao",
        headers={"Authorization": f"Bearer {token_j1}"}
    )
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.text[:200]}")
    if r.status_code in [200, 201]:
        data = r.json()
        p1_id = data.get("id")
        print(f"    Player ID: {p1_id}")
    else:
        print(f"    ERROR: {r.text}")
        
finally:
    proc.terminate()
    proc.wait(timeout=2)
