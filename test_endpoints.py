import requests
import json

r = requests.post('http://localhost:8000/api/auth/login', json={
    'email': 'organizador@test.com',
    'senha': 'Senha123!'
})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Testar os endpoints
print('Testando endpoints:')
for endpoint in ['/api/players/4', '/api/players/eventos/4/inscritos']:
    r = requests.get(f'http://localhost:8000{endpoint}', headers=headers)
    print(f'{endpoint}: Status {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'  Type: {type(data)}')
        if isinstance(data, list):
            print(f'  Count: {len(data)}')
        print(f'  First 100 chars: {str(data)[:100]}')
