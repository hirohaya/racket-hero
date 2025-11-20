# Implementação de Ambientes no Railway

## 📋 Resumo Executivo

Você terá **3 ambientes isolados**:

| Ambiente | Branch | URL | Propósito |
|----------|--------|-----|----------|
| **Development** | `develop` | `racket-hero-dev.railway.app` | Testes frequentes e bugs |
| **Staging** | `staging` | `racket-hero-staging.railway.app` | Validação antes de produção |
| **Production** | `main` | `racket-hero.app` | Usuários reais |

---

## ✅ Checklist de Implementação

### Fase 1: Preparação (1-2 horas)

- [ ] **1.1** Criar branches locais
  ```bash
  git checkout -b develop
  git push -u origin develop
  
  git checkout -b staging
  git push -u origin staging
  ```

- [ ] **1.2** Criar 2 novos projetos no Railway
  - Acesse https://railway.app/dashboard
  - Clique "New Project" → "Empty Project"
  - Crie: **racket-hero-dev** e **racket-hero-staging**

- [ ] **1.3** Conectar repositório GitHub
  - Para cada projeto Railway:
    1. Settings → GitHub Repo
    2. Selecione `hirohaya/racket-hero`
    3. Configure branch automática (dev → develop, staging → staging)

---

### Fase 2: Configuração de Secrets (30 min)

**No GitHub** (Settings → Secrets → Actions):

```
RAILWAY_TOKEN_DEV       ← Token do projeto dev
RAILWAY_TOKEN_STAGING   ← Token do projeto staging
RAILWAY_TOKEN_PROD      ← Token do projeto prod (existente)
```

**Como obter Railway tokens:**
1. Railway Dashboard → Project Settings
2. API Token
3. Copiar e colar como secret no GitHub

**No Railway** (cada projeto → Variables):

```
# Todas os projetos
ENVIRONMENT=dev/staging/production
NODE_ENV=development/production
PYTHONUNBUFFERED=1

# Backend
LOG_LEVEL=debug/info/warn
DATABASE_URL=postgresql://...
CORS_ORIGINS=https://...,http://...

# Frontend
REACT_APP_API_URL=https://racket-hero-{env}.railway.app/api
REACT_APP_ENVIRONMENT=dev/staging/production
```

---

### Fase 3: GitHub Actions (30 min)

**Os workflows já foram criados em:**
- `.github/workflows/deploy-dev.yml` ← Automático ao push em `develop`
- `.github/workflows/deploy-staging.yml` ← Automático ao push em `staging`
- `.github/workflows/deploy-prod.yml` ← Automático ao push em `main`

**Testar workflows:**
```bash
# Fazer um commit na branch develop
git checkout develop
git commit --allow-empty -m "test: trigger dev workflow"
git push

# Verificar em GitHub Actions
# https://github.com/hirohaya/racket-hero/actions
```

---

### Fase 4: Teste de Deploy (1 hora)

#### 4.1 Deploy Development
```bash
# Criar arquivo de teste
git checkout develop
echo "# Dev test" >> README.md
git add README.md
git commit -m "test: dev environment"
git push

# Acompanhar em:
# - GitHub Actions: https://github.com/hirohaya/racket-hero/actions
# - Railway Dev: https://railway.app/project/...
```

**Esperado:**
- ✅ Workflow inicia automaticamente
- ✅ Backend compila e inicia
- ✅ Frontend compila
- ✅ Tests rodam
- ✅ Deploy bem-sucedido

#### 4.2 Deploy Staging
```bash
# Rebase develop em staging
git checkout staging
git pull origin main
git rebase develop
git push
```

**Esperado:**
- ✅ Workflow roda testes completos
- ✅ E2E tests executam
- ✅ Deploy sem downtime
- ✅ PR comentada com resultados

#### 4.3 Production (quando pronto)
```bash
git checkout main
git pull origin staging
git push
```

---

## 🏗️ Fluxo de Desenvolvimento

```
Você cria feature branch
    ↓
git push → Testa localmente
    ↓
PRs em develop → GitHub Actions roda testes
    ↓
Merge → Auto deploy em dev.railway.app
    ↓
Manual teste em staging (1-2 dias)
    ↓
PRs em staging → Testes E2E completos
    ↓
Merge → Auto deploy em staging.railway.app
    ↓
Validação final
    ↓
PRs em main → Testes + Backup automático
    ↓
Merge → Auto deploy em prod.railway.app
    ↓
Monitoramento contínuo
```

---

## 🗄️ Gerenciamento de Banco de Dados

### Separação por Ambiente

```
Development:
├── Dados: SQLite local (descartáveis)
├── Reset: Diário (automático via script)
└── Backup: Não necessário

Staging:
├── Dados: PostgreSQL Railway (anônimos)
├── Reset: Semanal com dados de prod anônimos
└── Backup: Diário (7 dias)

Production:
├── Dados: PostgreSQL Railway HA (oficiais)
├── Reset: Nunca!
└── Backup: Diário (30 dias)
```

### Copiar dados (Prod → Staging)

```bash
# 1. Fazer backup de produção
cd backend
python backup_manager.py --create

# 2. Anonimizar dados sensíveis
python scripts/anonymize_db.py

# 3. Restaurar em staging
psql $STAGING_DATABASE_URL < backup.sql
```

---

## 📊 Monitoramento

### Verificações Automáticas

Cada deploy verifica:
- ✅ Health endpoint (`/health`)
- ✅ API responsividade
- ✅ Frontend carregamento
- ✅ Conectividade BD
- ✅ Logs para erros

### Dashboard Recomendado

Integrar com:
- **Datadog**: Logs centralizados
- **Sentry**: Error tracking
- **UptimeRobot**: Monitoramento 24/7
- **PagerDuty**: On-call alertas

---

## 🚨 Troubleshooting

### Deploy falha em staging
```
❌ Symptom: Workflow cancela
✅ Solution:
  1. Verificar: GitHub Actions logs
  2. Verificar: Railway build logs
  3. Verificar: Variables estão todas presentes
  4. Re-trigger: GitHub Actions
```

### Teste E2E falha
```
❌ Symptom: Teste falha em staging mas não em dev
✅ Solution:
  1. Verificar: URLs estão corretas (https://... não http)
  2. Verificar: Dados de seed existem
  3. Rerun tests manualmente
  4. Screenshot/video salvo em artifacts
```

### Banco de dados quebrado
```
❌ Symptom: Erro SQL ao conectar
✅ Solution:
  1. Verificar: DATABASE_URL válida
  2. Verificar: Conexão network (Railway)
  3. Restaurar from backup:
     psql $DB_URL < backup.sql
  4. Re-migrar: python -m alembic upgrade head
```

---

## 📈 Próximos Passos (Semana 2)

1. **Integração Contínua Melhorada**
   - [ ] SonarQube para qualidade de código
   - [ ] Snyk para vulnerabilidades
   - [ ] Performance tests

2. **Monitoramento**
   - [ ] Setup Datadog/LogRocket
   - [ ] Alertas Slack/Email
   - [ ] Dashboard de performance

3. **Documentação**
   - [ ] Runbook de deploy
   - [ ] Procedure de rollback
   - [ ] Disaster recovery plan

4. **Otimização**
   - [ ] Cache de dependências
   - [ ] Parallel tests
   - [ ] Blue-green deployments

---

## 📚 Referências Rápidas

| Recurso | Link |
|---------|------|
| Railway Docs | https://docs.railway.app |
| GitHub Actions | https://docs.github.com/en/actions |
| Playwright | https://playwright.dev/docs/ci |
| Railway CLI | `npm install -g @railway/cli` |

---

## 💬 FAQ

**P: Quanto custa ter 3 ambientes no Railway?**
A: Aproximadamente $5-10/mês por projeto. Railway é grátis até $5, depois cobra por uso.

**P: Posso resetar o banco de staging sem afetar produção?**
A: Sim! Cada ambiente tem seu próprio banco isolado.

**P: Quanto tempo leva um deploy?**
A: ~5 min (dev), ~10 min (staging com tests), ~15 min (prod com backup).

**P: E se o deploy falhar em produção?**
A: Rollback automático para versão anterior. Verifique Railway Dashboard.

---

**Status**: ✅ Pronto para implementar
**Próximo**: Execute Fase 1 (criar branches e projetos)
