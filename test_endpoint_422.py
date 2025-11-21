#!/usr/bin/env python
"""
Script para testar o endpoint /api/players/eventos/{event_id}/add após a correção
"""

import requests
import json

# URL base
API_BASE = "http://127.0.0.1:8000/api"

# Headers com autenticação
# Usando um token fictício para teste (pode não funcionar se a autenticação está ativa)
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test_token_for_testing"
}

# Dados do jogador a adicionar
player_data = {
    "name": "Teste Jogador",
    "club": None,  # Teste com None para replicar o erro 422
    "initial_elo": 1700
}

# Event ID (ajuste conforme necessário)
event_id = 1

print("=" * 70)
print("TESTE DO ENDPOINT: POST /api/players/eventos/{event_id}/add")
print("=" * 70)
print(f"\nURL: {API_BASE}/players/eventos/{event_id}/add")
print(f"Headers: {json.dumps(HEADERS, indent=2)}")
print(f"Payload: {json.dumps(player_data, indent=2)}")
print("\n" + "=" * 70)
print("Enviando requisição...")
print("=" * 70)

try:
    response = requests.post(
        f"{API_BASE}/players/eventos/{event_id}/add",
        json=player_data,
        headers=HEADERS
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 201:
        print("\n✓ [OK] Jogador adicionado com sucesso!")
    elif response.status_code == 422:
        print("\n✗ [ERRO] Status 422 - Unprocessable Entity")
        print("  Possíveis causas:")
        print("  1. Validação do Pydantic falhou")
        print("  2. Campos obrigatórios faltando")
        print("  3. Tipos de dados incorretos")
    else:
        print(f"\n⚠ Status inesperado: {response.status_code}")
        
except Exception as e:
    print(f"\n✗ Erro ao fazer requisição: {e}")
    print(f"  Tipo: {type(e).__name__}")
