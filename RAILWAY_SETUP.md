# 🚀 Railway Setup - Guia Prático

Este diretório contém toda a configuração necessária para fazer deploy no Railway.

## 📁 Arquivos de Configuração

### `railway.toml`
- Define como o Railway detecta e constrói seus serviços
- Configura healthchecks automáticos
- Detecta portas automaticamente

### `Procfile`
- Define comandos de start para backend e frontend
- Usado pelo Railway para iniciar aplicações

### `.env.railway`
- Variáveis de ambiente para produção no Railway
- **IMPORTANTE:** Não comita senhas reais, use Railway dashboard para isso

## 🎯 Próximos Passos

### 1️⃣ Preparar Repositório GitHub
```bash
# Já feito! Seus arquivos estão prontos no repo
git add railway.toml Procfile .env.railway
git commit -m "Feat: Add Railway deployment configuration"
git push origin main
```

### 2️⃣ Criar Conta Railway
1. Abra https://railway.app
2. Clique **"Start Coding Now"**
3. Selecione **"Continue with GitHub"**
4. Autorize Railway a acessar seu GitHub

### 3️⃣ Conectar Repositório
1. No dashboard Railway, clique **"Import from GitHub"**
2. Procure por `racket-hero`
3. Clique para importar

### 4️⃣ Criar Serviços (Automático)
Railway detectará automaticamente:
- ✅ Backend (FastAPI)
- ✅ Frontend (React)

### 5️⃣ Configurar Variáveis de Ambiente
No dashboard Railway, para cada serviço:

**Backend:**
```
DATABASE_URL=sqlite:///./racket_hero.db
CORS_ORIGINS=["https://seu-frontend-xxx.railway.app"]
LOG_LEVEL=INFO
ENVIRONMENT=production
SECRET_KEY=gere-uma-chave-segura
```

**Frontend:**
```
REACT_APP_API_URL=https://seu-backend-xxx.railway.app
NODE_ENV=production
```

### 6️⃣ Deploy Automático
1. Railway detecta qualquer push para `main`
2. Faz build automático
3. Deploy da nova versão
4. Tudo pronto! 🎉

## 📊 Estrutura do Projeto

```
racket-hero/
├── railway.toml          ← Configuração Railway
├── Procfile              ← Comandos de start
├── .env.railway          ← Variáveis de ambiente
├── backend/
│   ├── main.py           ← FastAPI app
│   ├── requirements.txt   ← Dependências Python
│   └── ...
└── frontend/
    ├── package.json      ← Dependências Node
    ├── src/
    └── ...
```

## 🔍 Monitoramento

### Ver Logs em Tempo Real
1. Dashboard Railway → Seu serviço
2. Aba **"Logs"**
3. Scroll para ver novos eventos

### Checar Saúde
```bash
curl https://seu-backend-xxx.railway.app/health
```

### Reiniciar Serviço
1. Dashboard → Serviço
2. Clique **"⋮"** (3 pontos)
3. Selecione **"Restart"**

## 💰 Custos

**Free Tier Railway:**
- ✅ $5 crédito mensalmente (gratuito)
- ✅ Suficiente para MVP
- ✅ Sem necessidade de cartão de crédito

## 🆘 Troubleshooting

### Backend não inicia
1. Verifique logs no Railway
2. Teste localmente: `cd backend && python main.py`
3. Procure por erro de import ou syntax

### Frontend não carrega
1. Verifique `REACT_APP_API_URL` está certo
2. Abra console do navegador (F12)
3. Procure por erro de fetch/CORS

### CORS Error
1. Atualize `CORS_ORIGINS` no backend
2. Inclua URL do frontend publicado
3. Redeploy (push para GitHub)

## 📚 Recursos

- [Railway Docs](https://docs.railway.app/)
- [Seu Dashboard Railway](https://railway.app/dashboard)
- [Documentação FastAPI](https://fastapi.tiangolo.com/)
- [Documentação React](https://react.dev/)

## 🎓 Próximas Ações

### Hoje
- ✅ Arquivos de config criados
- [ ] Push para GitHub
- [ ] Criar conta Railway
- [ ] Conectar GitHub ao Railway
- [ ] Primeiro deploy

### Esta Semana
- [ ] Testar com usuários
- [ ] Monitorar logs
- [ ] Ajustar performance se needed

---

**Status:** 🟢 Pronto para deploy no Railway!

Quer começar? 👉 Siga os "Próximos Passos" acima!
