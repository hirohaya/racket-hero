# Racket Hero - Índice do Repositório

## 📁 Estrutura de Diretórios

```
racket-hero/
├── backend/                  # Backend FastAPI + Python
│   ├── models/              # Modelos SQLAlchemy (Usuario, Event, Player, Match)
│   ├── routers/             # Endpoints da API (auth, events, players, matches, ranking)
│   ├── schemas/             # Schemas Pydantic
│   ├── utils/               # Utilitários (security, validators)
│   ├── tests/               # Testes unitários
│   ├── main.py              # Aplicação principal FastAPI
│   ├── database.py          # Configuração SQLAlchemy/PostgreSQL
│   └── requirements.txt      # Dependências Python
│
├── frontend/                # Frontend React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── pages/           # Páginas da aplicação
│   │   ├── services/        # API clients (axios)
│   │   └── App.js           # Componente raiz
│   └── public/
│
├── deployment/              # 📚 Guias de Deploy e Railway
│   ├── RAILWAY.md           # Visão geral Railway
│   ├── RAILWAY_SETUP_GUIDE.md
│   ├── RAILWAY_QUICK_START.md
│   ├── RAILWAY_VOLUME_SETUP.md
│   ├── RAILWAY_VOLUME_VISUAL_GUIDE.md
│   ├── RAILWAY_ARCHITECTURE.md
│   ├── RAILWAY_ENVIRONMENTS.md
│   └── RAILWAY_STEP_BY_STEP.md
│
├── guides/                  # 📖 Guias de Configuração
│   ├── GRAPHQL_ANALYSIS.md          # Análise: GraphQL vs REST
│   ├── POSTGRESQL_MIGRATION.md      # Migração SQLite → PostgreSQL
│   ├── POSTGRESQL_ACCESS_GUIDE.md   # Como acessar PostgreSQL
│   ├── DBEAVER_SETUP_QUICK.md       # Setup DBeaver
│   ├── TEST_ACCOUNTS_RAILWAY.md     # Contas de teste
│   └── VERIFY_RAILWAY_VOLUME.md     # Verificar volume Railway
│
├── docs/                    # 📝 Documentação Técnica
│   ├── ENDPOINTS_REDUNDANCY_ANALYSIS.md
│   ├── SEED_DATABASE_ISSUE.md
│   ├── AUTH_FIX_SUMMARY.md
│   ├── DELIVERY_SUMMARY.md
│   ├── DEPLOY_DADOS_TESTE_DEV.md
│   ├── DEV_ENVIRONMENT_TEST_REPORT.md
│   ├── LOCAL_ENVIRONMENT_TEST_REPORT.md
│   ├── DOCUMENTATION_INDEX.md
│   └── ... (mais documentação)
│
├── scripts/                 # 🔧 Scripts Utilitários
│   ├── migrate_create_tables.py
│   ├── add_test_data.py
│   ├── test_endpoints.py
│   ├── test_player_management.py
│   └── test_environments.sh
│
├── design-specs/            # 🎨 Especificações de Design
│   ├── DESIGN_SPECS.md
│   └── ... (assets e specs)
│
├── tests/                   # 🧪 Testes E2E
├── logs/                    # 📊 Logs de Aplicação
├── README.md                # 📌 Guia Principal
├── Dockerfile               # 🐳 Configuração Docker
├── docker-compose.yml       # Docker Compose
├── railway.toml             # Configuração Railway
├── start.sh                 # Script de inicialização
└── LICENSE
```

---

## 🚀 Quick Start

### 1. Leitura Recomendada (Ordem)
1. **README.md** - Overview do projeto
2. **deployment/RAILWAY_QUICK_START.md** - Deploy rápido
3. **guides/POSTGRESQL_MIGRATION.md** - Setup PostgreSQL
4. **guides/TEST_ACCOUNTS_RAILWAY.md** - Contas de teste

### 2. Setup Local
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Frontend (outro terminal)
cd frontend
npm install
npm start
```

### 3. Deploy no Railway
- Consulte: `deployment/RAILWAY_QUICK_START.md`
- Criar volume: `deployment/RAILWAY_VOLUME_SETUP.md`
- Contas de teste: `guides/TEST_ACCOUNTS_RAILWAY.md`

---

## 📚 Documentação por Tópico

### 🔐 Autenticação & Segurança
- `docs/AUTH_FIX_SUMMARY.md` - Correções de autenticação

### 🎯 API Endpoints
- `docs/ENDPOINTS_REDUNDANCY_ANALYSIS.md` - Análise de endpoints
- `backend/routers/*.py` - Código fonte dos routers

### 💾 Banco de Dados
- `guides/POSTGRESQL_MIGRATION.md` - Migração SQLite → PostgreSQL
- `guides/POSTGRESQL_ACCESS_GUIDE.md` - Acessar PostgreSQL
- `docs/SEED_DATABASE_ISSUE.md` - Problemas de seed
- `guides/TEST_ACCOUNTS_RAILWAY.md` - Contas de teste

### 🚀 Deployment
- `deployment/RAILWAY_SETUP_GUIDE.md` - Setup completo
- `deployment/RAILWAY_VOLUME_SETUP.md` - Volume persistente
- `guides/VERIFY_RAILWAY_VOLUME.md` - Verificar volume

### 🛠️ Ferramentas
- `guides/DBEAVER_SETUP_QUICK.md` - DBeaver (Database IDE)
- `guides/POSTGRESQL_ACCESS_GUIDE.md` - Acessar PostgreSQL (6 métodos)

### 🧪 Testing
- `docs/DEV_ENVIRONMENT_TEST_REPORT.md` - Relatório testes
- `scripts/test_endpoints.py` - Testes de endpoints
- `backend/tests/test_api.py` - Testes unitários

### 🏗️ Arquitetura
- `deployment/RAILWAY_ARCHITECTURE.md` - Arquitetura Railway
- `docs/DOCUMENTATION_INDEX.md` - Índice completo

### 📊 Análises
- `guides/GRAPHQL_ANALYSIS.md` - GraphQL vs REST

---

## 🎮 Usar o Projeto

### Endpoints Principais
```
GET    /health                    # Health check
POST   /api/auth/register         # Registrar
POST   /api/auth/login            # Login
GET    /api/events                # Listar eventos
POST   /api/events                # Criar evento
GET    /api/events/{id}           # Obter evento
POST   /api/players               # Adicionar jogador
GET    /api/players/{event_id}    # Listar jogadores
POST   /api/matches               # Criar partida
GET    /api/matches/{event_id}    # Listar partidas
GET    /api/ranking/{event_id}    # Ver ranking
```

### Contas de Teste (Railway)
- **Organizador:** `organizador@test.com` / `Senha123!`
- **Jogador:** `jogador@test.com` / `Senha123!`
- (+ 10 jogadores adicionais para teste)

---

## 📋 Checklist de Setup

- [ ] Clonar repositório
- [ ] Setup backend (venv + pip install)
- [ ] Setup frontend (npm install)
- [ ] Rodar backend localmente
- [ ] Rodar frontend (localhost:3000)
- [ ] Testar endpoints via `/docs`
- [ ] Setup PostgreSQL no Railway
- [ ] Criar tabelas via `/admin/create-tables`
- [ ] Seed dados via `/admin/seed-test-data`
- [ ] Testar login e funcionalidades

---

## 🔗 Links Rápidos

| Recurso | Local |
|---------|-------|
| Deploy | https://railway.app/ |
| Docs API | `/docs` (após rodar backend) |
| Status | `/health` |
| Database | DBeaver (guides/DBEAVER_SETUP_QUICK.md) |

---

## 📞 Troubleshooting

| Problema | Solução |
|----------|---------|
| PostgreSQL 404 | `guides/POSTGRESQL_ACCESS_GUIDE.md` |
| Volume não persiste | `deployment/RAILWAY_VOLUME_SETUP.md` |
| Sem contas de teste | `guides/TEST_ACCOUNTS_RAILWAY.md` |
| Endpoints redundantes | `docs/ENDPOINTS_REDUNDANCY_ANALYSIS.md` |
| Seed problems | `docs/SEED_DATABASE_ISSUE.md` |

---

## ✨ Estrutura Limpa

✅ **Antes:** 40+ arquivos .md na raiz  
✅ **Depois:** Organizado em 4 pastas  
- `deployment/` - Railway & deploy  
- `guides/` - Tutoriais & setup  
- `docs/` - Documentação técnica  
- `scripts/` - Utilitários  

---

**Última atualização:** 23/11/2025  
**Status:** ✅ Repositório limpo e organizado

