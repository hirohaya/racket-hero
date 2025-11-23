# 🎯 Railway Multi-Environment: Passo-a-Passo

## Parte 1: Preparação (15 min)

### Passo 1.1: Criar branches locais

```bash
# 1. Criar branch develop
git checkout -b develop
git push -u origin develop

# 2. Criar branch staging
git checkout -b staging
git push -u origin staging

# 3. Verificar branches
git branch -a
```

**Expected Output:**
```
  develop
  main
* staging
  remotes/origin/develop
  remotes/origin/main
  remotes/origin/staging
```

---

### Passo 1.2: Criar 2 novos projetos no Railway

**Acesso**: https://railway.app/dashboard

**Criar Projeto 1: Development**
1. Click "New Project" → "Empty Project"
2. Name: `racket-hero-dev`
3. Confirm

**Criar Projeto 2: Staging**
1. Click "New Project" → "Empty Project"
2. Name: `racket-hero-staging`
3. Confirm

**Você deve ter 3 projetos agora:**
```
✅ racket-hero (existing - production)
✅ racket-hero-dev (new)
✅ racket-hero-staging (new)
```

---

## Parte 2: Configuração do GitHub (30 min)

### Passo 2.1: Obter Railway API Tokens

**Para cada projeto Railway** (dev, staging, prod):

1. Abrir projeto Railway
2. Settings → API Token
3. Copy token (starts with `sk_live_...`)
4. Guardar em local seguro (notepad temporário)

**Exemplo:**
```
racket-hero-dev      → sk_live_abc123...
racket-hero-staging  → sk_live_def456...
racket-hero (prod)   → sk_live_ghi789... (já existe)
```

---

### Passo 2.2: Adicionar Secrets no GitHub

**Acesso**: https://github.com/hirohaya/racket-hero/settings/secrets/actions

Click "New repository secret" para cada um:

1️⃣ **RAILWAY_TOKEN_DEV**
   - Value: `sk_live_abc123...` (do dev project)
   - Click "Add secret"

2️⃣ **RAILWAY_TOKEN_STAGING**
   - Value: `sk_live_def456...` (do staging project)
   - Click "Add secret"

3️⃣ **RAILWAY_TOKEN_PROD**
   - Value: `sk_live_ghi789...` (já existe - verificar)
   - Se não existe, adicionar

4️⃣ **PROD_DATABASE_URL** (opcional - para backups)
   - Value: `postgresql://user:pass@...`
   - Click "Add secret"

**Verificar:**
```
✅ RAILWAY_TOKEN_DEV
✅ RAILWAY_TOKEN_STAGING
✅ RAILWAY_TOKEN_PROD
✅ PROD_DATABASE_URL
```

---

## Parte 3: Configuração no Railway (45 min)

### Passo 3.1: Conectar GitHub Repo (Dev)

1. Abrir projeto `racket-hero-dev` no Railway
2. Click "New" → "GitHub Repo"
3. Select: `hirohaya/racket-hero`
4. Click "Deploy"

**Railway agora vai:**
- Clonar o repositório
- Detectar Dockerfile
- Compilar imagem
- **FALHAR** (sem variáveis de ambiente)

Isso é esperado! Continue com o próximo passo.

---

### Passo 3.2: Configurar Variáveis de Ambiente (Dev)

Railway Project → Settings → Variables

Adicione cada variável:

```
ENVIRONMENT = development
NODE_ENV = development
LOG_LEVEL = debug
PYTHONUNBUFFERED = 1
CORS_ORIGINS = http://localhost:3000,http://localhost:8000
REACT_APP_API_URL = http://localhost:8000/api
REACT_APP_ENVIRONMENT = development
```

**No Railway UI:**
1. Click "New Variable"
2. Key: `ENVIRONMENT`
3. Value: `development`
4. Click "Add"
5. Repeat para todas as variáveis acima

---

### Passo 3.3: Configurar Database Connection (Dev)

```
DATABASE_URL = sqlite:///./racket_hero_dev.db
```

**Ou se usar PostgreSQL local:**
```
DATABASE_URL = postgresql://user:password@localhost:5432/racket_hero_dev
```

---

### Passo 3.4: Conectar GitHub Repo (Staging)

1. Abrir projeto `racket-hero-staging` no Railway
2. Click "New" → "GitHub Repo"
3. Select: `hirohaya/racket-hero`
4. Esperar compilação

---

### Passo 3.5: Configurar Variáveis (Staging)

```
ENVIRONMENT = staging
NODE_ENV = production
LOG_LEVEL = info
PYTHONUNBUFFERED = 1
CORS_ORIGINS = https://racket-hero-staging.railway.app
REACT_APP_API_URL = https://racket-hero-staging.railway.app/api
REACT_APP_ENVIRONMENT = staging
DATABASE_URL = postgresql://... (Railroad PostgreSQL)
```

---

### Passo 3.6: Configurar Produção (Upgrade Existente)

1. Abrir projeto `racket-hero` (production)
2. Settings → Variables
3. Verificar/atualizar:

```
ENVIRONMENT = production
NODE_ENV = production
LOG_LEVEL = warn
PYTHONUNBUFFERED = 1
CORS_ORIGINS = https://racket-hero.app
REACT_APP_API_URL = https://racket-hero.app/api
REACT_APP_ENVIRONMENT = production
```

---

## Parte 4: Configurar Workflows (15 min)

Os workflows GitHub Actions já foram criados em:
- `.github/workflows/deploy-dev.yml`
- `.github/workflows/deploy-staging.yml`
- `.github/workflows/deploy-prod.yml`

**Verificar se arquivos existem:**
```bash
ls -la .github/workflows/deploy-*.yml
```

---

## Parte 5: Primeiro Deploy (30 min)

### Passo 5.1: Testar Deploy em Development

```bash
# Mudar para branch develop
git checkout develop

# Criar commit de teste
git commit --allow-empty -m "test: trigger dev workflow"

# Push
git push origin develop
```

**Acompanhar:**
1. GitHub: https://github.com/hirohaya/racket-hero/actions
2. Procurar workflow "Deploy Development"
3. Ver status em tempo real

**Esperado:**
```
✅ Setup Node.js
✅ Setup Python
✅ Install dependencies
✅ Lint code
✅ Run tests
✅ Build frontend
✅ Deploy to Railway
✅ Health check
```

**Se falhar:**
- Click no job que falhou
- Ler os logs
- Comum: Variáveis de ambiente faltando
- Solution: Voltar ao Passo 3.2

---

### Passo 5.2: Verificar Deploy (Railway)

1. Abrir projeto `racket-hero-dev`
2. Clicar no serviço "app"
3. Ver build logs
4. Esperar até ver: "Ready on ..."
5. Copiar URL (ex: `https://racket-hero-dev-production.up.railway.app`)

**Acessar:**
```
Backend: https://racket-hero-dev-production.up.railway.app
Frontend: https://racket-hero-dev-production.up.railway.app/
API: https://racket-hero-dev-production.up.railway.app/api
```

---

### Passo 5.3: Testar Deploy em Staging

```bash
# Mudar para branch staging
git checkout staging

# Criar commit de teste
git commit --allow-empty -m "test: trigger staging workflow"

# Push
git push origin staging
```

**Acompanhar:**
1. GitHub Actions → Workflow "Deploy Staging"
2. Esperar testes completos (~30 min)

---

### Passo 5.4: Testar Deploy em Produção

⚠️ **CUIDADO!** Este é seu ambiente de produção!

```bash
# Mudar para branch main
git checkout main

# Criar commit de teste
git commit --allow-empty -m "test: trigger prod workflow"

# Push
git push origin main
```

**Acompanhar:**
1. GitHub Actions → Workflow "Deploy Production"
2. Railway production project
3. Verificar health check

---

## Parte 6: Validação (20 min)

### Checklist Final

```
Development (dev)
  ✅ GitHub Actions workflow executa
  ✅ Build bem-sucedido
  ✅ Health endpoint responde
  ✅ Frontend carrega
  
Staging
  ✅ Tests passam (unit + E2E)
  ✅ Build bem-sucedido
  ✅ Health checks passam
  ✅ Smoke tests rodam
  
Production
  ✅ Backup criado antes do deploy
  ✅ Build bem-sucedido
  ✅ Zero downtime deployment
  ✅ Health checks passam
  ✅ Application funcionando
```

---

## Parte 7: Integração Contínua (Opcional)

### Adicionar Notificações Slack

1. Criar Slack Webhook:
   - Slack App Admin → Webhooks
   - Create new webhook
   - Copy URL: `https://hooks.slack.com/services/...`

2. Adicionar secret no GitHub:
   - Settings → Secrets
   - Name: `SLACK_WEBHOOK_URL`
   - Value: URL copiada

3. Workflows já têm notificações! 🎉

---

## Diagrama Visual Final

```
┌─────────────────────────────────────┐
│     GitHub Repository               │
│   (hirohaya/racket-hero)            │
│                                     │
│  develop    staging    main         │
└──────┬──────────┬──────────┬────────┘
       │          │          │
       ▼          ▼          ▼
   [Workflow]  [Workflow]  [Workflow]
   deploy-dev  deploy-stg  deploy-prod
       │          │          │
       ▼          ▼          ▼
   ┌─────────┬──────────┬──────────────┐
   │  Railway│ Railway  │  Railway     │
   │   DEV   │ STAGING  │  PROD (HA)   │
   └─────────┴──────────┴──────────────┘
       ↓           ↓            ↓
   :3000       staging.app   racket-hero.app
```

---

## Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Workflow falha na linha 1 | Verifique se RAILWAY_TOKEN_ secrets existem |
| Deploy falha com erro BD | DATABASE_URL inválida ou BD não acessível |
| Frontend não encontra API | REACT_APP_API_URL incorreta |
| Health check timeout | Espere mais tempo, Railway pode ser lento |
| Rollback automático | Verifique logs no Railway → Deployments |

---

## 🎉 Sucesso!

Se chegou aqui e todos os checks passaram:

```
✅ 3 ambientes isolados configurados
✅ CI/CD pipelines automáticas
✅ GitHub Actions integradadoswith Railway
✅ Testes rodam automaticamente
✅ Deploys sem downtime
```

**Próximos passos recomendados:**
1. Setup Sentry para error tracking
2. Setup Datadog para logs centralizados
3. Criar runbook de rollback
4. Documentar procedures de deploy

---

**Status**: ✅ Implementação Completa
**Tempo Total**: ~2-3 horas
**Próximo**: Integrar monitoramento (Sentry/Datadog)
