# 🎯 Guia Visual Azure - Clique a Clique

**Para quem prefere visual ao invés de texto**

---

## 📌 Sumário Visual

```
1️⃣  Criar Conta Azure
    ↓
2️⃣  Resource Group
    ↓
3️⃣  PostgreSQL Database
    ↓
4️⃣  Container Registry (ACR)
    ↓
5️⃣  App Service
    ↓
6️⃣  Variáveis de Ambiente
    ↓
7️⃣  GitHub Actions Setup
    ↓
8️⃣  Deploy & Validação
    ↓
✅ Em Produção!
```

---

## 1️⃣ CRIAR CONTA AZURE (5 min)

### Passo 1.1: Ir para Azure
```
URL: https://azure.microsoft.com/pt-br/
```

### Passo 1.2: Clicar em "Iniciar gratuitamente"
```
Você vê na página inicial:
┌─────────────────────────────┐
│  Iniciar gratuitamente    ← CLIQUE AQUI
│  $200 de crédito por 30 dias
└─────────────────────────────┘
```

### Passo 1.3: Escolher login
```
Opções:
├─ Login com GitHub (RECOMENDADO)
├─ Login com Microsoft
└─ Login com Google

CLIQUE: "Login com GitHub"
```

### Passo 1.4: Autorizar Azure
```
GitHub pede permissão:
┌─────────────────────────────┐
│ Azure deseja acessar sua    │
│ conta GitHub para:          │
│ ├─ Ler repositórios         │
│ ├─ Acessar perfil           │
│ └─ Usar para CI/CD          │
│                             │
│ [Autorizar Azure]  ← CLIQUE │
└─────────────────────────────┘
```

### Passo 1.5: Preencher dados
```
Formulário:
├─ Nome completo: [Seu nome]
├─ Email: [seu@email.com]
├─ País/Região: Brasil
├─ Número telefone: [seu número]
├─ Cartão de crédito: [para validação]
└─ [Continuar] ← CLIQUE
```

### Passo 1.6: Validação telefone
```
Azure envia SMS com código:
┌─────────────────────────────┐
│ Código recebido: [______]   │
│ [Verificar]         ← CLIQUE│
└─────────────────────────────┘
```

### ✅ Resultado
```
Você tem acesso a:
✅ Azure Portal
✅ $200 de crédito (30 dias)
✅ Serviços Free (12 meses)
```

---

## 2️⃣ CRIAR RESOURCE GROUP (2 min)

### Passo 2.1: Abrir Portal Azure
```
URL: https://portal.azure.com
```

### Passo 2.2: Buscar "Resource groups"
```
┌──────────────────────────────┐
│ 🔍 Buscar recursos e serviços│
│   ├─ Digitar: resource groups
│   └─ Ver sugestão
│                              │
│ "Resource groups"   ← CLIQUE │
└──────────────────────────────┘
```

### Passo 2.3: Criar novo grupo
```
Na página Resource Groups:
┌──────────────────────────────┐
│ + Create resource group ← CLIQUE
│                              │
│ Ou se vazio:                 │
│ [Create resource group]      │
└──────────────────────────────┘
```

### Passo 2.4: Preencher detalhes
```
Formulário:
├─ Subscription: Sua subscription (Default)
│  
├─ Resource group name: 
│  └─ Digitar: racket-hero-rg
│
├─ Region:
│  └─ Selecionar: Brazil South ⭐
│     (ou East US 2 se não tiver BR)
│
└─ [Review + create] ← CLIQUE
```

### Passo 2.5: Revisar
```
Review + create:
┌──────────────────────────────┐
│ Validation passed            │
│ Summary:                      │
│ • Resource group: racket-hero-rg
│ • Region: Brazil South       │
│ • Subscription: [sua sub]    │
│                              │
│ [Create] ← CLIQUE            │
└──────────────────────────────┘
```

### ✅ Resultado
```
Resource Group criado:
✅ Nome: racket-hero-rg
✅ Região: Brazil South
✅ Pronto para recursos
```

---

## 3️⃣ CRIAR POSTGRESQL DATABASE (5 min)

### Passo 3.1: Buscar PostgreSQL
```
No portal Azure:
┌──────────────────────────────┐
│ 🔍 Buscar                    │
│   └─ Digitar: azure database for postgresql
│                              │
│ "Azure Database for PostgreSQL"
│ └─ Single server ← CLIQUE    │
└──────────────────────────────┘
```

### Passo 3.2: Criar servidor
```
┌──────────────────────────────┐
│ + Create          ← CLIQUE   │
│                              │
│ Escolha: Single server       │
│ (depois migra para Flexible) │
└──────────────────────────────┘
```

### Passo 3.3: Project Details
```
Preenchimento 1:
├─ Subscription: Sua subscription
├─ Resource group: racket-hero-rg ← SELECIONAR
├─ Server name: racket-hero-db
│  (será único, Azure valida)
└─ Region: Brazil South
```

### Passo 3.4: Authentication
```
Preenchimento 2:
├─ Admin username: azureuser
├─ Password: [GERE SENHA FORTE]
│  Exemplo: AzureP@ss2025!#$%
│
├─ Confirm password: [REPITA]
│
└─ IMPORTANTE: 
   ✍️  Guarde username e password!
   ✍️  Vai precisar depois!
```

### Passo 3.5: Compute + Storage
```
Preenchimento 3:
├─ Pricing Tier: Burstable (Recommended)
├─ Compute size: Standard_B1s
│  └─ vCores: 1
│  └─ Memory: 1 GB
│
├─ Storage: 32 GB
│  (suficiente para MVP)
│
└─ Backup Retention: 7 days
```

### Passo 3.6: Networking
```
Preenchimento 4:
├─ Connectivity: Public endpoint
├─ Firewall rules:
│  ├─ Allow Azure services: YES ✅
│  ├─ Add current client IP: YES ✅
│  │  (seu PC)
│  └─ Add to allow list
│
└─ Geo-redundancy: NO (para MVP)
```

### Passo 3.7: Review + Create
```
┌──────────────────────────────┐
│ [Review + create] ← CLIQUE   │
│                              │
│ Valida tudo...               │
│ Validation passed            │
│                              │
│ [Create] ← CLIQUE            │
└──────────────────────────────┘
```

### ⏳ Aguardar
```
Deployment em progresso:
┌──────────────────────────────┐
│ ⏳ Creating PostgreSQL        │
│ (Takes 3-5 minutes)          │
│                              │
│ ✅ Deployment succeeded       │
│ Go to resource ← CLIQUE      │
└──────────────────────────────┘
```

### ✅ Resultado
```
PostgreSQL Server criado:
✅ Nome: racket-hero-db.postgres.database.azure.com
✅ Admin: azureuser
✅ Senha: [sua senha]
✅ Status: Running
```

### 📝 Salvar informações:
```
Quando cria, salve:
├─ Server name: racket-hero-db
├─ Admin username: azureuser
├─ Password: [sua senha]
├─ Host: racket-hero-db.postgres.database.azure.com
└─ Database: postgres

Você vai precisar desses dados em:
└─ DATABASE_URL=postgresql://azureuser:SENHA@HOST/postgres
```

---

## 4️⃣ CRIAR CONTAINER REGISTRY (3 min)

### Passo 4.1: Buscar Container Registry
```
No portal:
┌──────────────────────────────┐
│ 🔍 Buscar                    │
│   └─ Digitar: container registries
│                              │
│ "Container registries"       │
│ └─ CLIQUE                    │
└──────────────────────────────┘
```

### Passo 4.2: Criar registry
```
┌──────────────────────────────┐
│ + Create          ← CLIQUE   │
└──────────────────────────────┘
```

### Passo 4.3: Detalhes
```
Formulário:
├─ Subscription: Sua subscription
├─ Resource group: racket-hero-rg
├─ Registry name: racketheroregistry
│  (deve ser ÚNICO)
│  (sem caracteres especiais)
│
├─ Location: Brazil South
└─ SKU: Basic ⭐
   (Suficiente para MVP)
   
Clique: [Review + create]
```

### Passo 4.4: Review + Create
```
┌──────────────────────────────┐
│ [Create] ← CLIQUE            │
│                              │
│ ⏳ Deployment...             │
│ ✅ Success                   │
│ "Go to resource" ← CLIQUE    │
└──────────────────────────────┘
```

### Passo 4.5: Habilitar Admin User
```
Na página do ACR:
Settings → Access keys

├─ Enable admin user: [TOGGLE] ← CLIQUE
│
Depois você vê:
├─ Login server: racketheroregistry.azurecr.io
├─ Username: racketheroregistry
├─ Password: [token gerado]
│
✍️  COPIE ESSES DADOS!
    Vai usar em GitHub Secrets
```

### ✅ Resultado
```
Container Registry criado:
✅ Nome: racketheroregistry.azurecr.io
✅ Admin user: ativado
✅ Credenciais obtidas
```

---

## 5️⃣ CRIAR APP SERVICE (3 min)

### Passo 5.1: Buscar App Service
```
No portal:
┌──────────────────────────────┐
│ 🔍 Buscar                    │
│   └─ Digitar: app services  │
│                              │
│ "App Services"               │
│ └─ CLIQUE                    │
└──────────────────────────────┘
```

### Passo 5.2: Criar app
```
┌──────────────────────────────┐
│ + Create          ← CLIQUE   │
│                              │
│ Ou: [Create App Service]     │
└──────────────────────────────┘
```

### Passo 5.3: Detalhes básicos
```
Preenchimento 1:
├─ Subscription: Sua subscription
├─ Resource group: racket-hero-rg
├─ Name: racket-hero-app
│  (seu domínio será)
│  (racket-hero-app.azurewebsites.net)
│
├─ Publish: Docker Container ← IMPORTANTE
├─ Operating System: Linux
├─ Region: Brazil South
│
└─ [Next: Docker] ← CLIQUE
```

### Passo 5.4: App Service Plan
```
Preenchimento 2 (App Service Plan):
├─ Create new:
│  ├─ Name: racket-hero-plan
│  └─ Sku and size:
│     ├─ Clique "Change size"
│     ├─ Selecione "Free F1"
│     └─ Clique "Apply"
│
└─ [Next: Docker] ← CLIQUE
```

### Passo 5.5: Docker (deixe para depois)
```
Preenchimento 3 (Docker):
├─ Image Source: Docker Hub (por enquanto)
├─ Ou deixe vazio
│
├─ Vamos configurar via GitHub Actions depois
│
└─ [Review + create] ← CLIQUE
```

### Passo 5.6: Review + Create
```
┌──────────────────────────────┐
│ [Create] ← CLIQUE            │
│                              │
│ ⏳ Deployment...             │
│ ✅ Success                   │
│ "Go to resource" ← CLIQUE    │
└──────────────────────────────┘
```

### ✅ Resultado
```
App Service criado:
✅ Nome: racket-hero-app
✅ URL: racket-hero-app.azurewebsites.net
✅ Pronto para configuração
```

---

## 6️⃣ VARIÁVEIS DE AMBIENTE (3 min)

### Passo 6.1: Ir para Configuration
```
No seu App Service (racket-hero-app):
Menu esquerdo:
├─ Settings
│  └─ Configuration ← CLIQUE
```

### Passo 6.2: Application Settings
```
Sua vê:
┌──────────────────────────────┐
│ Application settings         │
│ + New application setting    │
│                              │
│ [Adicionar as que faltam]    │
└──────────────────────────────┘
```

### Passo 6.3: Adicionar DATABASE_URL
```
Clique "+ New application setting"

├─ Name: DATABASE_URL
│
├─ Value: postgresql://azureuser:SENHA@racket-hero-db.postgres.database.azure.com/postgres
│  (substitua SENHA pela sua)
│
└─ [OK] ← CLIQUE

Depois [Save] no topo
```

### Passo 6.4: Adicionar CORS_ORIGINS
```
Clique "+ New application setting"

├─ Name: CORS_ORIGINS
│
├─ Value: https://racket-hero-app.azurewebsites.net
│
└─ [OK] ← CLIQUE
```

### Passo 6.5: Adicionar LOG_LEVEL
```
Clique "+ New application setting"

├─ Name: LOG_LEVEL
│
├─ Value: info
│
└─ [OK] ← CLIQUE
```

### Passo 6.6: Salvar todas
```
No topo da página:
┌──────────────────────────────┐
│ [Save] ← CLIQUE              │
│                              │
│ ⚠️  Isso vai reiniciar o app  │
│                              │
│ [Continue] ← CLIQUE          │
└──────────────────────────────┘
```

### ✅ Resultado
```
Variáveis de ambiente definidas:
✅ DATABASE_URL
✅ CORS_ORIGINS
✅ LOG_LEVEL
✅ Aplicadas ao App Service
```

---

## 7️⃣ GITHUB SECRETS (5 min)

### Passo 7.1: Ir para GitHub
```
https://github.com/hirohaya/racket-hero
```

### Passo 7.2: Settings → Secrets
```
Menu do repo:
├─ ⚙️ Settings ← CLIQUE
├─ Secrets and variables
│  └─ Actions ← CLIQUE
```

### Passo 7.3: Adicionar Secrets
```
Você vê:
┌──────────────────────────────┐
│ New repository secret        │
│ [New repository secret] ← CLIQUE
└──────────────────────────────┘
```

### Passo 7.4: Adicionar AZURE_REGISTRY_LOGIN_SERVER
```
├─ Name: AZURE_REGISTRY_LOGIN_SERVER
├─ Value: racketheroregistry.azurecr.io
│  (copie do seu ACR)
│
└─ [Add secret] ← CLIQUE
```

### Passo 7.5: Adicionar AZURE_REGISTRY_USERNAME
```
├─ Name: AZURE_REGISTRY_USERNAME
├─ Value: racketheroregistry
│  (seu ACR username)
│
└─ [Add secret] ← CLIQUE
```

### Passo 7.6: Adicionar AZURE_REGISTRY_PASSWORD
```
├─ Name: AZURE_REGISTRY_PASSWORD
├─ Value: [seu password do ACR]
│  (copie do Access keys)
│
└─ [Add secret] ← CLIQUE
```

### ✅ Resultado
```
Secrets adicionados:
✅ AZURE_REGISTRY_LOGIN_SERVER
✅ AZURE_REGISTRY_USERNAME
✅ AZURE_REGISTRY_PASSWORD
✅ Prontos para GitHub Actions
```

---

## 8️⃣ DEPLOY GITHUB ACTIONS (Automático)

### Passo 8.1: Criar Workflow
```
No seu repo GitHub:

Crie o arquivo:
.github/workflows/deploy-azure.yml

(Se já não existir do DEPLOY_AZURE_COMPLETO.md)
```

### Passo 8.2: Push para Main
```
No seu terminal local:

git add .
git commit -m "Deploy Azure setup"
git push origin main
```

### Passo 8.3: Acompanhar Deploy
```
Na página do repo GitHub:
├─ Actions ← CLIQUE
├─ Workflows
│  └─ "Deploy to Azure"
│     └─ Veja o progresso:
│        ├─ ⏳ Building...
│        ├─ ✅ Build succeeded
│        ├─ ⏳ Deploying...
│        ├─ ✅ Deploy succeeded
│        └─ Tempo total: ~5 min
```

### ✅ Resultado
```
Deploy completo:
✅ Docker image buildado
✅ Image enviada para ACR
✅ App Service atualizado
✅ Container iniciado
```

---

## 9️⃣ VALIDAR DEPLOYMENT (2 min)

### Passo 9.1: Testar Health
```
No navegador:
https://racket-hero-app.azurewebsites.net/health

Você vê:
┌──────────────────────────────┐
│ {                            │
│   "status": "ok",            │
│   "message": "Racket Hero... │
│   "version": "1.0.0",        │
│   "timestamp": "2025-11-19..."│
│ }                            │
└──────────────────────────────┘

✅ API está rodando!
```

### Passo 9.2: Testar Database
```
No navegador:
https://racket-hero-app.azurewebsites.net/health/db

Você vê:
┌──────────────────────────────┐
│ {                            │
│   "status": "ok",            │
│   "database": {              │
│     "status": "ok",          │
│     "message": "Database...  │
│   }                          │
│ }                            │
└──────────────────────────────┘

✅ Database está conectado!
```

### Passo 9.3: Acessar Swagger Docs
```
No navegador:
https://racket-hero-app.azurewebsites.net/docs

Você vê:
┌──────────────────────────────┐
│ Swagger UI                   │
│                              │
│ ├─ GET /health              │
│ ├─ GET /health/db           │
│ ├─ POST /api/auth/register  │
│ ├─ POST /api/auth/login     │
│ ├─ ... todos os endpoints   │
│                              │
│ ✅ API 100% funcional!       │
└──────────────────────────────┘
```

### ✅ Resultado Final
```
Tudo funcionando:
✅ API respondendo
✅ Database conectado
✅ Endpoints acessíveis
✅ EM PRODUÇÃO! 🚀
```

---

## 📋 RESUMO VISUAL - O QUE CLICAR

### Sequência de Clicks:

1. **Azure Portal Home**
   ```
   https://portal.azure.com
   ```

2. **Resource Groups** → New
3. **PostgreSQL** → New Server
4. **Container Registry** → New
5. **App Services** → New Web App
6. **App Service → Configuration** → New Settings
7. **GitHub → Settings → Secrets** → New Secret
8. **GitHub → Actions** → Acompanhar Deploy

---

## 🎯 E Pronto!

Depois de seguir todos os 9 passos:

```
✅ Conta Azure criada
✅ Resource Group criado
✅ PostgreSQL rodando
✅ Container Registry pronto
✅ App Service deployado
✅ Variáveis configuradas
✅ GitHub Secrets adicionados
✅ Deploy automático ativo
✅ Health endpoints validados

🚀 SITE EM PRODUÇÃO!
https://racket-hero-app.azurewebsites.net
```

---

**Tempo total:** ~45 minutos  
**Dificuldade:** Fácil (basta seguir os cliques)  
**Suporte:** Veja `DEPLOY_AZURE_COMPLETO.md` para detalhes

Boa sorte! 🚀
