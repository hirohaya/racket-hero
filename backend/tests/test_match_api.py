#!/usr/bin/env python
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Usar token que foi pré-salvo na sessão anterior
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJvcmdAdGVzdC5jb20iLCJleHAiOjE3MzE5MTAxNzksInR5cGUiOiJvcmdhbml6YWRvciJ9.8P_x2WVZXvW0J4GgzqM0H5cqL0MQfJLhgW0g2bIbA4Q"

headers = {"Authorization": f"Bearer {token}"}

# Get matches for event 3
try:
    response = requests.get(f"{BASE_URL}/api/matches/3", headers=headers)
    print(f"Status: {response.status_code}")
    data = response.json()
    print("\n=== RAW RESPONSE ===")
    print(json.dumps(data, indent=2))
    
    if isinstance(data, list) and len(data) > 2:
        print("\n=== THIRD MATCH (created last) ===")
        match3 = data[2]
        print(f"ID: {match3.get('id')}")
        print(f"Player 1 ID: {match3.get('player_1_id')}")
        print(f"Player 2 ID: {match3.get('player_2_id')}")
        print(f"Winner ID: {match3.get('winner_id')}")
        print(f"Winner Name: {match3.get('winner_name')}")
except Exception as e:
    print(f"Error: {e}")
