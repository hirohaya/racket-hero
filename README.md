# Racket Hero - Tournament Management System

![Status](https://img.shields.io/badge/status-production--ready-green)
![Tests](https://img.shields.io/badge/tests-36%2F36%20PASSING-green)
![Coverage](https://img.shields.io/badge/coverage-backend%3A%2039%25-blue)

## 📋 Overview

**Racket Hero** é um sistema de gerenciamento de torneios de pingue-pongue com ranking dinâmico (ELO), integração de autenticação JWT e admin dashboard.

### Status: ✅ PRODUCTION READY

- **Testes Backend**: 13/13 PASSING ✅
- **Testes Frontend**: 23/23 PASSING ✅
- **Coverage**: Backend 39% (>30% requirement)
- **Database**: SQLite com migrations
- **Deployment**: Pronto para produção

## 🚀 Quick Start

### Pré-requisitos
- Python 3.9+
- Node 16+
- npm/yarn

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v  # Run tests
python main.py              # Start server
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm test -- --watchAll=false  # Run tests
npm start                       # Start development server
```

### 3. Acessar Sistema
- **Backend API**: http://127.0.0.1:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://127.0.0.1:8000/docs

### 4. Criar Contas de Teste (Opcional)
```bash
# Criar 3 contas padrão (Admin, Jogador, Organizador)
cd backend
python
>>> from tests.create_test_accounts import create_test_accounts_db
>>> create_test_accounts_db()
```

**Contas padrão criadas:**
- 🔐 **Admin**: `admin@test.com` / `Senha123!`
- 🎯 **Jogador**: `jogador@test.com` / `Senha123!`
- 📋 **Organizador**: `organizador@test.com` / `Senha123!`

## 📊 Características Implementadas

### Core Features
- ✅ Autenticação JWT com refresh tokens
- ✅ Gerenciamento de eventos (torneios)
- ✅ Registro de jogadores
- ✅ Criação e edição de partidas
- ✅ Ranking dinâmico com ELO
- ✅ Admin dashboard

### Infraestrutura
- ✅ Logging JSON estruturado em produção
- ✅ Sistema de backup automático (diário 03:00)
- ✅ Validação robusta com Pydantic
- ✅ Error handling centralizado
- ✅ Health checks

### Testes
- ✅ 13 testes backend (API endpoints)
- ✅ 25+ testes de modelos
- ✅ 23 testes frontend (componentes)
- ✅ Fixtures pytest com database em memória

## 📁 Estrutura do Projeto

```
racket-hero/
├── README.md                    # Este arquivo
├── COMECE_AQUI.md              # Guia de início rápido
├── INDEX.md                    # Índice de documentação
│
├── backend/
│   ├── main.py                 # FastAPI app principal
│   ├── database.py             # SQLAlchemy setup
│   ├── logger_production.py    # JSON logging
│   ├── backup_manager.py       # Backup system
│   ├── validators.py           # Pydantic schemas
│   │
│   ├── models/                 # SQLAlchemy models
│   ├── routers/                # API route handlers
│   ├── schemas/                # Request/response models
│   ├── utils/                  # Utilities
│   ├── tests/                  # Pytest suite
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── pages/              # Route pages
│   │   ├── components/         # Reusable components
│   │   ├── context/            # React context
│   │   ├── services/           # API calls
│   │   ├── __tests__/          # Jest tests
│   │   └── App.test.js
│   ├── package.json
│   └── public/
│
└── .gitignore
```

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py -v
```

### Frontend Tests
```bash
cd frontend
# Run all tests
npm test -- --watchAll=false --no-coverage

# Run with coverage
npm test -- --watchAll=false --coverage
```

## 📚 Documentation

### Documentação Principal
- **[COMECE_AQUI.md](COMECE_AQUI.md)** - Guia de início rápido e status atual
- **[INDEX.md](INDEX.md)** - Índice completo da documentação
- **[GUIA_IMPLEMENTACAO.md](GUIA_IMPLEMENTACAO.md)** - Guia técnico de implementação

### Próximos Passos & Planejamento
- **[docs/PROXIMOS_PASSOS.md](docs/PROXIMOS_PASSOS.md)** - Roadmap detalhado v1.1+
- **[docs/ROADMAP.md](docs/ROADMAP.md)** - Timeline e planejamento técnico
- **[docs/CHECKLIST_PRODUCAO.md](docs/CHECKLIST_PRODUCAO.md)** - Validação pré-deploy

### Desenvolvimento
- **[docs/DESENVOLVIMENTO_LOCAL.md](docs/DESENVOLVIMENTO_LOCAL.md)** - Setup local e workflow
- **[docs/FAQ.md](docs/FAQ.md)** - Perguntas frequentes e troubleshooting
- **[docs/screenshots/](docs/screenshots/)** - Screenshots e imagens

### Estrutura de Documentação
```
docs/
├── PROXIMOS_PASSOS.md          # O que fazer a seguir
├── ROADMAP.md                  # Timeline de releases
├── CHECKLIST_PRODUCAO.md       # Deploy checklist
├── DESENVOLVIMENTO_LOCAL.md    # Dev setup
├── FAQ.md                      # Perguntas frequentes
└── screenshots/                # Imagens/prints
```

## 🔑 Key Endpoints

### Auth
- `POST /api/auth/register` - Criar conta
- `POST /api/auth/login` - Login
- `POST /api/auth/refresh` - Refresh token

### Events
- `POST /api/events` - Criar evento
- `GET /api/events` - Listar eventos
- `GET /api/events/{event_id}` - Detalhes do evento

### Players
- `POST /api/players` - Adicionar jogador
- `GET /api/events/{event_id}/players` - Listar jogadores

### Matches
- `POST /api/matches` - Criar partida
- `PATCH /api/matches/{match_id}` - Atualizar resultado

### Ranking
- `GET /api/events/{event_id}/ranking` - Ranking ELO

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite + SQLAlchemy
- **Auth**: JWT (PyJWT)
- **Validation**: Pydantic V2
- **Logging**: Python logging (JSON)
- **Testing**: Pytest

### Frontend
- **Framework**: React 19
- **Router**: React Router 6
- **HTTP**: Axios
- **Testing**: Jest + React Testing Library
- **Styling**: CSS modules

## 📈 Project Metrics

| Métrica | Valor |
|---------|-------|
| Lines of Code (Backend) | 3000+ |
| Lines of Code (Frontend) | 2000+ |
| Test Coverage (Backend) | 39% |
| Tests Passing | 36/36 ✅ |
| API Endpoints | 20+ |
| Documentation | Complete |

## 🚦 Status Commands

### Check Backend Health
```bash
curl http://127.0.0.1:8000/health
```

### Check Frontend Build
```bash
cd frontend && npm run build
```

### Run Full Test Suite
```bash
# Backend
cd backend && pytest tests/ -v

# Frontend
cd frontend && npm test -- --watchAll=false
```

## 🔐 Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
REACT_APP_API_URL=http://127.0.0.1:8000
```

## �️ Debug & Helper Scripts (Local Use Only)

Para depuração e testes locais, você pode criar scripts auxiliares na pasta `scripts/`:

### Exemplo: Script para Criar Contas Adicionais
```python
# scripts/create_more_accounts.py (LOCAL ONLY - not tracked in git)
import sys
sys.path.insert(0, '../backend')
from tests.create_more_test_accounts import main
main()
```

### Exemplo: Script para Testar API
```python
# scripts/test_api_health.py (LOCAL ONLY - not tracked in git)
import requests
response = requests.get("http://127.0.0.1:8000/health")
print(response.json())
```

**Nota**: Scripts de debug e ferramentas de desenvolvimento local estão no `.gitignore` para manter o repositório limpo. Crie-os conforme necessário para seus testes locais.

## �🐛 Troubleshooting

### Backend Issues
- **ModuleNotFoundError**: Execute `pip install -r requirements.txt`
- **Database locked**: Delete `*.db` and restart
- **Port 8000 in use**: Change `PORT` in main.py

### Frontend Issues
- **npm install fails**: Delete `node_modules/` and `package-lock.json`
- **Tests fail**: Run `npm test -- --clearCache --watchAll=false`
- **Port 3000 in use**: Change `PORT` environment variable

## 📞 Support

Para dúvidas ou problemas:
1. Consulte [COMECE_AQUI.md](COMECE_AQUI.md)
2. Verifique [INDEX.md](INDEX.md)
3. Abra uma issue no repositório

## 📝 License

MIT License - See LICENSE file for details

---

**Última Atualização**: 19 de Novembro, 2025  
**Status**: Production Ready ✅  
**Versão**: 1.2.0  

Criado com ❤️ usando FastAPI + React
