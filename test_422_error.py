#!/usr/bin/env python
"""
Script para testar o erro 422 ao adicionar jogador
"""

import json
import sys
sys.path.insert(0, 'backend')

from pydantic import BaseModel, ValidationError

class AddPlayerRequest(BaseModel):
    """Schema para adicionar jogador a um evento"""
    name: str
    club: str = None
    initial_elo: float = 1600.0

# Teste 1: Dados válidos
print("=" * 60)
print("TESTE 1: Dados válidos")
print("=" * 60)
try:
    data = {
        "name": "João Silva",
        "club": "Clube A",
        "initial_elo": 1600.0
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

# Teste 2: initial_elo como string (pode causar 422)
print("\n" + "=" * 60)
print("TESTE 2: initial_elo como string")
print("=" * 60)
try:
    data = {
        "name": "Maria Santos",
        "club": None,
        "initial_elo": "1600"
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

# Teste 3: Dados mínimos
print("\n" + "=" * 60)
print("TESTE 3: Dados mínimos (apenas name)")
print("=" * 60)
try:
    data = {
        "name": "Pedro Costa"
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

# Teste 4: Nome vazio
print("\n" + "=" * 60)
print("TESTE 4: Nome vazio")
print("=" * 60)
try:
    data = {
        "name": ""
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

# Teste 5: Falta nome (obrigatório)
print("\n" + "=" * 60)
print("TESTE 5: Falta campo 'name' (obrigatório)")
print("=" * 60)
try:
    data = {
        "club": "Clube B"
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

# Teste 6: initial_elo com valor inválido
print("\n" + "=" * 60)
print("TESTE 6: initial_elo com valor inválido (string pura)")
print("=" * 60)
try:
    data = {
        "name": "Ana Silva",
        "initial_elo": "abc"
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

print("\n" + "=" * 60)
print("Schema do Pydantic:")
print("=" * 60)
print(json.dumps(AddPlayerRequest.model_json_schema(), indent=2))
