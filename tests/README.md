# Tests - Massa de Dados e Testes E2E

## Estrutura

```
tests/
├── data/
│   ├── events.json      # Eventos de teste
│   ├── players.json     # Jogadores de teste
│   └── matches.json     # Partidas de teste
├── seed.py              # Script para popular banco com dados de teste
└── README.md           # Este arquivo
```

## Como Usar

### 1. Popular o Banco com Dados de Teste

```bash
# Entre no diretório do projeto
cd backend

# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1

# Execute o seed
python ../tests/seed.py
```

Isso irá:
- Limpar o banco de dados
- Criar 3 eventos
- Criar 8 jogadores
- Criar 5 partidas

### 2. Verificar os Dados

Abra o navegador em:
- `http://localhost:3000` - Frontend
- `http://localhost:3000/debug` - Ver logs

### 3. Testes E2E com Playwright MCP

Os testes E2E são executados manualmente usando o Playwright MCP sem gerar código.

## Dados de Teste

### Eventos (events.json)
- Campeonato Regional 2025 (2025-11-20)
- Torneio Local (2025-11-15)
- Casual Friday Night (2025-11-14)

### Jogadores (players.json)
Para cada evento, jogadores com Elo inicial variando de 1480 a 1700

### Partidas (matches.json)
Partidas conectando jogadores com vencedores definidos para teste de ranking

## Próximos Testes

1. **Backend (API)**
   - GET /events - Listar eventos
   - GET /players/{event_id} - Listar jogadores
   - POST /matches - Criar partida
   - GET /ranking/{event_id} - Ver rankings

2. **Frontend**
   - Navegar página de eventos
   - Visualizar jogadores
   - Criar nova partida
   - Verificar rankings

3. **Ranking & Elo**
   - Verificar cálculos de Elo após partidas
   - Confirmar atualizações em tempo real
