# Railway - Configuração de Ambientes (Dev, Homologação, Produção)

## 📋 Visão Geral da Estratégia

Você terá **3 ambientes independentes no Railway**:

```
┌─────────────────┐
│   Desenvolvimento    │  (Branch: develop)
│  - Testes automáticos │  - Deploys frequentes
│  - Dados descartáveis │  - BD SQLite or PostgreSQL
└─────────────────┘
         ↓
┌─────────────────┐
│   Homologação   │  (Branch: staging)
│  - Testes E2E   │  - Antes de produção
│  - Dados reais  │  - Ambiente espelho
└─────────────────┘
         ↓
┌─────────────────┐
│   Produção      │  (Branch: main)
│  - Dados oficiais │  - Sem downtime
│  - Backup diário   │  - Alta disponibilidade
└─────────────────┘
```

## 🚀 Passo 1: Criar Projetos no Railway

### 1.1 Criar 3 Projetos Separados

No painel do Railway (https://railway.app):

1. **racket-hero-dev** (Desenvolvimento)
   - Deploy automático da branch `develop`
   - Banco de dados: PostgreSQL Dev
   - Environment variables: prefixo `DEV_`

2. **racket-hero-staging** (Homologação)
   - Deploy automático da branch `staging`
   - Banco de dados: PostgreSQL Staging
   - Environment variables: prefixo `STAGING_`

3. **racket-hero-prod** (Produção) - JÁ EXISTE
   - Deploy automático da branch `main`
   - Banco de dados: PostgreSQL Prod
   - Environment variables: prefixo `PROD_`

## 🔧 Passo 2: Configurar Branches no Git

```bash
# Branch Development (diária)
git checkout -b develop
git push -u origin develop

# Branch Staging (semanal)
git checkout -b staging
git push -u origin staging

# Branch Main (release)
# (já existe)
```

## 📝 Passo 3: Atualizar railway.toml para Cada Ambiente

Você pode usar um arquivo por ambiente ou variáveis de ambiente. **Recomendação: Usar variáveis + script de build**

### Opção A: Arquivo Único com Variáveis

```toml
[build]
builder = "nixpacks"

[build.env]
NODE_ENV = "${NODE_ENV:-production}"
PYTHONUNBUFFERED = "1"

# Backend
[[services]]
name = "backend"
startCommand = "python main.py"
root = "backend"

[services.variables]
LOG_LEVEL = "${LOG_LEVEL:-info}"
DATABASE_URL = "${DATABASE_URL}"
CORS_ORIGINS = "${CORS_ORIGINS}"
ENVIRONMENT = "${ENVIRONMENT:-production}"

# Frontend
[[services]]
name = "frontend"
startCommand = "npm start"
root = "frontend"

[services.variables]
REACT_APP_API_URL = "${REACT_APP_API_URL:-/api}"
REACT_APP_ENVIRONMENT = "${ENVIRONMENT:-production}"
```

## 🌍 Passo 4: Variáveis de Ambiente por Ambiente

### Development (racket-hero-dev)
```env
ENVIRONMENT=development
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgresql://user:pass@localhost/racket_hero_dev
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,https://racket-hero-dev.railway.app
REACT_APP_API_URL=https://racket-hero-dev.railway.app/api
BACKUP_ENABLED=false
```

### Staging (racket-hero-staging)
```env
ENVIRONMENT=staging
NODE_ENV=production
LOG_LEVEL=info
DATABASE_URL=postgresql://user:pass@localhost/racket_hero_staging
CORS_ORIGINS=https://racket-hero-staging.railway.app
REACT_APP_API_URL=https://racket-hero-staging.railway.app/api
BACKUP_ENABLED=true
```

### Production (racket-hero-prod)
```env
ENVIRONMENT=production
NODE_ENV=production
LOG_LEVEL=warn
DATABASE_URL=postgresql://user:pass@localhost/racket_hero_prod
CORS_ORIGINS=https://racket-hero.app
REACT_APP_API_URL=https://racket-hero.app/api
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
```

## 🔄 Passo 5: GitHub Workflows para Deploy Automático

### .github/workflows/deploy-dev.yml
```yaml
name: Deploy Dev

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway Dev
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_DEV }}
        run: |
          npm install -g @railway/cli
          railway up --service backend --service frontend \
            --environment development \
            --project racket-hero-dev
      
      - name: Run E2E Tests
        run: |
          npm install -g playwright
          npx playwright install
          npx playwright test --config=playwright.config.dev.js
```

### .github/workflows/deploy-staging.yml
```yaml
name: Deploy Staging

on:
  push:
    branches: [staging]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Run Tests
        run: |
          cd frontend && npm install && npm test
          cd ../backend && pip install -r requirements.txt && pytest
      
      - name: Deploy to Railway Staging
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_STAGING }}
        run: |
          npm install -g @railway/cli
          railway up --service backend --service frontend \
            --environment staging \
            --project racket-hero-staging
      
      - name: Smoke Tests
        run: |
          curl -f https://racket-hero-staging.railway.app/health
```

### .github/workflows/deploy-prod.yml
```yaml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Backup
        env:
          DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
        run: |
          python backend/backup_manager.py --create
      
      - name: Deploy to Railway Production
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN_PROD }}
        run: |
          npm install -g @railway/cli
          railway up --service backend --service frontend \
            --environment production \
            --project racket-hero-prod \
            --no-cache
      
      - name: Health Check
        run: |
          for i in {1..5}; do
            curl -f https://racket-hero.app/health && break
            sleep 10
          done
      
      - name: Notify Slack
        if: success()
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"text":"✅ Production deployment successful"}'
```

## 📊 Passo 6: Configuração de Banco de Dados

### PostgreSQL por Ambiente

**Development**:
- Pode ser PostgreSQL local ou Railway
- 1 réplica
- Sem backup automático (dados descartáveis)

**Staging**:
- PostgreSQL Railway
- Espelho de produção
- Backup diário (7 dias retenção)

**Production**:
- PostgreSQL Railway com HA
- Backup diário (30 dias)
- Replicação master-slave
- Point-in-time recovery ativado

### Migração de BD entre Ambientes

```bash
# Copiar estrutura prod → staging
pg_dump -s $PROD_DB | psql $STAGING_DB

# Copiar dados anônimos (com anonymizer)
# backend/scripts/copy_db_anon.py
```

## ✅ Passo 7: Checklist de Implementação

### Semana 1: Setup Básico
- [ ] Criar 3 projetos no Railway
- [ ] Criar branches (develop, staging)
- [ ] Adicionar RAILWAY_TOKEN como secrets no GitHub
- [ ] Configurar variáveis de ambiente em cada projeto

### Semana 2: GitHub Actions
- [ ] Criar workflows de deploy automático
- [ ] Testar deploy dev → staging → prod
- [ ] Validar healthchecks funcionam

### Semana 3: Testes
- [ ] Escrever testes E2E para staging
- [ ] Setup Playwright com CI/CD
- [ ] Documentar processo de testes

### Semana 4: Monitoramento
- [ ] Setup logs centralizados (Datadog/LogRocket)
- [ ] Alertas de downtime
- [ ] Dashboard de performance

## 📈 Fluxo de Desenvolvimento Recomendado

```
Feature Branch
    ↓
git push → GitHub Actions
    ↓
Tests & Lint
    ↓
Merge to develop
    ↓
Auto Deploy Dev
    ↓
Manual Testing
    ↓
Create Pull Request → staging
    ↓
Auto Deploy Staging
    ↓
E2E Tests & Validation
    ↓
Code Review & Approval
    ↓
Merge to main
    ↓
Auto Deploy Production
    ↓
Health Check & Monitoring
```

## 🔐 Secrets Necessários

Adicionar no GitHub (Settings → Secrets):

```
RAILWAY_TOKEN_DEV
RAILWAY_TOKEN_STAGING
RAILWAY_TOKEN_PROD
PROD_DATABASE_URL
SLACK_WEBHOOK (opcional)
SENTRY_DSN (opcional, para error tracking)
```

## 🆘 Troubleshooting

### Deploy lento?
- Use `--no-cache` apenas em produção
- Otimize node_modules com `npm ci --omit=dev`

### Build falha?
- Verifique `railway logs --service backend`
- Valide variáveis de ambiente estão todas presentes

### Teste fails no staging?
- Use dados reais anônimos
- Execute seeds de teste antes de E2E
- Mock APIs externas se necessário

## 📚 Referências

- Railway Docs: https://docs.railway.app
- GitHub Actions: https://docs.github.com/en/actions
- Playwright: https://playwright.dev/docs/ci
