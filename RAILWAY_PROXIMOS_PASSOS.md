# 🚀 Railway Setup Completo - Próximos Passos

**Data:** 19 de Novembro, 2025  
**Status:** ✅ Projeto pronto para Railway  
**Tempo estimado para deploy:** 15 minutos  

---

## 📋 O que foi criado

Sua aplicação Racket Hero foi configurada para funcionar no Railway. Aqui estão os arquivos criados:

### ✅ Arquivos de Configuração Railway
- **`railway.toml`** - Configuração principal do Railway
  - Define como detectar backend e frontend
  - Configura healthchecks automáticos
  - Detecta portas automaticamente

- **`Procfile`** - Comandos de start
  - Backend: `cd backend && python main.py`
  - Frontend: `cd frontend && npm start`

- **`.env.railway`** - Variáveis de ambiente
  - Todas as configurações necessárias
  - Pronto para usar no Railway dashboard

### ✅ Documentação e Scripts
- **`RAILWAY_SETUP.md`** - Guia de configuração local
- **`DEPLOY_RAILWAY_COMPLETO.md`** - Guia completo de deployment
- **`scripts/validate_railway_setup.py`** - Validação do projeto
- **`scripts/init_railway_db.py`** - Inicialização de database

---

## 🎯 Próximas Ações (15 minutos)

### ✅ Passo 1: Committar Configurações (1 min)

```powershell
cd c:\Users\hiros\OneDrive\Documents\projetos\racket-hero

# Adicionar todos os arquivos
git add railway.toml Procfile .env.railway RAILWAY_SETUP.md

# Committar
git commit -m "Feat: Configure Railway deployment"

# Enviar para GitHub
git push origin main
```

**Verifique no terminal:**
```
[main 12ab34cd] Feat: Configure Railway deployment
 4 files changed, 150 insertions(+)
```

---

### 🔑 Passo 2: Criar Conta Railway (3 min)

1. Abra: https://railway.app
2. Clique em **"Start Coding Now"** (canto superior direito)
3. Selecione **"Continue with GitHub"**
4. Autorize Railway a acessar seu GitHub:
   - Clique **"Authorize Railway"**
   - Confirme senha do GitHub se pedido

**Você será redirecionado para o dashboard Railway** ✅

---

### 📦 Passo 3: Importar Repositório (2 min)

1. No **Dashboard Railway**, clique **"Import from GitHub"** (ou New Project)
2. Uma popup abre com seus repositórios
3. **Procure por `racket-hero`** e clique nele
4. Clique **"Select Repository"**

**Railway agora tem acesso ao seu código** ✅

---

### 🔧 Passo 4: Railway Detecta Serviços Automaticamente (3 min)

Railway lerá seu `railway.toml` e criará automaticamente:

```
┌─────────────────────────────────┐
│ ✅ Backend Service              │
│    (FastAPI na porta detectada) │
├─────────────────────────────────┤
│ ✅ Frontend Service             │
│    (React na porta 3000)        │
└─────────────────────────────────┘
```

**No dashboard, você verá algo como:**
```
racket-hero
├─ backend (detectado automaticamente)
└─ frontend (detectado automaticamente)
```

Se aparecer um botão **"Deploy"**, clique-o. Caso contrário, vá para o próximo passo.

---

### ⚙️ Passo 5: Configurar Variáveis de Ambiente (3 min)

Railway irá gerar URLs públicas assim que começar o build:
- Backend: `https://seu-backend-random.railway.app`
- Frontend: `https://seu-frontend-random.railway.app`

**Para cada serviço (backend e frontend):**

1. Clique no serviço no dashboard
2. Abra a aba **"Variables"** (ou **"Env"**)
3. Adicione as variáveis:

#### Backend Variables:
```
ENVIRONMENT=production
LOG_LEVEL=INFO
DATABASE_URL=sqlite:///./racket_hero.db
CORS_ORIGINS=["https://seu-frontend-random.railway.app"]
SECRET_KEY=(veja instruções abaixo)
ALGORITHM=HS256
```

#### Para gerar SECRET_KEY seguro:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copie o resultado e cole em `SECRET_KEY`

#### Frontend Variables:
```
REACT_APP_API_URL=https://seu-backend-random.railway.app
NODE_ENV=production
```

---

### 🚀 Passo 6: Deploy Automático (1 min)

Railway começará o build automaticamente quando você:

**Opção A: Ao importar repositório**
- Se clicou "Deploy", vai começar agora

**Opção B: Ao fazer push para GitHub**
- Qualquer push para `main` dispara novo deploy
- Isso já foi feito no Passo 1 ✅

**O que esperar:**
```
Building... (2-3 min)
  ✓ Backend build
  ✓ Frontend build
  
Deploying... (1-2 min)
  ✓ Backend iniciado
  ✓ Frontend iniciado
  
Status: ✅ RUNNING
```

---

### ✅ Passo 7: Validar Deployment (2 min)

#### Testar Backend Health:
```powershell
# Substitua pela URL do seu backend (Railway mostra isso)
Invoke-WebRequest -Uri "https://seu-backend-random.railway.app/health" -UseBasicParsing | Select-Object StatusCode, @{Name="Body";Expression={$_.Content}}
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "message": "API is healthy",
  "timestamp": "2025-11-19T20:00:00.000Z"
}
```

#### Testar Frontend:
1. Abra no navegador: `https://seu-frontend-random.railway.app`
2. Você deve ver a página de login do Racket Hero
3. Se vê branco ou erro, cheque os logs (veja Troubleshooting)

#### Testar Criação de Conta:
1. Clique **"Sign Up"** (ou **"Create Account"**)
2. Preencha:
   - Email: `teste@email.com`
   - Password: `SenhaTest123!`
3. Clique **"Create Account"**
4. Você deve ser redirecionado para login
5. Faça login com as credenciais criadas
6. Clique **"New Event"** ou **"Create Tournament"**
7. Preencha um evento de teste
8. Clique **"Create"**

**Se tudo funciona, seu app está em produção!** 🎉

---

## 🎯 URLs Finais

Após deploy bem-sucedido, você terá:

```
Backend API:
  https://seu-backend-random.railway.app
  https://seu-backend-random.railway.app/health
  https://seu-backend-random.railway.app/docs (Swagger UI)

Frontend:
  https://seu-frontend-random.railway.app
  
Compartilhar com usuários:
  👉 https://seu-frontend-random.railway.app
```

---

## 🐛 Se Algo Não Funcionar

### Backend não inicia (502 Bad Gateway)

1. No dashboard Railway, clique no serviço **backend**
2. Abra a aba **"Logs"** (ou **"Build & Deploy"**)
3. Procure por mensagens de erro (em vermelho)
4. Comum:
   - `ImportError`: Algum módulo faltando
   - `SyntaxError`: Erro no código Python
   - `ModuleNotFoundError`: requirements.txt incompleto

**Solução:**
```powershell
# Teste localmente
cd backend
python main.py

# Se houver erro, fix e faça:
git add .
git commit -m "Fix: Backend error"
git push origin main
# Railway redeploy automaticamente
```

### Frontend mostra branco/carregando

1. Abra console do navegador: `F12`
2. Vá na aba **"Console"**
3. Procure por erro em vermelho (CORS error ou fetch error)
4. Se vir "Cannot GET /api/...", a URL do backend está errada

**Solução:**
1. Verifique que `REACT_APP_API_URL` está correto no Railway
2. Deve ser a URL pública do backend
3. Update a variável no Railroad dashboard
4. Clique redeploy

### CORS Error (Frontend não consegue chamar Backend)

**Mensagem no console:**
```
Access to XMLHttpRequest at 'https://backend.railway.app/...' 
from origin 'https://frontend.railway.app' has been blocked by CORS policy
```

**Solução:**
1. No backend do Railway, update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=["https://seu-frontend-random.railway.app"]
   ```
2. Salve
3. Clique para redeploy
4. Aguarde 2-3 minutos

---

## 📊 Monitorando Seu App

### Ver Logs em Tempo Real
1. Dashboard Railway
2. Clique no serviço (backend ou frontend)
3. Abra aba **"Logs"**
4. Scroll para ver novos eventos

### Métricas de Performance
1. Clique no serviço
2. Abra aba **"Metrics"**
3. Veja:
   - CPU usage
   - Memory usage
   - Network I/O
   - Uptime

### Reiniciar Serviço
Se algo ficar lento:
1. Dashboard → Serviço
2. Clique no menu **"⋮"** (3 pontos)
3. Selecione **"Restart"**

---

## 💰 Custos

**Railway Free Tier:**
- ✅ $5 crédito monthly (gratuito!)
- ✅ Suficiente para MVP
- ✅ Sem necessidade de cartão de crédito (pode ser adicionado depois)

**Estimado para Racket Hero MVP:**
- Backend (CPU + Memory): ~$2/mês
- Frontend (CPU + Memory): ~$2/mês
- Database: $0 (SQLite grátis)
- **Total: ~$4/mês** ✅ Dentro do free tier!

---

## 🎓 Após o Deploy

### Hoje ✅
- [x] Arquivos de config criados
- [x] Repositório atualizado no GitHub
- [ ] Criar conta Railway
- [ ] Conectar GitHub ao Railway
- [ ] Validar primeiro deploy

### Esta Semana
- [ ] Testar com usuários reais
- [ ] Monitorar logs para bugs
- [ ] Otimizar performance se needed
- [ ] Configurar domínio próprio (opcional)

### Próximas Semanas
- [ ] Implementar FASE 2 (code quality improvements)
  - Estrutured logging
  - Validation improvements
  - Global error handling
  - Rate limiting
  - Security hardening
- [ ] Adicionar novas features
- [ ] Coletar feedback de usuários

---

## 📚 Referências Rápidas

### URLs Importantes
- **Railway Dashboard:** https://railway.app/dashboard
- **GitHub Repository:** https://github.com/hirohaya/racket-hero
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/

### Arquivos Criados
- `railway.toml` - Configuração Railway
- `Procfile` - Comandos de start
- `.env.railway` - Variáveis padrão
- `RAILWAY_SETUP.md` - Guia local
- `DEPLOY_RAILWAY_COMPLETO.md` - Guia completo

### Variáveis Padrão
```
Backend:
├─ ENVIRONMENT=production
├─ LOG_LEVEL=INFO
├─ DATABASE_URL=sqlite:///./racket_hero.db
├─ CORS_ORIGINS=["https://seu-frontend.railway.app"]
└─ SECRET_KEY=gere-uma-chave-segura

Frontend:
└─ REACT_APP_API_URL=https://seu-backend.railway.app
```

---

## ✨ Parabéns! 🎉

```
┌──────────────────────────────────────┐
│  ✅ Seu projeto está pronto!         │
│  ✅ Railway está configurado         │
│  ✅ GitHub está atualizado           │
│                                      │
│  Próximo: Criar conta em             │
│  https://railway.app                 │
│                                      │
│  Racket Hero será um sucesso! 🚀    │
└──────────────────────────────────────┘
```

---

**Dúvidas?** Consulte:
- `DEPLOY_RAILWAY_COMPLETO.md` - Guia detalhado
- `RAILWAY_SETUP.md` - Setup técnico
- `docs/FAQ.md` - Perguntas frequentes

**Pronto para começar?** 👉 Siga os passos 1-7 acima!
