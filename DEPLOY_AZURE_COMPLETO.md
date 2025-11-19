# 🚀 Guia de Deploy no Microsoft Azure

**Para Racket Hero - Production Ready MVP**

---

## 📋 Índice

1. [Visão Geral Azure](#visão-geral-azure)
2. [Pré-requisitos](#pré-requisitos)
3. [Opções de Deploy](#opções-de-deploy)
4. [Guia Passo a Passo (Recomendado)](#guia-passo-a-passo-recomendado)
5. [Configurações Específicas](#configurações-específicas)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral Azure

### Por que Azure?

✅ **Vantagens:**
- Integração com GitHub Actions
- App Service rápido e confiável
- Free tier generoso (12 meses)
- Database PostgreSQL gerenciado
- Backup automático
- Escalabilidade fácil
- Suporte em português

❌ **Desvantagens:**
- Pode ser mais complexo que Railway
- Requer mais configuração
- Custo pode ser maior se escalar

### Opções Azure para Racket Hero

| Opção | Serviço | Custo | Complexidade | Recomendação |
|-------|---------|-------|--------------|--------------|
| **A** | App Service + PostgreSQL | $10-50/mês | Média | ⭐ Recomendado |
| **B** | Container Instances | $5-30/mês | Baixa | Alternativa |
| **C** | Kubernetes (AKS) | $50+/mês | Alta | Para scale |

**Recomendação: Opção A (App Service)**
- Melhor custo-benefício
- Menor complexidade
- Suficiente para MVP

---

## 🔧 Pré-requisitos

### Conta e Acessos
- ✅ Conta Microsoft Azure (ou Google)
- ✅ Repositório GitHub com racket-hero
- ✅ Cartão de crédito (para validação, não cobrado no free tier)
- ✅ Permissões de admin no GitHub repo

### Ferramentas (Opcional)
```bash
# Azure CLI (opcional, pode fazer tudo no site)
# Windows: https://aka.ms/installazurecliwindows
# Mac: brew install azure-cli
# Linux: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Verificar instalação
az --version
```

---

## 🛣️ Opções de Deploy

### **OPÇÃO A: App Service + PostgreSQL (RECOMENDADO)**

**Quando usar:**
- ✅ MVP production-ready
- ✅ Precisa de database gerenciado
- ✅ Quer escalabilidade futura
- ✅ Quer CI/CD integrado

**Passo a passo:** [Ver seção abaixo](#guia-passo-a-passo-recomendado)

**Custo:**
- App Service: Free tier (1 ano) depois ~$11-15/mês
- PostgreSQL: Free tier depois ~$35-50/mês
- **Total:** Free (1 ano) depois ~$50/mês

**Características:**
- Escalabilidade automática
- Backup diário
- CI/CD integrado
- Custom domain
- SSL grátis

---

### **OPÇÃO B: Container Instances (ALTERNATIVA)**

**Quando usar:**
- ✅ Quer simplicidade
- ✅ Docker já pronto
- ✅ Orçamento baixo

**Passos resumidos:**
1. Criar Azure Container Registry (ACR)
2. Upload da imagem Docker
3. Criar Container Instance
4. Configurar networking

**Custo:**
- Container: ~$10-15/mês
- Registry: Free (até 10 repositórios)
- **Total:** ~$15-20/mês

**Nota:** SQLite não persiste. Precisa Azure Database.

---

### **OPÇÃO C: Kubernetes (AKS) (FUTURO)**

**Quando usar:**
- ❌ Não recomendado para MVP
- ✅ Quando escalar para 1000+ usuários

**Custo:**
- Cluster: ~$0.10/hora (~$70/mês)
- Nodes: Extra
- **Total:** $100+/mês

---

## 📖 Guia Passo a Passo (Recomendado)

### **PASSO 1: Criar Conta Azure (5 min)**

#### Via Site
1. Ir para https://azure.microsoft.com/pt-br/
2. Clique em "Iniciar gratuitamente"
3. Escolha: Login com GitHub ou Microsoft
4. Preencha dados
5. Adicione cartão de crédito (validação, não cobra)
6. Confirme

#### Resultado:
- ✅ Conta ativa
- ✅ $200 de crédito (30 dias)
- ✅ Serviços free (12 meses)

---

### **PASSO 2: Criar Resource Group (2 min)**

Resource Group = pasta para organizar recursos

#### Via Azure Portal
1. Abrir https://portal.azure.com
2. Procure por "Resource groups"
3. Clique "Create"
4. **Nome:** `racket-hero-rg`
5. **Região:** `(Brazil) Brazil South` ou `East US 2`
6. Clique "Review + create"
7. Clique "Create"

**Dica:** Brazil South é mais rápido para usuários BR

---

### **PASSO 3: Criar PostgreSQL Database (3 min)**

#### Via Azure Portal
1. No portal, procure por "Azure Database for PostgreSQL"
2. Clique "Create"
3. Escolha "Single server" (depois migra para Flexible)

#### Configurações:
```
Project Details:
  ├─ Subscription: Sua subscription
  ├─ Resource group: racket-hero-rg
  └─ Server name: racket-hero-db (deve ser único)

Compute + Storage:
  ├─ Compute tier: Burstable (B1s é suficiente)
  ├─ Compute size: Standard_B1s
  └─ Storage: 32 GB (suficiente para MVP)

Authentication:
  ├─ Admin username: azureuser
  └─ Password: [Gere senha forte - GUARDE ISSO!]

Networking:
  ├─ Connectivity method: Public endpoint
  ├─ Allow Azure services: YES
  └─ Add current client IP: YES (seu IP)

Backup:
  ├─ Backup retention: 7 days
  └─ Geo-redundant: Disabled (para MVP)
```

#### Salvar:
- ✅ Server name: `racket-hero-db`
- ✅ Username: `azureuser`
- ✅ Password: `[Sua senha]`
- ✅ Connection string: (vará precisar depois)

**Clique "Create" e espere 3-5 minutos**

---

### **PASSO 4: Criar App Service (2 min)**

#### Via Azure Portal
1. Procure por "App Services"
2. Clique "Create"
3. Clique "Web App"

#### Configurações:
```
Project Details:
  ├─ Subscription: Sua subscription
  ├─ Resource group: racket-hero-rg
  ├─ Name: racket-hero-app (será seu domínio)
  └─ Publish: Docker Container

Runtime Stack:
  ├─ OS: Linux
  ├─ Region: Brazil South (ou East US 2)
  └─ App Service Plan: Criar novo
     ├─ Name: racket-hero-plan
     └─ Pricing tier: Free F1 (grátis por 1 ano)

Docker:
  ├─ Image source: GitHub Container Registry
  ├─ Repository: hirohaya/racket-hero
  ├─ Image: latest
  └─ Startup command: (deixe vazio)
```

**Nota:** Vamos configurar Docker depois via GitHub Actions

**Clique "Create" e espere 2-3 minutos**

---

### **PASSO 5: Configurar Variáveis de Ambiente (3 min)**

App Service precisa conhecer a connection string do banco

#### Via Azure Portal
1. Vá para seu App Service: `racket-hero-app`
2. Procure por "Configuration"
3. Clique em "New application setting"

#### Adicione estas variáveis:
```
DATABASE_URL=postgresql://azureuser:SENHA@racket-hero-db.postgres.database.azure.com/postgres

CORS_ORIGINS=https://racket-hero-app.azurewebsites.net

LOG_LEVEL=info

ENVIRONMENT=production
```

**Substituir:**
- `SENHA` pela senha do PostgreSQL
- URL do host conforme seu server

#### Como obter URL do PostgreSQL:
1. Vá para seu PostgreSQL Server
2. Overview → Connection strings
3. Copie "ODBC" (ajuste o formato)

**Após adicionar, clique "Save"**

---

### **PASSO 6: Configurar Deployment via GitHub Actions (5 min)**

Azure pode fazer deploy automático quando você fizer push

#### Opção A: Via Portal (Mais fácil)
1. No App Service, procure "Deployment Center"
2. Clique em "Deployment Center"
3. **Source:** GitHub
4. **Organization:** sua conta GitHub
5. **Repository:** racket-hero
6. **Branch:** main
7. **Build provider:** GitHub Actions
8. Clique "Save"

Azure vai criar workflow automaticamente!

#### Opção B: Manual (Mais controle)
Vamos criar no próximo passo.

---

### **PASSO 7: Criar GitHub Actions Workflow para Azure (5 min)**

Crie arquivo `.github/workflows/deploy-azure.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches:
      - main

env:
  REGISTRY_URL: ${{ secrets.AZURE_REGISTRY_LOGIN_SERVER }}
  IMAGE_NAME: racket-hero

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Login to Azure Container Registry
      uses: azure/docker-login@v1
      with:
        login-server: ${{ secrets.AZURE_REGISTRY_LOGIN_SERVER }}
        username: ${{ secrets.AZURE_REGISTRY_USERNAME }}
        password: ${{ secrets.AZURE_REGISTRY_PASSWORD }}

    - name: Build Docker image
      run: |
        docker build -t ${{ env.REGISTRY_URL }}/${{ env.IMAGE_NAME }}:latest .
        docker push ${{ env.REGISTRY_URL }}/${{ env.IMAGE_NAME }}:latest

    - name: Deploy to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'racket-hero-app'
        images: ${{ env.REGISTRY_URL }}/${{ env.IMAGE_NAME }}:latest
```

#### Adicionar Secrets no GitHub:
1. Ir para: repo → Settings → Secrets and variables
2. Clique "New repository secret"

Adicione:
- `AZURE_REGISTRY_LOGIN_SERVER` - seu ACR login server
- `AZURE_REGISTRY_USERNAME` - seu ACR username
- `AZURE_REGISTRY_PASSWORD` - seu ACR password
- `AZURE_CREDENTIALS` - (para deploy)

**Como obter essas credenciais:**
[Ver seção Configurações Específicas abaixo](#configurações-específicas)

---

### **PASSO 8: Validar Health Check (2 min)**

Após deploy completar:

1. Abra: `https://racket-hero-app.azurewebsites.net/health`
2. Deve retornar:
```json
{
  "status": "ok",
  "message": "Racket Hero API is running",
  "version": "1.0.0",
  "timestamp": "2025-11-19T..."
}
```

3. Teste database:
`https://racket-hero-app.azurewebsites.net/health/db`

4. Acesse API docs:
`https://racket-hero-app.azurewebsites.net/docs`

---

### **PASSO 9: Configurar Domínio Próprio (Opcional - 5 min)**

Se tem domínio próprio (ex: api.seu-site.com)

#### Via Azure Portal
1. No App Service, procure "Custom domains"
2. Clique "Add custom domain"
3. Preencha seu domínio
4. Escolha validação CNAME ou A record
5. Siga instruções do seu registrador
6. Retorne ao Azure e clique "Validate"

**Depois:**
- Azure gera SSL grátis automaticamente
- Domínio pronto em 5 minutos

---

## 🔧 Configurações Específicas

### Obter Credentials do Azure Container Registry

#### Criar ACR:
1. Portal Azure → Container Registries
2. Clique "Create"
3. Nome: `racketheroregistry` (deve ser único)
4. Resource group: `racket-hero-rg`
5. Location: `Brazil South`
6. SKU: `Basic` (suficiente para MVP)
7. Clique "Create"

#### Obter Credenciais:
1. Vá para seu ACR
2. Settings → Access keys
3. Enable admin user
4. Copie:
   - Login server: `racketheroregistry.azurecr.io`
   - Username: `racketheroregistry`
   - Password: `[token]`

---

### Connection String PostgreSQL

Após PostgreSQL criar:

1. Vá para seu servidor PostgreSQL
2. Settings → Connection strings
3. Copie URL JDBC (não exatamente)

**Formato correto para Python:**
```
postgresql://azureuser:SENHA@racket-hero-db.postgres.database.azure.com/postgres
```

**Para SQLAlchemy:**
```
postgresql+psycopg2://azureuser:SENHA@racket-hero-db.postgres.database.azure.com/postgres
```

---

### Migrar de SQLite para PostgreSQL

Seu código já suporta variável de ambiente!

#### No `backend/database.py`:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./racket_hero.db")
```

**Basta mudar `DATABASE_URL` no Azure para PostgreSQL!**

---

## 📊 Checklist de Deploy Azure

### ✅ Antes de Começar
- [ ] Conta Azure criada
- [ ] Cartão de crédito adicionado
- [ ] GitHub repo sincronizado
- [ ] Código em main branch

### ✅ Infraestrutura
- [ ] Resource Group criado
- [ ] PostgreSQL Server criado
- [ ] App Service criado
- [ ] App Service Plan gratuito
- [ ] Container Registry criado (ACR)

### ✅ Configuração
- [ ] Variáveis de ambiente definidas
- [ ] DATABASE_URL configurada
- [ ] CORS_ORIGINS configurada
- [ ] Secrets GitHub adicionados
- [ ] GitHub Actions workflow criado

### ✅ Deploy
- [ ] Primeiro push para main
- [ ] GitHub Actions executado
- [ ] Docker image buildado
- [ ] Container deployado
- [ ] App Service iniciado

### ✅ Validação
- [ ] /health retorna 200 OK
- [ ] /health/db retorna 200 OK
- [ ] /docs acessível (Swagger)
- [ ] Logs monitorados
- [ ] Alerts configurados

### ✅ Produção
- [ ] Domínio configurado (opcional)
- [ ] SSL ativo
- [ ] Backup automático ativo
- [ ] Monitoring ativo
- [ ] Usuários testam

---

## 🆘 Troubleshooting

### Problema: App Service não inicia

**Sintoma:**
```
502 Bad Gateway
Application Error
```

**Soluções:**
1. Verifique logs:
   - Azure Portal → App Service → Log Stream
   - Procure por erro Python/startup

2. Valide DATABASE_URL:
   - Teste connection no seu PC local
   - Verifique credenciais
   - Verifique firewall do PostgreSQL

3. Verifique Dockerfile:
   - Build localmente com docker
   - Teste se roda
   - Publique no ACR

```bash
# Test local
docker build -t racket-hero .
docker run -p 8000:8000 racket-hero

# Upload para ACR
docker tag racket-hero racketheroregistry.azurecr.io/racket-hero:latest
docker push racketheroregistry.azurecr.io/racket-hero:latest
```

---

### Problema: Database não conecta

**Sintoma:**
```
/health/db retorna erro
ConnectionRefusedError
```

**Soluções:**
1. Verifique firewall do PostgreSQL:
   - Azure Portal → PostgreSQL → Connection security
   - Verifique "Allow Azure services to access this server"
   - Adicione IP do App Service se necessário

2. Verifique DATABASE_URL:
   ```bash
   # Teste com psql local
   psql "postgresql://azureuser:SENHA@racket-hero-db.postgres.database.azure.com/postgres"
   ```

3. Verifique credenciais:
   - Copie exatamente username e password
   - Escape caracteres especiais (%, @, etc)

---

### Problema: GitHub Actions falha

**Sintoma:**
```
Docker build fails
Push to registry fails
```

**Soluções:**
1. Verifique Secrets:
   - Settings → Secrets → Verifique todos
   - Teste credenciais localmente

2. Verifique Dockerfile:
   ```bash
   docker build -t test .
   ```

3. Verifique ACR:
   - Subscription válida?
   - ACR ativo?
   - Admin user habilitado?

---

### Problema: Slow performance

**Sintoma:**
```
First request lento (3-5 segundos)
Requests subsequentes rápidos
```

**Solução:**
- Normal para App Service Free tier
- Upgrade para Premium (pago) resolve
- Cold start é esperado

---

## 💰 Custos Estimados

### Free Tier (Primeiro Ano)
```
App Service Free:        $0 (12 meses)
PostgreSQL Free:         $0 (primeiro mês)
Storage:                 $0 (32GB grátis)
Bandwidth:               $0 (85GB/mês grátis)
───────────────────────
Total:                   $0 (1º ano)
```

### Após Free Tier (Estimado)
```
App Service Basic:       ~$15/mês
PostgreSQL Basic:        ~$35-50/mês
Storage extra (50GB):    ~$5/mês
───────────────────────
Total:                   ~$55-70/mês
```

### Como Reduzir Custos
1. Deixar em Free tier enquanto possível
2. Usar PostgreSQL Flexible Server (mais barato)
3. Implementar auto-scaling (pagar só por uso)
4. Usar reserved instances (desconto 30%)

---

## 📚 Referências Úteis

### Documentação Oficial
- [Azure App Service Docs](https://learn.microsoft.com/pt-br/azure/app-service/)
- [PostgreSQL Azure](https://learn.microsoft.com/pt-br/azure/postgresql/)
- [Container Registry](https://learn.microsoft.com/pt-br/azure/container-registry/)
- [GitHub Actions Azure](https://github.com/Azure/login)

### Tutoriais
- [Deploy Python FastAPI no Azure](https://learn.microsoft.com/pt-br/azure/app-service/quickstart-python)
- [PostgreSQL Connection Strings](https://learn.microsoft.com/pt-br/azure/postgresql/single-server/concepts-connection-libraries)

### Community
- [Azure Docs PT-BR](https://learn.microsoft.com/pt-br/azure/)
- [Stack Overflow Azure Tag](https://stackoverflow.com/questions/tagged/azure)

---

## ✅ Quick Checklist (30-45 min)

```bash
⏱️ 5 min:   Criar conta Azure
⏱️ 2 min:   Criar Resource Group
⏱️ 5 min:   Criar PostgreSQL
⏱️ 2 min:   Criar App Service
⏱️ 5 min:   Criar Container Registry
⏱️ 3 min:   Adicionar variáveis de ambiente
⏱️ 5 min:   Criar GitHub Actions workflow
⏱️ 3 min:   Adicionar Secrets no GitHub
⏱️ 10 min:  Esperar deploy
⏱️ 2 min:   Validar /health endpoint
─────────────────────
Total:     ~45 minutos
```

---

## 🚀 PRÓXIMO PASSO

1. **Escolha a opção:**
   - Opção A: App Service (RECOMENDADO) ⭐
   - Opção B: Container Instances
   - Opção C: Kubernetes

2. **Se escolher Opção A:**
   - Siga "Guia Passo a Passo" acima
   - Comece pelo PASSO 1

3. **Dúvidas?**
   - Consulte seção Troubleshooting
   - Verifique Referências Úteis

---

**Criado:** 19 de Novembro de 2025  
**Status:** Pronto para Usar  
**Tempo Estimado:** 30-45 minutos até produção

**Boa sorte! 🚀**
