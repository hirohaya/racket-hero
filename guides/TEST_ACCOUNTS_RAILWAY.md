# Contas de Teste - Racket Hero Railway

## 🔐 Contas Disponíveis

### 1️⃣ Organizador
- **Email:** `organizador@test.com`
- **Senha:** `Senha123!`
- **Tipo:** Organizador de Eventos
- **Função:** Pode criar eventos, gerenciar jogadores e partidas

### 2️⃣ Jogador Principal
- **Email:** `jogador@test.com`
- **Senha:** `Senha123!`
- **Tipo:** Jogador
- **Função:** Pode participar de eventos

### 3️⃣ Jogadores Adicionais (para teste de busca e partidas)

| Nome | Email | Senha |
|------|-------|-------|
| João Silva | joao.silva@example.com | Senha123! |
| Maria Santos | maria.santos@example.com | Senha123! |
| Pedro Oliveira | pedro.oliveira@example.com | Senha123! |
| Ana Costa | ana.costa@example.com | Senha123! |
| Lucas Ferreira | lucas.ferreira@example.com | Senha123! |
| Patricia Alves | patricia.alves@example.com | Senha123! |
| Roberto Gomes | roberto.gomes@example.com | Senha123! |
| Juliana Rocha | juliana.rocha@example.com | Senha123! |
| Bruno Martins | bruno.martins@example.com | Senha123! |
| Camila Ribeiro | camila.ribeiro@example.com | Senha123! |

---

## 🚀 Como Adicionar as Contas de Teste

### Método 1: Via Endpoint (Recomendado) ✅

1. Vá em seu app: `https://seu-app.up.railway.app/docs`
2. Procure por **`POST /admin/seed-test-data`**
3. Clique em **"Try it out"**
4. Clique em **"Execute"**
5. Se aparecer `"status": "success"` ✅ contas foram criadas!

### Método 2: Acesso via DBeaver

Se preferir adicionar manualmente:

```sql
-- Inserir organizador
INSERT INTO usuario (email, nome, senha_hash, tipo, ativo, criado_em)
VALUES (
  'organizador@test.com',
  'Organizador Teste',
  '$2b$12$...', -- hash de Senha123!
  'ORGANIZADOR',
  true,
  NOW()
);

-- Inserir jogadores
INSERT INTO usuario (email, nome, senha_hash, tipo, ativo, criado_em)
VALUES
  ('jogador@test.com', 'Jogador Teste', '$2b$12$...', 'JOGADOR', true, NOW()),
  ('joao.silva@example.com', 'João Silva', '$2b$12$...', 'JOGADOR', true, NOW());
  -- ... etc
```

---

## 📝 Evento de Teste Automático

Quando as contas são criadas, um evento é gerado:

- **Nome:** Torneio Teste
- **Data:** 2025-12-01
- **Hora:** 14:00
- **Status:** Ativo
- **Organizador:** organizador@test.com
- **Jogadores:** Todos os 11 jogadores de teste

---

## ✅ Verificar se Funcionou

### Via Frontend:
1. Faça login com `organizador@test.com` / `Senha123!`
2. Você verá o evento "Torneio Teste"
3. Clique no evento e veja os 11 jogadores

### Via DBeaver:
1. Conecte ao PostgreSQL
2. Execute:
   ```sql
   SELECT COUNT(*) as total_usuarios FROM usuario;
   SELECT * FROM usuario LIMIT 15;
   SELECT * FROM evento;
   SELECT * FROM player;
   ```

---

## 🔒 Segurança

⚠️ **IMPORTANTE:**
- Essas contas são **APENAS para teste/desenvolvimento**
- **NUNCA use em produção com dados reais**
- Se compartilhou as credenciais, resete as senhas:
  - Via DBeaver: Update senha_hash
  - Via endpoint: DELETE FROM usuario WHERE email = 'xxx@xxx.com'

---

## 🎯 Casos de Teste

Com essas contas, você pode testar:

✅ **Login:**
- Fazer login como organizador
- Fazer login como jogador

✅ **Eventos:**
- Criar novo evento
- Editar evento "Torneio Teste"
- Visualizar eventos

✅ **Jogadores:**
- Buscar jogadores por nome
- Adicionar jogador a evento
- Remover jogador de evento

✅ **Partidas:**
- Criar partida entre 2 jogadores
- Editar resultado
- Deletar partida
- Ver ranking atualizado

✅ **Ranking:**
- Ver ranking do evento
- Verificar ELO dos jogadores
- Histórico de partidas

---

## 🔗 Endpoints Úteis

### Para Seed Manual:
```
POST /admin/seed-test-data
```

### Para Criar Tabelas (se necessário):
```
POST /admin/create-tables
```

### Para Health Check:
```
GET /health
GET /health/db
```

---

## 📞 Troubleshooting

### Erro: "Email já existe"
**Solução:** As contas já foram criadas. Faça login com uma delas.

### Erro: "Tabelas não existem"
**Solução:** 
1. Execute `POST /admin/create-tables` primeiro
2. Depois `POST /admin/seed-test-data`

### Erro: "Senha inválida"
**Solução:**
1. Copie a senha exatamente como está acima
2. Verifique se não tem espaços extras
3. Senha padrão: `Senha123!`

---

## 🎨 Para Próximos Testes

Após adicionar as contas, você pode:
- [ ] Fazer login como organizador
- [ ] Criar um novo evento
- [ ] Adicionar mais jogadores ao evento
- [ ] Criar partidas entre jogadores
- [ ] Verificar ranking atualizado
- [ ] Testar todas as funcionalidades do app

---

**Status:** ✅ Contas de teste criadas com sucesso no PostgreSQL Railway!

