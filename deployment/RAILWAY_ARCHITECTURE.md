# 🚀 Railway Multi-Environment Setup - Resumo Visual

## Arquitetura Completa

```
┌────────────────────────────────────────────────────────────────┐
│                     GIT REPOSITORY                              │
│                   (hirohaya/racket-hero)                       │
└────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┼─────────┐
                    │         │         │
              [develop]  [staging]   [main]
                    │         │         │
        ┌───────────▼──┐ ┌───▼──────┐ ┌▼────────────┐
        │   GitHub     │ │ GitHub   │ │  GitHub    │
        │  Actions     │ │ Actions  │ │  Actions   │
        │ (deploy-dev) │ │ (staging)│ │ (deploy-prod)
        └───────┬──────┘ └────┬─────┘ └────┬───────┘
                │              │            │
        ┌───────▼──────┐ ┌────▼─────┐ ┌───▼────────┐
        │  RAILWAY     │ │ RAILWAY  │ │  RAILWAY   │
        │   PROJECT    │ │ PROJECT  │ │  PROJECT   │
        │ (racket-hero │ │(racket-  │ │(racket-hero│
        │     -dev)    │ │ hero-    │ │   -prod)   │
        │              │ │staging)  │ │            │
        └───────┬──────┘ └────┬─────┘ └───┬────────┘
                │              │            │
        ┌───────▼──────┐ ┌────▼─────┐ ┌───▼────────┐
        │   Backend    │ │ Backend  │ │  Backend   │
        │   Frontend   │ │ Frontend │ │  Frontend  │
        │ PostgreSQL   │ │PostgreSQL│ │ PostgreSQL │
        │     (Dev)    │ │(Staging) │ │  (Prod HA) │
        └──────────────┘ └──────────┘ └────────────┘
                │              │            │
              ↓              ↓            ↓
        localhost:3000  staging.app   racket-hero.app
        localhost:8000  staging/api   /api
```

---

## Fluxo de Deploy Automático

```
Developer Push
    ↓
    ├─→ [develop] ──────────────────────────────────┐
    │                                                │
    ├─→ [staging] ──────────────────────────────────┼──→ GitHub Actions
    │                                                │   (Test Suite)
    └─→ [main] ─────────────────────────────────────┤
                                                     │
                                        ┌────────────▼──────────────┐
                                        │  Run Tests                 │
                                        │  - Backend: pytest         │
                                        │  - Frontend: jest          │
                                        │  - Lint: ESLint + Pylint   │
                                        └────────┬───────┬──────┬───┘
                                                 │       │      │
                                    ┌────────────▼───┐   │      │
                                    │  Build & Push  │   │      │
                                    │  Docker Image  │   │      │
                                    └────────┬───────┘   │      │
                                             │           │      │
                               ┌─────────────▼───────────▼──┐   │
                               │    Deploy to Railway       │   │
                               │  - Backend service         │   │
                               │  - Frontend service        │   │
                               │  - Environment variables   │   │
                               └─────────────┬──────────────┘   │
                                             │                  │
                         ┌───────────────────▼──┐               │
                         │  Health Checks        │               │
                         │  - API /health        │               │
                         │  - Frontend /         │               │
                         │  - Database ping      │               │
                         └───────────┬───────────┘               │
                                     │                          │
                        ┌────────────▼──────────┐               │
                        │  Smoke Tests          │               │
                        │  [staging+prod only]  │               │
                        │  - E2E validation     │               │
                        └────────┬───────────────┘               │
                                 │                              │
                 ┌───────────────▼──────────────┐               │
                 │  ✅ Deployment Successful    │               │
                 │                              │               │
                 │  [dev]       [staging]       │               │
                 │  auto-deploy auto+tests      │               │
                 │  (15 min)    (30 min)        │               │
                 └──────────────────────────────┘               │
                                                                 │
                                                      ┌──────────▼────────┐
                                                      │  ⚠️ Production     │
                                                      │  Manual Approval   │
                                                      │                    │
                                                      │  Merge to main only│
                                                      │  when ready!       │
                                                      └────────────────────┘
```

---

## Ambientes Comparados

| Aspecto | Development | Staging | Production |
|---------|-------------|---------|-----------|
| **Branch** | `develop` | `staging` | `main` |
| **URL** | localhost:3000 | staging.railway.app | racket-hero.app |
| **BD** | SQLite/Local | PostgreSQL | PostgreSQL HA |
| **Auto Deploy** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Testes** | Básicos | Completos+E2E | Completos+Smoke |
| **Dados** | Descartáveis | Anônimos | Oficiais |
| **Backup** | ❌ Não | ✅ 7 dias | ✅ 30 dias |
| **Retenção** | 1 dia | 7 dias | 30 dias |
| **SLA** | N/A | 99% | 99.9% |
| **Escala** | 1 instância | 1-2 instâncias | 2+ instâncias HA |

---

## CI/CD Pipeline Detalhado

```
┌─────────────────────────────────────┐
│ 1. Code Push (develop/staging/main)  │
└────────────┬────────────────────────┘
             │
┌────────────▼─────────────────────────┐
│ 2. GitHub Actions Triggered           │
│    - Checkout code                    │
│    - Setup Node.js + Python           │
│    - Cache dependencies               │
└────────────┬─────────────────────────┘
             │
┌────────────▼──────────────────────────┐
│ 3. Quality & Security Checks           │
│    ├─ Lint (ESLint + Black)            │
│    ├─ Security (Bandit + npm audit)    │
│    └─ Type checking (TypeScript)       │
└────────────┬──────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│ 4. Unit Tests                            │
│    ├─ Backend: pytest (coverage > 70%)   │
│    ├─ Frontend: jest (coverage > 70%)    │
│    └─ Fail-fast on errors                │
└────────────┬────────────────────────────┘
             │
┌────────────▼──────────────────────────────┐
│ 5. Build Artifacts                        │
│    ├─ Backend: Docker image                │
│    ├─ Frontend: React production build     │
│    └─ Push to container registry (optional)│
└────────────┬──────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 6. Deploy to Railway                        │
│    ├─ Set environment variables              │
│    ├─ Run migrations (if any)                │
│    ├─ Deploy backend service                 │
│    └─ Deploy frontend service                │
└────────────┬────────────────────────────────┘
             │
┌────────────▼───────────────────────────────────┐
│ 7. Post-Deploy Validation                      │
│    ├─ Health check (30s timeout)               │
│    ├─ Connectivity check                       │
│    ├─ Database integrity check (prod only)     │
│    └─ SSL/TLS certificate validation           │
└────────────┬───────────────────────────────────┘
             │
     ┌───────┴───────┐
     │ staging/prod? │
     └───┬───────┬──┘
         │       │
         ✅      ❌
         │       │
    [Continue]  [Rollback]
```

---

## Estrutura de Secrets

```
GitHub Repository Settings → Secrets & variables → Actions

RAILWAY_TOKEN_DEV        = sk_live_xxx... (dev project)
RAILWAY_TOKEN_STAGING    = sk_live_xxx... (staging project)
RAILWAY_TOKEN_PROD       = sk_live_xxx... (prod project)
PROD_DATABASE_URL        = postgresql://... (for backups)
SLACK_WEBHOOK_URL        = https://hooks.slack.com/... (notifications)
SENTRY_DSN              = https://xxx@sentry.io/... (error tracking)
```

---

## Rollback Automático

```
Deploy Falha em Produção?
         │
         ▼
    Health Check Error
         │
         ▼
    ❌ Smoke Test Failed
         │
         ▼
    🔄 Automatic Rollback
         │
         ├─→ Revert to previous version
         ├─→ Restart services
         ├─→ Verify health
         └─→ Notify team via Slack
```

---

## Timeline de Deploy

```
develop → dev.railway.app
├─ Setup: 1 min
├─ Install: 2 min
├─ Build: 3 min
├─ Deploy: 5 min
├─ Tests: 2 min
└─ Total: ~13 minutes

staging → staging.railway.app  
├─ Setup: 1 min
├─ Tests: 10 min (unit + integration)
├─ Build: 3 min
├─ Deploy: 5 min
├─ Smoke Tests: 10 min (E2E)
└─ Total: ~29 minutes

main → racket-hero.app
├─ Backup: 2 min
├─ Tests: 10 min
├─ Build: 3 min
├─ Deploy: 5 min
├─ Smoke Tests: 5 min
└─ Total: ~25 minutes
```

---

## Monitoramento & Alertas

```
┌─────────────────────┐
│   Application       │
│  Running on         │
│  Railway            │
└──────────┬──────────┘
           │
    ┌──────┴────────┐
    │               │
    ▼               ▼
  Logs         Metrics
    │               │
    ├─→ Datadog ←──┤
    │               │
    └─→ Error Check─┘
            │
    ┌───────┴─────────┐
    │                 │
    ▼ (if error)      ▼ (if metric spike)
  Sentry         PagerDuty
    │                 │
    └────────┬────────┘
             │
             ▼
        Slack Alert
             │
             ▼
      Team Notified!
```

---

## Próximas Implementações (Roadmap)

```
✅ Phase 1 (Agora)
  - Multi-environment setup
  - GitHub Actions workflows
  - Auto-deploy pipelines

⏳ Phase 2 (Próximas 2 semanas)
  - Centralized logging (Datadog)
  - Error tracking (Sentry)
  - Performance monitoring

📋 Phase 3 (Próximo mês)
  - Database backup automation
  - Disaster recovery procedures
  - Load testing framework

🔮 Phase 4 (Future)
  - Canary deployments
  - Blue-green deployments
  - Advanced monitoring & SLOs
```

---

## Quick Commands

```bash
# Setup inicial
git checkout -b develop && git push -u origin develop
git checkout -b staging && git push -u origin staging

# Deploy para dev
git commit --allow-empty -m "deploy: dev"
git push origin develop

# Deploy para staging
git commit --allow-empty -m "deploy: staging"
git push origin staging

# Deploy para produção
git commit --allow-empty -m "release: v1.0.0"
git push origin main

# Ver logs no Railway
railway logs --service backend --follow

# Trigger manual de workflow
gh workflow run deploy-staging.yml --ref staging
```

---

## 📞 Suporte

- Railway Docs: https://docs.railway.app
- GitHub Actions: https://docs.github.com/en/actions
- Debug Workflows: View "Action" tab no GitHub

---

**Status**: ✅ Ready to Implement
**Próximo Passo**: Create branches & Railway projects
