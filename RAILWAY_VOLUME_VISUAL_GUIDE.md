# Screenshots: Configurar Volume no Railway

## Local Exato no Dashboard

```
Railway Dashboard
├── Projects
│   └── racket-hero
│       ├── backend (← Clique aqui)
│       └── frontend
│           ↓
│       Backend Service Panel
│       ├── Deployments
│       ├── Environment (← Pode estar aqui)
│       ├── Variables (← OU aqui)
│       ├── Monitoring
│       └── Settings
│           ↓
│       [Procure por "Storage" ou "Volumes"]
│       ↓
│       Add Volume / Storage
│       ├── Mount Path: /app/backend
│       └── [Save] → [Redeploy]
```

---

## Passo a Passo com Links

### 1️⃣ Abrir Railway
- Link: https://railway.app/dashboard/projects

### 2️⃣ Selecionar Projeto racket-hero
- Clique em "racket-hero" na lista de projetos

### 3️⃣ Selecionar Backend Service
- No menu do projeto, procure por "backend"
- Clique em "backend"

### 4️⃣ Encontrar Volumes/Storage
**Opção A - Aba "Variables":**
- Clique na aba "Variables"
- Role para baixo
- Procure por "Storage" ou "Volumes"

**Opção B - Menu Lateral:**
- No menu à esquerda, procure por "Storage" 
- Ou "Volumes"

### 5️⃣ Criar Novo Volume
- Botão: "+ Add Volume" ou "New Storage"
- Campo **Mount Path**: `/app/backend`
- Clique em "Save" ou "Create"

### 6️⃣ Redeploy
- Após salvar, sistema vai pedir para fazer deploy
- Clique em "Redeploy" ou "Deploy Changes"
- Aguarde 2-3 minutos

---

## ✅ Verificação Final

Depois do deploy:
1. Vá em Backend → Variables
2. Procure por "Volumes" ou "Storage"
3. Você deve ver:
   ```
   Storage
   Mount: /app/backend
   Size: [tamanho em GB]
   ```

4. ✅ Volume está configurado!

---

## Se Não Encontrar a Opção de Volume

**Pode ser que:**
- A aba esteja em outro local (experiência do usuário varia por conta)
- Clique em "Settings" do backend service
- Procure por "Storage", "Volumes", ou "Persistent Data"

**Ou use a alternativa CLI:**
```bash
npm install -g @railway/cli
railway login
railway volume create racket_hero_data /app/backend
railway redeploy
```

---

## Dúvidas Frequentes

**P: Onde fico após o deploy?**
R: Os arquivos estarão em `/app/backend/racket_hero.db` no volume persistente

**P: Quanto custa adicionar um volume?**
R: Railway oferece **5GB gratuitos** por serviço

**P: Posso ver os arquivos do volume?**
R: Não pela web, mas você pode via SSH ou CLI

**P: E se eu quiser resetar os dados?**
R: Delete o volume e redeploy. O seed criará dados novos

