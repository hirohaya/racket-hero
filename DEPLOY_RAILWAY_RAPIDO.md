# 🚀 Deploy Rápido em Railway (30-60 minutos)

**Para quem quer MVP em produção HOJE**

---

## ⚡ Quick Summary

- **Tempo:** 30-60 minutos
- **Custo:** Grátis (até 5GB)
- **Complexidade:** Muito fácil
- **Resultados:** Produção ao vivo

---

## 🎯 Pré-requisitos

✅ Conta GitHub (você tem)  
✅ Dockerfile (já criado)  
✅ docker-compose.yml (já criado)  
✅ FASE 1 commitada (✅ feito!)

---

## 📋 Passo a Passo

### **Passo 1: Criar Conta Railway (5 min)**

1. Ir para https://railway.app
2. Clique em "Sign in with GitHub"
3. Authorize "Railway" no GitHub
4. Você será redirecionado para dashboard

### **Passo 2: Criar Novo Projeto (2 min)**

1. No dashboard, clique "New Project"
2. Selecione "Deploy from GitHub repo"
3. Escolha "racket-hero" do seu GitHub
4. Railway começará build automático

### **Passo 3: Esperar Build (5-10 min)**

Railway vai:
1. ✅ Clonar seu repo
2. ✅ Executar Dockerfile
3. ✅ Build frontend (Node)
4. ✅ Setup backend (Python)
5. ✅ Iniciar container

**Monitore em:** https://railway.app → Dashboard

### **Passo 4: Configurar Variáveis de Ambiente (2 min)**

No Railway Dashboard:
1. Vá para "Variables"
2. Adicione (se não estiverem):
   ```
   DATABASE_URL=sqlite:///./racket_hero.db
   CORS_ORIGINS=https://your-railway-url.railway.app
   LOG_LEVEL=info
   ```

### **Passo 5: Validar Health Check (2 min)**

1. Espere container estar "Running"
2. Copie o URL (ex: https://racket-hero-production.railway.app)
3. Abra em browser:
   ```
   https://your-railway-url/health
   ```
4. Deve retornar:
   ```json
   {
     "status": "ok",
     "message": "Racket Hero API is running",
     "version": "1.0.0",
     "timestamp": "2025-11-19T..."
   }
   ```

### **Passo 6: Validar Database (1 min)**

```
https://your-railway-url/health/db
```

Deve retornar algo como:
```json
{
  "status": "ok",
  "api": {"status": "ok", "version": "1.0.0"},
  "database": {
    "status": "ok",
    "message": "Database connection successful"
  },
  "timestamp": "2025-11-19T..."
}
```

### **Passo 7: Acessar API (1 min)**

1. Vá para:
   ```
   https://your-railway-url/docs
   ```
2. Veja todos os endpoints (Swagger)
3. Teste criar uma conta:
   - POST /api/auth/register
   - Email: test@example.com
   - Nome: Test User
   - Senha: password123456

### **Passo 8: (Opcional) Configurar Domínio Próprio (5 min)**

No Railway:
1. Vá para "Settings"
2. Em "Custom Domain"
3. Adicione seu domínio (ex: api.seu-site.com)
4. Configure DNS conforme instruções

---

## 🎯 Troubleshooting

### Problema: Build falha
```
❌ Error: Cannot find module
```
**Solução:** Verifique se requirements.txt está na raiz ou corrija path no Dockerfile

### Problema: Container crashes
```
❌ CrashLoopBackOff
```
**Solução:** 
1. Verifique logs em Railway Dashboard
2. Cheque variáveis de ambiente
3. Valide Dockerfile localmente

### Problema: /health retorna 502
```
❌ Bad Gateway
```
**Solução:**
1. Espere 30s mais (boot inicial lento)
2. Cheque se container está Running
3. Veja logs para erro

### Problema: Banco de dados não persiste
```
❌ Data lost after restart
```
**Solução:** 
1. Railway não persiste SQLite por padrão
2. Use PostgreSQL Railway (grátis)
3. Ou implemente backup automático

---

## 📊 Monitorar Produção

### Acessar Logs
1. Railway Dashboard → Logs tab
2. Ver output de requests
3. Procurar erros

### Acessar Métricas
1. Railway Dashboard → Metrics tab
2. Ver CPU, Memory, Network
3. Validar performance

### Testar Endpoints
```bash
# Health
curl https://your-railway-url/health

# API Docs
https://your-railway-url/docs

# Testar Create Event
curl -X POST https://your-railway-url/api/events \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","date":"2025-11-20","time":"10:00"}'
```

---

## ✅ Checklist de Produção

- [ ] Railway account criada
- [ ] Projeto deployado
- [ ] Build completo (✅ verde em dashboard)
- [ ] Container rodando (✅ status "Running")
- [ ] /health retorna 200 OK
- [ ] /health/db retorna 200 OK
- [ ] API docs acessível em /docs
- [ ] Criou conta teste (register endpoint)
- [ ] Fez login (test com conta criada)
- [ ] Logs monitorados
- [ ] Domínio configurado (opcional)

---

## 🎁 Próximos Passos Após Deploy

### Imediato (1 dia):
- [ ] Compartilhar URL com usuários
- [ ] Coletar feedback
- [ ] Monitorar logs de erro

### Esta Semana:
- [ ] Implementar FASE 2 (em paralelo)
- [ ] Adicionar logging estruturado
- [ ] Setup alertas no Railway

### Próximas Semanas:
- [ ] Migrar de SQLite → PostgreSQL
- [ ] Setup backup automático
- [ ] Implementar CI/CD mais avançado

---

## 💰 Custos

| Item | Custo |
|------|-------|
| Railway (básico) | Grátis |
| Railway (5GB+) | ~$5-20/mês |
| Domínio (.com) | ~$12/ano |
| Email (optional) | ~$6/mês |
| Total | ~$5-40/mês |

---

## ⚠️ Observações Importantes

1. **SQLite em Railway:** Não é ideal para produção
   - Limite: ~5GB
   - Sem backup automático
   - Melhor usar PostgreSQL depois

2. **Cold Starts:** Primeiro acesso pode ser lento
   - Railway dorme containers inativos
   - 2-3 segundos de boot
   - Upgrade resolve (pago)

3. **Backup:** Configure backup diário
   - Importante para dados do usuário
   - Railway oferece snapshots
   - Ou implementar backup_manager.py

4. **CORS:** Validar configuração CORS
   - Frontend e backend mesmo domínio
   - Se diferentes, ajustar CORS_ORIGINS

---

## 🚀 COMECE AGORA

1. Abra: https://railway.app
2. Login com GitHub
3. Deploy racket-hero
4. Espere 10 minutos
5. Teste /health
6. 🎉 Está em produção!

---

## 📞 Dúvidas?

**P: Pode testar antes de publicar para usuários?**  
R: Sim! Teste em Railway antes de compartilhar URL.

**P: Como fazer rollback se der problema?**  
R: Railway mantém histórico. Clique "Rollback" no Dashboard.

**P: Posso usar meu próprio servidor?**  
R: Sim, mas Railway é mais simples para MVP.

**P: Pode usar Railway grátis indefinidamente?**  
R: Sim, até 5GB. Depois paga conforme uso.

---

**Estimado:** 30-60 minutos até estar em produção ✅

*Boa sorte! 🚀*
