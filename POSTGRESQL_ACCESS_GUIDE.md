# Como Acessar o PostgreSQL no Railway

## 🚀 Método 1: Via Railway Dashboard (Mais Fácil)

### Passo 1: Encontrar as Credenciais
1. Vá para https://railway.app
2. Clique no seu projeto **racket-hero**
3. Procure pelo serviço **database** (PostgreSQL)
4. Clique na aba **"Connect"** ou **"Database"**
5. Você verá:
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

### Passo 2: Copiar a Connection String
- Clique em **"Copy"** ou selecione e copie a URL completa
- **NÃO compartilhe essa URL com ninguém!**

---

## 💻 Método 2: Via pgAdmin (Interface Gráfica) ✅ RECOMENDADO

### Passo 1: Acessar pgAdmin
1. Vá para https://www.pgadmin.org/download/
2. **OU** use a versão online: https://pgadmin.io/

### Passo 2: Conectar ao Banco
1. Abra pgAdmin
2. Clique em **"Add New Server"** (ícone + ou botão)
3. Preencha:
   - **Name:** `Racket Hero DB`
   - **Hostname/address:** (pegar do Railway Dashboard - veja abaixo)
   - **Port:** `5432` (ou o port do Railway)
   - **Username:** `railway` (ou seu user)
   - **Password:** (pegar do Railway)
   - **Database:** `racket_hero`

### Passo 3: Onde Pegar as Credenciais (Railway Dashboard)

1. Backend → **Variables** (lado esquerdo)
2. Procure por: `DATABASE_URL`
3. Parece assim:
   ```
   postgresql://railway:xxxxx@postgres.railway.internal:5432/racket_hero
   ```

4. **Extraia:**
   - **Host:** `postgres.railway.internal`
   - **Port:** `5432`
   - **User:** `railway`
   - **Password:** Está entre `:` e `@` na URL
   - **Database:** `racket_hero`

---

## 🖥️ Método 3: Via Terminal/PowerShell

### Pré-requisito: Instalar PostgreSQL Client

```powershell
# Se tiver Chocolatey:
choco install postgresql

# Ou baixar de: https://www.postgresql.org/download/windows/
```

### Conectar ao Banco

```powershell
# Copie a DATABASE_URL do Railway e use assim:
$env:PGPASSWORD = "SEU_PASSWORD"
psql -h postgres.railway.internal -U railway -d racket_hero -p 5432

# Depois disso, você verá:
# racket_hero=#
```

### Comandos Úteis no psql

```sql
-- Ver todas as tabelas
\dt

-- Ver estrutura de uma tabela
\d usuario

-- Ver dados de uma tabela
SELECT * FROM evento LIMIT 10;

-- Contar registros
SELECT COUNT(*) FROM usuario;

-- Sair
\q
```

---

## 🔍 Método 4: Via DBeaver (Recomendado)

### Passo 1: Baixar DBeaver
- https://dbeaver.io/download/
- Versão **Community Edition** é gratuita

### Passo 2: Criar Nova Conexão
1. Abra DBeaver
2. **Database** → **New Database Connection**
3. Selecione **PostgreSQL**
4. Clique em **Next**

### Passo 3: Configurar Conexão
- **Server Host:** `postgres.railway.internal`
- **Port:** `5432`
- **Database:** `racket_hero`
- **Username:** `railway`
- **Password:** (copie do Railway)

### Passo 4: Testar Conexão
- Clique em **Test Connection**
- Se aparecer "Connected", ✅ está funcionando!

---

## 🌐 Método 5: Via Python (Para Scripts)

### Instalar SQLAlchemy
```bash
pip install sqlalchemy psycopg2-binary
```

### Conectar e Consultar

```python
from sqlalchemy import create_engine, text

# Copie a DATABASE_URL do Railway
database_url = "postgresql://railway:xxxxx@postgres.railway.internal:5432/racket_hero"

engine = create_engine(database_url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuario LIMIT 5"))
    for row in result:
        print(row)
```

---

## 📊 Método 6: Via Flask Shell (No Seu Projeto)

```bash
# No diretório raiz
cd backend

# Ativar variáveis de ambiente do Railway
$env:DATABASE_URL = "postgresql://railway:xxxxx@postgres.railway.internal:5432/racket_hero"

# Entrar no shell Python
python

# Dentro do Python:
from database import SessionLocal
from models.usuario import Usuario

db = SessionLocal()
usuarios = db.query(Usuario).all()
for u in usuarios:
    print(f"{u.nome} - {u.email}")
```

---

## 🔑 Encontrar DATABASE_URL Facilmente

### No Railway Dashboard:

1. Projeto **racket-hero**
2. Serviço **backend**
3. Aba **"Variables"**
4. Procure por `DATABASE_URL` (scroll se necessário)
5. **Copie a URL completa**

### Exemplo de URL:
```
postgresql://railway:abcd1234@postgres.railway.internal:5432/racket_hero
         ↑                ↑                           ↑                ↑
      usuario        password            hostname/endereço         banco
```

---

## ✅ Verificar se Está Funcionando

### Via pgAdmin/DBeaver:
1. Conecte ao banco
2. Navegue em **Databases** → **racket_hero** → **Schemas** → **public**
3. Você deve ver tabelas:
   - `usuario`
   - `evento`
   - `player`
   - `match`
   - `evento_organizador`

### Via SQL:
```sql
-- Listar todas as tabelas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Contar eventos
SELECT COUNT(*) as total_eventos FROM evento;

-- Ver um evento
SELECT * FROM evento LIMIT 1;
```

---

## 🚨 Troubleshooting

### Erro: "Connection refused"
- **Causa:** Host incorreto
- **Solução:** Certifique-se de usar `postgres.railway.internal` (não localhost)

### Erro: "Password authentication failed"
- **Causa:** Senha copiada errada
- **Solução:** Copie novamente do Railway Dashboard

### Erro: "Database does not exist"
- **Causa:** Nome do banco está errado
- **Solução:** Use `racket_hero` (não `postgres` ou outro)

### Erro: "Host is unreachable"
- **Causa:** Pode estar em rede diferente
- **Solução:** 
  1. Verifique se backend está rodando no Railway
  2. Aguarde 2-3 minutos após deploy
  3. Tente novamente

---

## 🔒 Segurança

### ⚠️ NUNCA:
- ❌ Compartilhe a `DATABASE_URL`
- ❌ Commite a senha no Git
- ❌ Use em variáveis de ambiente públicas

### ✅ SEMPRE:
- ✅ Use variáveis de ambiente (Railway faz isso automaticamente)
- ✅ Regenere a senha se comprometida (Railway Dashboard → Database → Settings)
- ✅ Use conexões SSL quando possível

---

## 📋 Resumo Rápido

| Método | Facilidade | Recursos |
|--------|-----------|----------|
| **pgAdmin** | ⭐⭐⭐ Fácil | Ver/editar dados via UI |
| **DBeaver** | ⭐⭐⭐ Fácil | Visual, poderoso, gratuito |
| **psql** | ⭐⭐ Médio | Terminal, rápido |
| **Python** | ⭐⭐ Médio | Scripts, automação |
| **Flask Shell** | ⭐⭐ Médio | Usar modelos ORM |

---

## 🎯 Próximos Passos

1. [ ] Copiar `DATABASE_URL` do Railway
2. [ ] Escolher método de acesso (pgAdmin ou DBeaver recomendado)
3. [ ] Conectar ao banco
4. [ ] Ver tabelas e dados
5. [ ] Testar criar um evento via frontend
6. [ ] Verificar que aparece no banco ✅

---

## 💡 Dica Profissional

Se quiser **acessar do seu computador local**:

1. Instale DBeaver
2. Use a `DATABASE_URL` do Railway
3. Você consegue **editar dados remotamente**
4. Ótimo para debug!

