# 🏓 Racket Hero - Local Development Setup

Este arquivo descreve como configurar o projeto localmente para desenvolvimento.

## 📋 Pré-requisitos

- Python 3.9+ (backend)
- Node.js 16+ (frontend)
- PostgreSQL ou SQLite (local development)
- Git

## 🚀 Setup Rápido

### 1. Clone o Repositório

```bash
git clone https://github.com/hirohaya/racket-hero.git
cd racket-hero
```

### 2. Backend Setup

```bash
# Criar virtual environment
python -m venv backend/venv

# Ativar virtual environment
# Windows:
backend\venv\Scripts\activate
# macOS/Linux:
source backend/venv/bin/activate

# Instalar dependências
cd backend
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# Editar .env com suas configurações locais
```

### 3. Frontend Setup

```bash
# Instalar dependências
cd frontend
npm install

# Criar arquivo .env (se necessário)
# cp .env.example .env
```

### 4. Iniciar o Projeto

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # ou .venv\Scripts\activate no Windows
python main.py
# Acesso: http://127.0.0.1:8000
# Docs: http://127.0.0.1:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# Acesso: http://localhost:3000
```

## 📁 Estrutura do Projeto

```
racket-hero/
├── backend/              # FastAPI application
│   ├── main.py          # Entry point
│   ├── database.py       # SQLAlchemy config
│   ├── models/          # Database models
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic models
│   └── requirements.txt  # Python dependencies
│
├── frontend/            # React application
│   ├── src/
│   ├── public/
│   └── package.json
│
├── README.md            # Project overview
├── LOCAL_SETUP.md       # This file
└── docker-compose.yml   # Docker configuration
```

## 🗄️ Database Setup

### Desenvolvimento Local

Use SQLite por padrão (mais simples):

```python
# backend/.env
DATABASE_URL=sqlite:///./pingchampions.db
```

Ou use PostgreSQL:

```python
# backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/racket_hero
```

## 🧪 Testing

### Rodar testes

```bash
cd backend
pytest tests/
```

### Verificar cobertura

```bash
pytest tests/ --cov=. --cov-report=html
```

## 🐳 Docker Setup (Opcional)

```bash
# Build e iniciar com Docker Compose
docker-compose up -d

# Verificar logs
docker-compose logs -f

# Parar
docker-compose down
```

## 📝 Variáveis de Ambiente

### Backend (.env)

```
DATABASE_URL=sqlite:///./pingchampions.db
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### Frontend (.env)

```
REACT_APP_API_URL=http://127.0.0.1:8000
```

## 🔐 Autenticação

Usuários de teste (criados automaticamente):

- **Organizador**: `organizador@test.com` / `Senha123!`
- **Jogadores**: `jogador1@test.com` até `jogador10@test.com` / `Senha123!`

## 🛠️ Desenvolvimento

### Criar novo endpoint

1. Criar roteador em `backend/routers/novo_router.py`
2. Importar em `backend/main.py`
3. Testar em `http://127.0.0.1:8000/docs`

### Criar novo componente React

1. Criar em `frontend/src/components/NovoComponente.js`
2. Importar e usar em outras páginas
3. Testar no navegador

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'fastapi'"

```bash
# Ativar virtual environment
source backend/venv/bin/activate  # ou .venv\Scripts\activate
# Instalar dependências
pip install -r backend/requirements.txt
```

### Erro: "Port 8000 already in use"

```bash
# Usar porta diferente
python -m uvicorn main:app --port 8001
```

### Erro: "Cannot connect to database"

1. Verificar se PostgreSQL está rodando (se usando PostgreSQL)
2. Verificar DATABASE_URL em `.env`
3. Para SQLite, deletar arquivo `.db` para recriar

### Erro: "npm: command not found"

1. Instalar Node.js: https://nodejs.org/
2. Reiniciar terminal
3. Rodar `npm install` novamente

## 📚 Documentação

- [README.md](./README.md) - Overview do projeto
- [docs/](./docs/) - Documentação técnica
- [guides/](./guides/) - Guias de setup e configuração
- [deployment/](./deployment/) - Guias de deploy

## 📧 Support

Para dúvidas, abra uma issue no GitHub: https://github.com/hirohaya/racket-hero/issues

---

**Última atualização**: November 2025
