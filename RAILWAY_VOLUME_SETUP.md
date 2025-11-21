# Como Configurar Volume Persistente no Railway

## Método 1: Via Dashboard Railway (Mais Fácil) ✅

### Passo 1: Acessar o Dashboard
1. Vá para https://railway.app
2. Clique no seu projeto `racket-hero`
3. Clique no serviço **backend** (não o frontend)

### Passo 2: Configurar Volume
1. No painel do backend, clique em **"Variables"** (lado esquerdo)
2. Procure pela seção **"Volumes"** ou **"Storage"**
3. Clique em **"Add Volume"** ou **"+ New"**

### Passo 3: Configurar o Caminho
- **Mount Path (Caminho no Container):** `/app/backend`
- **Ou se preferir:** `/app/data`

### Passo 4: Salvar e Deploy
1. Clique em **"Save"** ou **"Add"**
2. Clique em **"Redeploy"** para aplicar as mudanças
3. Aguarde o deploy completar

---

## Método 2: Via `railway.toml` (Configuração como Código)

Crie ou edite o arquivo `railway.toml` na raiz do projeto:

```toml
[build]
  builder = "dockerfile"

[deploy]
  startCommand = "bash start.sh"
  numReplicas = 1
  healthcheckPath = "/health"
  healthcheckInterval = 30

[[build.volumes]]
  source = "racket_hero_data"
  destination = "/app/backend"

[[services]]
  name = "backend"
  variables = {}
  
  [services.volumes]
    source = "racket_hero_data"
    destination = "/app/backend"
```

---

## Método 3: Via CLI Railway

Se você tem o Railway CLI instalado:

```bash
# Login no Railway
railway login

# Navegar para o projeto
railway project select racket-hero

# Criar volume
railway volume create racket_hero_data /app/backend

# Verificar volumes
railway volume list

# Deploy
railway deploy
```

---

## ✅ Verificar se está funcionando

### 1. No Dashboard:
- Vá em **Backend** → **Variables** 
- Procure por **"Volumes"** ou **"Storage"**
- Você deve ver: `/app/backend` (mounted)

### 2. Testar persistência:
1. Fazer deploy (seed executa UMA VEZ)
2. Criar um evento no Dashboard
3. Fazer deploy novamente
4. ✅ Evento ainda deve estar lá!

---

## ⚠️ Importante: Limpar dados antigos

Se você já fez vários deploys e quer resetar tudo:

**Via Dashboard:**
1. Vá em **Backend** → **Variables** → **Volumes**
2. Clique no volume `racket_hero_data`
3. Clique em **"Delete"** ou **"Clear"**
4. Redeploy

**Via CLI:**
```bash
railway volume delete racket_hero_data
railway deploy
```

---

## 🔍 Localização Exata dos Dados

Depois de configurar o volume:
- **Banco de dados SQLite:** `/app/backend/racket_hero.db`
- **Logs:** `/app/backend/logs/`
- **Backups:** `/app/backend/backups/`

Tudo será **persistido** entre deploys! 🎉

---

## Próximos Passos

- [ ] Configurar volume via Dashboard
- [ ] Fazer deploy
- [ ] Criar um evento manualmente
- [ ] Fazer outro deploy
- [ ] Verificar se evento ainda existe
- [ ] ✅ Sucesso!
