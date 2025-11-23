import requests
import json
from datetime import datetime

# Login
r = requests.post('http://localhost:8000/api/auth/login', json={
    'email': 'organizador@test.com',
    'senha': 'Senha123!'
})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Obter eventos do organizador
r = requests.get('http://localhost:8000/api/events/meus-eventos', headers=headers)
events = r.json()
print(f"[1] Eventos encontrados: {len(events)}")

if not events:
    print("[1b] Criando novo evento...")
    r = requests.post(
        'http://localhost:8000/api/events',
        json={
            'name': 'Torneio Teste',
            'date': '2025-12-01',
            'time': '14:00',
            'active': True
        },
        headers=headers
    )
    if r.status_code == 201:
        event_id = r.json()['id']
        print(f"    ✓ Evento criado com ID: {event_id}")
    else:
        print(f"    ✗ Erro ao criar evento: {r.json()}")
        exit(1)
else:
    event_id = events[0]['id']

event_name = 'Torneio Teste'
print(f"[2] Usando evento: ID={event_id}, Nome={event_name}")

# Obter jogadores atuais
r = requests.get(f'http://localhost:8000/api/players/{event_id}', headers=headers)
current_players = r.json()
if not isinstance(current_players, list):
    print(f"[3] Erro ao obter jogadores: {current_players}")
    exit(1)
print(f"[3] Jogadores atuais: {len(current_players)}")
for p in current_players[:3]:
    print(f"    - {p.get('name', 'N/A')} (ID: {p.get('id')})")

# Testar adicionar jogador
print("\n[4] Testando adicionar jogador...")
r = requests.post(
    f'http://localhost:8000/api/players/eventos/{event_id}/add',
    json={
        'name': 'João Silva Novo',
        'club': 'Clube Teste',
        'initial_elo': 1650
    },
    headers=headers
)
print(f"    Status: {r.status_code}")
response = r.json()
print(f"    Response: {json.dumps(response, indent=2, ensure_ascii=False)}")

if r.status_code == 201:
    player_id = response['id']
    print(f"\n[5] Sucesso! Jogador criado com ID: {player_id}")
    
    # Obter jogadores novamente para confirmar
    r = requests.get(f'http://localhost:8000/api/players/{event_id}', headers=headers)
    new_players = r.json()
    print(f"[6] Jogadores após adicionar: {len(new_players) if isinstance(new_players, list) else 'ERRO'}")
    
    # Testar remover jogador
    print(f"\n[7] Testando remover jogador {player_id}...")
    r = requests.delete(
        f'http://localhost:8000/api/players/{player_id}',
        headers=headers
    )
    print(f"    Status: {r.status_code}")
    print(f"    Response: {r.json()}")
    
    # Verificar final
    r = requests.get(f'http://localhost:8000/api/players/{event_id}', headers=headers)
    final_players = r.json()
    print(f"[8] Jogadores finais: {len(final_players) if isinstance(final_players, list) else 'ERRO'}")
    print(f"\n✓ Todos os testes completados com sucesso!")
else:
    print(f"\n✗ Erro ao adicionar jogador: {response}")
