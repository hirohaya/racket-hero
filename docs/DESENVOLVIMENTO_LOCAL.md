# Guia de Desenvolvimento Local - Racket Hero

**Data:** 19 de Novembro de 2025  
**Status:** MVP (v1.0)

---

## 🚀 Quick Start (5 minutos)

### 1. Clone e Setup
```bash
git clone https://github.com/hirohaya/racket-hero.git
cd racket-hero

# Backend
cd backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Iniciar Servidor
```bash
# Backend (terminal 1)
cd backend
python -m uvicorn main:app --reload

# Frontend (terminal 2)
cd frontend
npm start
```

### 3. Acessar
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## 📋 Pré-requisitos

### Obrigatório
- Python 3.13+
- Node.js 18+
- npm ou yarn
- Git

### Verificar Versões
```bash
python --version  # 3.13+
node --version    # v18+
npm --version     # 9+
```

---

## 🏗️ Estrutura de Pastas

```
backend/
├── main.py                 # Aplicação FastAPI
├── database.py             # SQLAlchemy setup
├── validators.py           # Pydantic schemas
├── backup_manager.py       # Sistema de backup
├── logger.py               # Logging padrão
├── logger_production.py    # JSON logging
│
├── models/                 # SQLAlchemy models
│   ├── usuario.py
│   ├── event.py
│   ├── player.py
│   └── match.py
│
├── routers/                # API endpoints
│   ├── auth.py             # Login/register
│   ├── events.py           # CRUD eventos
│   ├── players.py          # CRUD jogadores
│   ├── matches.py          # CRUD partidas
│   ├── ranking.py          # Rankings
│   └── evento_organizadores.py
│
├── schemas/                # Pydantic models
│   ├── auth.py
│   ├── matches.py
│   └── ...
│
├── utils/                  # Utilidades
│   ├── security.py         # JWT, hashing
│   ├── permissions.py      # Roles
│   └── ...
│
├── tests/                  # Testes
│   ├── test_api.py         # Testes principais
│   ├── conftest.py         # Fixtures
│   └── ...
│
└── requirements.txt        # Dependências

frontend/
├── src/
│   ├── App.js              # Componente raiz
│   ├── index.js            # Entry point
│   │
│   ├── pages/              # Páginas
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Home.js
│   │   └── ...
│   │
│   ├── components/         # Componentes reutilizáveis
│   ├── services/           # API calls
│   ├── hooks/              # Custom hooks
│   └── styles/             # CSS
│
└── public/                 # Assets estáticos
```

---

## 🔧 Configuração de Desenvolvimento

### Backend - Variáveis de Ambiente

**Criar arquivo:** `backend/.env`
```env
# Database
DATABASE_URL=sqlite:///./racket_hero.db

# JWT
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_LEVEL=DEBUG
JSON_LOGS=false

# Email (se implementar)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-app
```

### Frontend - Variáveis de Ambiente

**Criar arquivo:** `frontend/.env`
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_API_TIMEOUT=10000
```

---

## 🗄️ Database Setup

### Criar Database
```bash
cd backend
python -c "from database import Base, engine; Base.metadata.create_all(engine)"
```

### Seed Data (Desenvolvimento)

**Arquivo:** `backend/scripts/seed_dev.py`
```python
from database import SessionLocal
from models.usuario import Usuario
from models.event import Event
from models.player import Player
from utils.security import hash_password

db = SessionLocal()

# Criar usuários
users = [
    {"email": "admin@test.com", "senha": "Admin123!", "nome": "Admin"},
    {"email": "org@test.com", "senha": "Org123!", "nome": "Organizador"},
    {"email": "player@test.com", "senha": "Player123!", "nome": "Jogador"},
]

for u in users:
    user = Usuario(
        email=u["email"],
        senha=hash_password(u["senha"]),
        nome=u["nome"],
        tipo="admin" if u["email"] == "admin@test.com" else "usuario"
    )
    db.add(user)

db.commit()
print("[OK] Dados de teste criados")
```

**Executar:**
```bash
cd backend
python scripts/seed_dev.py
```

---

## 🧪 Executar Testes

### Backend
```bash
cd backend

# Testes básicos
pytest tests/test_api.py -v

# Com coverage
pytest tests/test_api.py --cov=. --cov-report=html

# Teste específico
pytest tests/test_api.py::TestAuthRouter::test_login_success -v

# Watch mode
pytest-watch tests/
```

### Frontend
```bash
cd frontend

# Testes básicos
npm test -- --watchAll=false

# Com coverage
npm test -- --coverage --watchAll=false

# Watch mode
npm test
```

---

## 🐛 Debugging

### Backend - VSCode

**Arquivo:** `.vscode/launch.json`
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "jinja": true,
      "justMyCode": false,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

**Iniciar:** F5 ou Run → Start Debugging

### Frontend - React DevTools

```bash
# Instalar extensão Chrome/Firefox
# React DevTools
# Redux DevTools (se usar Redux)
```

---

## 📝 Workflow de Desenvolvimento

### 1. Criar Feature Branch
```bash
git checkout -b feature/nome-da-feature
# ou
git checkout -b bugfix/nome-do-bug
# ou
git checkout -b docs/nome-doc
```

### 2. Fazer Mudanças

#### Backend
```bash
cd backend

# Editar código
# Rodar testes
pytest tests/test_api.py -v

# Verificar linting
pylint routers/
flake8 routers/

# Formatar código
black .
```

#### Frontend
```bash
cd frontend

# Editar código
# Verificar linting
npm run lint

# Formatar código
npm run format

# Rodar testes
npm test -- --watchAll=false
```

### 3. Commit
```bash
git add .
git commit -m "feat: descrição clara da mudança"
# ou
git commit -m "fix: corrige problema"
git commit -m "docs: atualiza documentação"
```

### 4. Push e Pull Request
```bash
git push origin feature/nome-da-feature
# Abrir PR no GitHub
```

### 5. Code Review
- Solicitar review de outro desenvolvedor
- Resolver comentários
- Rebase se necessário

### 6. Merge
```bash
# Após aprovação
git checkout main
git pull origin main
git merge feature/nome-da-feature
git push origin main
```

---

## 🔍 Ferramentas de Desenvolvimento

### Backend

#### Instaladas
```bash
# Linting
pylint
flake8
black

# Testing
pytest
pytest-cov
pytest-watch

# ORM/Database
sqlalchemy
alembic (para migrations)

# API
fastapi
uvicorn
pydantic
```

#### Recomendadas (instalar opcionalmente)
```bash
pip install ipdb          # Debugger interativo
pip install django-extensions  # Django shell_plus equivalent
pip install hypothesis    # Property-based testing
```

### Frontend

#### Instaladas
```bash
# Testing
jest
@testing-library/react
@testing-library/jest-dom

# Linting
eslint
eslint-plugin-react

# Formatting
prettier
```

#### Recomendadas
```bash
npm install -g debug     # Debug logging
npm install redux-devtools  # State debugging
```

---

## 📊 Checklist de PR

Antes de submeter pull request:

- [ ] Código segue convenções do projeto
- [ ] Testes passam (100%)
- [ ] Sem console.log() debug (exceto erros críticos)
- [ ] Documentação atualizada
- [ ] Sem conflitos com main
- [ ] Commits com mensagens claras
- [ ] 1 feature por PR (se possível)

---

## 🚨 Troubleshooting Comum

### Backend não inicia
```bash
# 1. Verificar Python
python --version

# 2. Verificar dependencies
pip list | grep fastapi

# 3. Verificar imports
cd backend && python -c "import main; print('OK')"

# 4. Limpar cache
rm -rf __pycache__ .pytest_cache
pip install -r requirements.txt --force-reinstall
```

### Frontend não inicia
```bash
# 1. Limpar cache
rm -rf node_modules package-lock.json
npm install

# 2. Limpar build
npm run build
rm -rf build/

# 3. Reiniciar servidor
npm start
```

### Database corrompido
```bash
cd backend

# 1. Backup
cp racket_hero.db racket_hero.db.bak

# 2. Recriare
rm racket_hero.db
python -c "from database import Base, engine; Base.metadata.create_all(engine)"

# 3. Seed data
python scripts/seed_dev.py
```

### Testes falhando
```bash
# Backend
cd backend
pytest tests/test_api.py -v --tb=short

# Frontend
cd frontend
npm test -- --verbose
```

---

## 📚 Referências

### Documentação Oficial
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [React](https://react.dev/)
- [Pydantic](https://docs.pydantic.dev/)

### Repositórios
- Backend: `/backend`
- Frontend: `/frontend`
- Docs: `/docs`
- Scripts: `/scripts`

### Contatos
- Issues: GitHub Issues
- Discussões: GitHub Discussions
- Documentação: `/docs/`

---

**Última Atualização:** 19 de Novembro de 2025  
**Mantido por:** Equipe de Desenvolvimento
