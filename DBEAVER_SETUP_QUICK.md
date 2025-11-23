# Como Usar a URL PostgreSQL no DBeaver

## 🔍 Sua URL JDBC:
```
jdbc:postgresql://postgresql://postgres:ubXmOXNUzzsiJjNcwessnSXpWIJOKNtT@metro.proxy.rlwy.net:29879/railway:5432/postgres
```

## ✅ Extrair Credenciais Corretas

### Credenciais Limpas:
- **Host:** `metro.proxy.rlwy.net`
- **Port:** `29879`
- **Username:** `postgres`
- **Password:** `ubXmOXNUzzsiJjNcwessnSXpWIJOKNtT`
- **Database:** `postgres` ou `railway`

---

## 🖥️ Configurar no DBeaver

### Passo 1: Criar Nova Conexão
1. Abra **DBeaver**
2. **Database** → **New Database Connection**
3. Selecione **PostgreSQL**
4. Clique em **Next**

### Passo 2: Preencher Informações

| Campo | Valor |
|-------|-------|
| **Server Host** | `metro.proxy.rlwy.net` |
| **Port** | `29879` |
| **Database** | `postgres` ou `railway` |
| **Username** | `postgres` |
| **Password** | `ubXmOXNUzzsiJjNcwessnSXpWIJOKNtT` |
| **Save password locally** | ✅ Marque |

### Passo 3: Testar Conexão
- Clique em **Test Connection**
- Se aparecer "Connected successfully" ✅ está funcionando!

### Passo 4: Concluir
- Clique em **Finish**

---

## ⚠️ IMPORTANTE: Segurança

**NUNCA compartilhe essa senha!**

Se a compartilhou acidentalmente:
1. Vá no Railway Dashboard
2. Serviço **database** → **Settings**
3. Clique em **"Reset Password"**
4. Railway gerará uma nova senha automaticamente

---

## 🔗 Para o Backend

Use esta URL completa no Railway (variável `DATABASE_URL`):

```
postgresql://postgres:ubXmOXNUzzsiJjNcwessnSXpWIJOKNtT@metro.proxy.rlwy.net:29879/railway
```

---

## ✨ Agora você pode:

✅ Acessar o banco no DBeaver  
✅ Ver todas as tabelas  
✅ Editar dados  
✅ Executar queries SQL  
✅ Fazer backups manuais  

---

## 🎯 Próximo Passo

1. Configure no DBeaver com as credenciais acima
2. Teste a conexão
3. Explore as tabelas (usuario, evento, player, match)
4. Verifique se tem dados de teste

Funcionou? 🚀

