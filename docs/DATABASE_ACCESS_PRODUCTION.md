# 📊 Guia de Acesso ao Banco de Dados em Produção - Racket Hero

## 🎯 Visão Geral

O Racket Hero usa **SQLite** como banco de dados padrão. Em produção no Railway, o banco está armazenado como arquivo no container.

---

## 📍 Localização do Banco em Produção

```
Container Railway
├── /app/
│   ├── backend/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── racket_hero.db  ← BANCO DE DADOS
│   ├── frontend/build/
│   └── logs/
```

**Caminho**: `/app/racket_hero.db` (dentro do container)

---

## 🔌 Métodos de Acesso

### 1️⃣ Via API HTTP (Recomendado)

A forma mais segura de acessar os dados é através da **API HTTP**.

#### Endpoints Disponíveis

```bash
# Health check
GET /health

# Autenticação
POST /api/auth/register     # Criar novo usuário
POST /api/auth/login        # Login (retorna JWT token)

# Eventos
GET  /api/events            # Listar eventos
POST /api/events            # Criar evento
GET  /api/events/{id}       # Detalhe do evento

# Jogadores
GET  /api/players           # Listar jogadores
POST /api/players           # Adicionar jogador
GET  /api/players/{id}      # Detalhe do jogador

# Partidas
GET  /api/matches           # Listar partidas
POST /api/matches           # Registrar partida
GET  /api/ranking           # Ranking ELO
```

#### Exemplo com cURL

```bash
# 1. Login
curl -X POST https://seu-app.railway.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com", "password":"Senha123!"}'

# Resposta
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user_id": "550e8400-..."
}

# 2. Usar token para acessar dados
TOKEN="eyJhbGc..."

curl -X GET https://seu-app.railway.app/api/events \
  -H "Authorization: Bearer $TOKEN"
```

#### Exemplo com Python

```python
import requests
import json

BASE_URL = "https://seu-app.railway.app"

# 1. Login
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={"email": "admin@test.com", "password": "Senha123!"}
)
token = login_response.json()["access_token"]

# 2. Buscar eventos
headers = {"Authorization": f"Bearer {token}"}
events = requests.get(
    f"{BASE_URL}/api/events",
    headers=headers
)

print(json.dumps(events.json(), indent=2))
```

---

### 2️⃣ Via SSH + SQLite CLI (Acesso Direto)

Para acesso direto ao arquivo do banco.

#### Pré-requisitos
- SSH access ao Railway
- `sqlite3` CLI instalado localmente

#### Passos

```bash
# 1. Obter connection string do Railway
# Railway Dashboard → seu-projeto → Connect → SSH

# 2. Conectar via SSH
ssh -i ~/.ssh/id_rsa user@railway-host

# 3. Dentro do container, acessar o banco
cd /app
sqlite3 racket_hero.db

# 4. Comandos SQL
sqlite> SELECT * FROM usuario;
sqlite> SELECT * FROM event;
sqlite> SELECT * FROM player;
sqlite> SELECT * FROM match;

# 5. Sair
sqlite> .exit
```

---

### 3️⃣ Via Script Python (Download & Análise)

Para extrair dados do banco em produção.

```python
#!/usr/bin/env python3
"""
extract_production_data.py - Extrai dados do banco de produção
Conecta ao Railway via SSH e faz backup dos dados
"""

import subprocess
import sqlite3
import json
from datetime import datetime

def get_ssh_connection():
    """Obtém string SSH do Railway (copiar do dashboard)"""
    return "ssh -i ~/.ssh/id_rsa user@your-railway-host"

def query_remote_database(sql):
    """Executa query no banco remoto"""
    cmd = f'{get_ssh_connection()} "cd /app && sqlite3 racket_hero.db \\"{sql}\\""'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def export_all_data():
    """Exporta todos os dados em JSON"""
    data = {}
    
    # Usuarios
    usuarios_json = query_remote_database("SELECT * FROM usuario;")
    # ... parse JSON
    
    # Events
    events_json = query_remote_database("SELECT * FROM event;")
    
    # Players
    players_json = query_remote_database("SELECT * FROM player;")
    
    # Matches
    matches_json = query_remote_database("SELECT * FROM match;")
    
    # Salvar em arquivo
    with open(f"backup_{datetime.now().isoformat()}.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("✅ Dados exportados com sucesso!")

if __name__ == "__main__":
    export_all_data()
```

---

### 4️⃣ Via Railway Dashboard

**Opção mais simples** para visualização rápida.

```
1. Acessar railway.app
2. Clicar no projeto "racket-hero"
3. Abrir aba "Deployments"
4. Clicar em "View Logs"
5. Clicar em "Connect" (SSH)
6. Executar: sqlite3 /app/racket_hero.db
```

---

## 🔐 Segurança ao Acessar o Banco

### ✅ Boas Práticas

1. **Use HTTPS** para toda comunicação HTTP
2. **Nunca** compartilhe JWT tokens em logs
3. **Sempre** use variáveis de ambiente para credenciais
4. **Faça backup** antes de fazer alterações diretas
5. **Use readonly** para queries de auditoria

### ❌ Evitar

- Expor DATABASE_URL em logs públicos
- Usar SSH sem autenticação por chave
- Acessar banco sem autenticação prévia
- Modificar dados diretamente no SQLite (sempre use API)

---

## 📊 Estrutura do Banco de Dados

```sql
-- Usuários (Autenticação)
CREATE TABLE usuario (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    nome TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    tipo TEXT,  -- 'admin', 'organizador', 'jogador'
    criado_em DATETIME,
    atualizado_em DATETIME
);

-- Eventos (Torneios)
CREATE TABLE event (
    id INTEGER PRIMARY KEY,
    organizador_id TEXT FOREIGN KEY,
    nome TEXT NOT NULL,
    data TEXT,  -- YYYY-MM-DD
    hora TEXT,  -- HH:MM
    ativo BOOLEAN,
    criado_em DATETIME
);

-- Jogadores
CREATE TABLE player (
    id INTEGER PRIMARY KEY,
    event_id INTEGER FOREIGN KEY,
    nome TEXT NOT NULL,
    clube TEXT,
    elo_inicial FLOAT,
    elo_atual FLOAT,
    criado_em DATETIME
);

-- Partidas
CREATE TABLE match (
    id INTEGER PRIMARY KEY,
    event_id INTEGER FOREIGN KEY,
    player_1_id INTEGER FOREIGN KEY,
    player_2_id INTEGER FOREIGN KEY,
    winner_id INTEGER FOREIGN KEY,
    elo_player_1 FLOAT,
    elo_player_2 FLOAT,
    criado_em DATETIME
);
```

---

## 🔍 Queries Úteis

### Ver Todos os Usuários
```sql
SELECT id, nome, email, tipo FROM usuario;
```

### Listar Eventos Ativos
```sql
SELECT id, nome, data, hora FROM event WHERE ativo = 1;
```

### Ranking de Jogadores (ELO)
```sql
SELECT 
    nome,
    elo_atual,
    ROW_NUMBER() OVER (ORDER BY elo_atual DESC) as ranking
FROM player
ORDER BY elo_atual DESC;
```

### Histórico de Partidas
```sql
SELECT 
    m.id,
    p1.nome as player_1,
    p2.nome as player_2,
    CASE WHEN m.winner_id = p1.id THEN p1.nome ELSE p2.nome END as vencedor,
    m.criado_em
FROM match m
JOIN player p1 ON m.player_1_id = p1.id
JOIN player p2 ON m.player_2_id = p2.id
ORDER BY m.criado_em DESC;
```

### Contar Partidas por Evento
```sql
SELECT 
    e.nome,
    COUNT(m.id) as total_partidas,
    COUNT(DISTINCT m.player_1_id) + COUNT(DISTINCT m.player_2_id) as jogadores
FROM event e
LEFT JOIN match m ON e.id = m.event_id
GROUP BY e.id;
```

---

## 🔄 Backup & Restore

### Fazer Backup

```bash
# Via SSH
ssh user@railway-host "cd /app && sqlite3 racket_hero.db .dump > backup.sql"

# Copiar para local
scp user@railway-host:/app/backup.sql ./backup_$(date +%Y%m%d).sql
```

### Restaurar de Backup

```bash
# Via SSH
ssh user@railway-host "cd /app && sqlite3 racket_hero.db < backup.sql"
```

### Backup Automático

O sistema tem **backup automático** configurado via `backup_manager.py`:

```bash
# Ver backups disponíveis
curl -X GET https://seu-app.railway.app/api/admin/backups \
  -H "Authorization: Bearer $TOKEN"

# Restaurar um backup
curl -X POST https://seu-app.railway.app/api/admin/backups/{filename}/restore \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🚨 Troubleshooting

### Erro: "No such table: usuario"
```
Causa: Banco não inicializado
Solução: Aguarde 30s após deploy, ou force reinicialização
```

### Erro: "database is locked"
```
Causa: Múltiplas conexões simultâneas (SQLite limitation)
Solução: Railway reiniciará o container automaticamente
```

### Erro: "FOREIGN KEY constraint failed"
```
Causa: Inserir dados que violam relações
Solução: Sempre usar API (faz validação automática)
```

---

## 📞 Contato & Suporte

Para acessar o banco de produção:

1. **Local Development**: `sqlite3 backend/racket_hero.db`
2. **Railway Production**: Use SSH ou API
3. **Via API**: Qualquer endpoint HTTP com token JWT

---

**Última atualização**: 2025-11-19  
**Versão**: 1.0 (SQLite MVP)  
**Próximos passos**: Migrar para PostgreSQL em v2.0 (se necessário)
