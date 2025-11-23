# Migração para PostgreSQL - Railway

## ✅ Mudanças Realizadas

### 1. **requirements.txt**
- ✅ Adicionado: `psycopg2-binary==2.9.9` (driver PostgreSQL para Python)

### 2. **database.py**
- ✅ Detecta automaticamente PostgreSQL vs SQLite
- ✅ Usa `NullPool` para PostgreSQL (melhor para conexões em nuvem)
- ✅ Mantém backward compatibility com SQLite local

### 3. **Dockerfile**
- ✅ Adicionado: `postgresql-client` (ferramentas PostgreSQL)
- ✅ Atualizado: `DATABASE_URL` padrão para PostgreSQL

### 4. **railway.toml**
- ✅ Adicionado serviço PostgreSQL automático
- ✅ Configuração de DATABASE_URL dinâmica
- ✅ Variáveis de ambiente do PostgreSQL

---

## 🚀 Como Fazer Deploy no Railway

### Passo 1: Deletar Volume (se tiver)
1. Vá em **Backend** → **Variables**
2. Procure por **Volumes**
3. Delete qualquer volume existente
4. Clique em **Save**

### Passo 2: Fazer Push das Mudanças

```bash
# No seu local (PowerShell)
cd c:\Users\hiros\OneDrive\Documents\projetos\racket-hero
git add requirements.txt backend/database.py Dockerfile railway.toml
git commit -m "feat: migrate from SQLite to PostgreSQL on Railway"
git push origin develop
```

### Passo 3: Deploy Automático no Railway

1. Acesse **https://railway.app**
2. Vá no projeto **racket-hero**
3. Railway detectará automaticamente `railway.toml`
4. **Aguarde 5-10 minutos** para deploy completo

### Passo 4: Verificar Deploy

1. Vá na aba **Deployments** do Backend
2. Procure por: `"Deployment Successful"`
3. Abra a aplicação em seu domínio (geralmente `https://racket-hero.up.railway.app`)

---

## 🔍 Verificar se Está Funcionando

### Via Logs do Backend

1. Backend → aba **Logs**
2. Procure por:
   ```
   [OK] Test data seeded successfully
   [INFO] Application started on 0.0.0.0:8000
   ```

### Via Aplicação Frontend

1. Navegue para seu app
2. Tente:
   - Visualizar eventos ✅
   - Criar um novo evento ✅
   - Adicionar um jogador ✅
   - Criar uma partida ✅
3. **Faça outro deploy**
4. Verifique se os eventos/jogadores ainda existem ✅

---

## 📊 O que Mudou para o Usuário?

**NADA!** 🎉

- ✅ Frontend continua igual
- ✅ APIs continuam iguais
- ✅ Dados persistem automaticamente (melhor que antes!)
- ✅ Sem risco de perder dados em redeploys

---

## 🛠️ Troubleshooting

### Erro: "Could not connect to database"

**Solução:**
1. Railway está criando o PostgreSQL (pode levar 2-3 minutos)
2. Aguarde mais um pouco e faça refresh
3. Verifique se `DATABASE_URL` está definida em **Variables**

### Erro: "No such table"

**Solução:**
1. Banco foi criado mas tabelas não
2. Força um redeploy do backend:
   - Backend → clique em **Redeploy**
3. Aguarde 2-3 minutos

### Dados desapareceram

**Solução:**
1. Verifique se seed está rodando (procure "Test data seeded" nos logs)
2. Se não tiver seed, edite `init_db()` em `database.py`
3. Redeploy

---

## 📈 Benefícios da Migração

| Aspecto | SQLite | PostgreSQL |
|---------|--------|-----------|
| **Persistência** | ⚠️ Depende de volume | ✅ Automática |
| **Performance** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Escalabilidade** | ❌ Limitado | ✅ Ilimitado |
| **Backup** | ⚠️ Manual | ✅ Automático |
| **Segurança** | ⚠️ Arquivo exposto | ✅ Banco protegido |
| **Custo** | Gratuito | Gratuito (Railway) |
| **Múltiplos processos** | ❌ Lock de arquivo | ✅ Conexões independentes |

---

## 🎯 Próximos Passos

1. ✅ Fazer commit das mudanças
2. ✅ Aguardar deploy no Railway (5-10 min)
3. ✅ Testar aplicação no frontend
4. ✅ Criar evento para confirmar persistência
5. ✅ Fazer outro deploy e verificar se evento continua

---

## 📝 Notas Importantes

- **Dados antigos:** Perdidos (novo banco PostgreSQL)
  - Solução: Seed recria dados de teste automaticamente
  
- **Custo:** Railway oferece **5GB gratuitos** de PostgreSQL por mês
  - Se ultrapassar, avisa para upgrade

- **Backups:** Railway faz backups automáticos
  - Acessível via Dashboard → Database → Backups

---

## 🔗 Referências

- [Railway PostgreSQL Docs](https://docs.railway.app/databases/postgresql)
- [SQLAlchemy PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql/)
- [Psycopg2 Docs](https://www.psycopg.org/psycopg2/docs/)

