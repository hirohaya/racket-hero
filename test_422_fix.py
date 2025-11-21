#!/usr/bin/env python
"""
Script para testar o erro 422 após a correção
"""

import json
import sys
sys.path.insert(0, 'backend')

from pydantic import BaseModel, ValidationError
from typing import Optional

class AddPlayerRequest(BaseModel):
    """Schema para adicionar jogador a um evento - CORRIGIDO"""
    name: str
    club: Optional[str] = None
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

# Teste 2: club como None (o problema anterior)
print("\n" + "=" * 60)
print("TESTE 2: club como None (problema anterior)")
print("=" * 60)
try:
    data = {
        "name": "Maria Santos",
        "club": None,
        "initial_elo": 1600
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

# Teste 4: initial_elo como string (conversão automática)
print("\n" + "=" * 60)
print("TESTE 4: initial_elo como string (conversão automática)")
print("=" * 60)
try:
    data = {
        "name": "Ana Silva",
        "initial_elo": "1600"
    }
    player = AddPlayerRequest(**data)
    print("✓ Sucesso!")
    print(f"  {player.model_dump_json()}")
except ValidationError as e:
    print(f"✗ Erro: {e}")

print("\n" + "=" * 60)
print("Schema do Pydantic (CORRIGIDO):")
print("=" * 60)
print(json.dumps(AddPlayerRequest.model_json_schema(), indent=2))
