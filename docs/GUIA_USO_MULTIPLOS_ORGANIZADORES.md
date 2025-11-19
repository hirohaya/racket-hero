aa# Guia de Uso: Gerenciar Múltiplos Organizadores

## 📚 Índice
1. [Visão Geral](#visão-geral)
2. [Endpoints](#endpoints)
3. [Exemplos Práticos](#exemplos-práticos)
4. [Casos de Uso](#casos-de-uso)
5. [Troubleshooting](#troubleshooting)

---

## Visão Geral

### O que mudou?
Antes: Um evento tinha 1 organizador (salvo em `event.usuario_id`)
Depois: Um evento pode ter N organizadores (em tabela `evento_organizador`)

### Quem pode fazer o quê?

| Ação | Criador do Evento | Outro Organizador | Admin | Jogador |
|------|---------|---------|-------|---------|
| Ver organizadores | ✅ | ✅ | ✅ | ❌ |
| Adicionar organizador | ✅ | ✅ | ✅ | ❌ |
| Remover organizador | ✅ | ✅* | ✅ | ❌ |
| Remover a si mesmo | ✅ | ✅ | ✅ | ❌ |
| Remover criador | ❌ | ❌ | ✅ | ❌ |

*Pode remover organizadores adicionados, mas não o criador

---

## Endpoints

### 1. Listar Organizadores
```
GET /events/{event_id}/organizadores
```

**Autenticação**: Requerida (qualquer tipo de usuário)
**Retorna**: Array de organizadores

**Exemplo de Requisição**:
```bash
curl -X GET http://localhost:8000/events/1/organizadores \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Exemplo de Resposta** (200 OK):
```json
[
  {
    "id": 3,
    "email": "organizador@test.com",
    "é_criador": 1,
    "adicionado_em": "2025-11-18T13:39:07.902862"
  },
  {
    "id": 1,
    "email": "admin@test.com",
    "é_criador": 0,
    "adicionado_em": "2025-11-18T16:41:57"
  }
]
```

**Possíveis Erros**:
```json
// 404 - Evento não encontrado
{"detail": "Evento não encontrado"}

// 400 - Erro no banco
{"detail": "Erro ao listar organizadores"}
```

---

### 2. Adicionar Organizador
```
POST /events/{event_id}/organizadores
```

**Autenticação**: Requerida (deve ser organizador do evento ou admin)
**Body**: `{"usuario_id": <int>}`
**Retorna**: Confirmação com dados do novo organizador

**Exemplo de Requisição**:
```bash
curl -X POST http://localhost:8000/events/1/organizadores \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -H "Content-Type: application/json" \
  -d '{"usuario_id": 1}'
```

**Exemplo de Resposta** (200 OK):
```json
{
  "success": true,
  "message": "'admin@test.com' foi adicionado como organizador",
  "evento_id": 1,
  "novo_organizador": {
    "id": 1,
    "email": "admin@test.com",
    "nome": "admin"
  }
}
```

**Possíveis Erros**:
```json
// 404 - Evento não encontrado
{"detail": "Evento não encontrado"}

// 404 - Usuário não encontrado
{"detail": "Usuário não encontrado"}

// 403 - Não é organizador
{"detail": "Você não é organizador deste evento"}

// 400 - Já é organizador
{"detail": "'admin@test.com' já é organizador deste evento"}
```

---

### 3. Remover Organizador
```
DELETE /events/{event_id}/organizadores/{organizador_id}
```

**Autenticação**: Requerida (deve ser organizador do evento ou admin)
**Retorna**: Confirmação da remoção

**Exemplo de Requisição**:
```bash
curl -X DELETE http://localhost:8000/events/1/organizadores/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

**Exemplo de Resposta** (200 OK):
```json
{
  "success": true,
  "message": "'admin@test.com' foi removido como organizador",
  "evento_id": 1,
  "removido": {
    "id": 1,
    "email": "admin@test.com"
  }
}
```

**Possíveis Erros**:
```json
// 404 - Evento não encontrado
{"detail": "Evento não encontrado"}

// 403 - Não é organizador
{"detail": "Você não é organizador deste evento"}

// 404 - Organizador não encontrado no evento
{"detail": "Organizador não encontrado neste evento"}

// 400 - É o criador original
{"detail": "Não é possível remover o criador original do evento"}
```

---

## Exemplos Práticos

### Cenário 1: João quer que Maria organize o torneio com ele

```
1️⃣ João faz login
   POST /api/auth/login
   {"email": "joao@eventos.com", "senha": "Senha123!"}
   → Recebe token JWT

2️⃣ João cria novo evento
   POST /events
   {
     "name": "Campeonato Regional 2025",
     "date": "2025-12-15",
     "time": "19:00"
   }
   → Evento ID 7 criado
   → João automaticamente é organizador (é_criador=1)

3️⃣ João quer adicionar Maria
   POST /events/7/organizadores
   {"usuario_id": 5}  // 5 é o ID de maria@eventos.com
   → Maria agora é organizadora (é_criador=0)

4️⃣ João e Maria podem ver organizadores
   GET /events/7/organizadores
   → Retorna: João (criador) + Maria (adicionada)

5️⃣ Maria pode ver evento em sua lista
   GET /events/meus-eventos
   → Evento 7 aparece porque está registrada em evento_organizador
```

---

### Cenário 2: Removendo um organizador que não quer mais

```
1️⃣ João quer remover Maria
   DELETE /events/7/organizadores/5
   → Sucesso! Maria removida

2️⃣ Verificação
   GET /events/7/organizadores
   → Retorna: Apenas João (criador)

3️⃣ Maria tenta ver eventos
   GET /events/meus-eventos
   → Evento 7 desaparece (não está mais em evento_organizador)
```

---

### Cenário 3: Tentativa de remover o criador (protegido)

```
1️⃣ Maria tenta remover João
   DELETE /events/7/organizadores/3  // 3 é João
   
2️⃣ Resposta com erro (400):
   {
     "detail": "Não é possível remover o criador original do evento"
   }
   
3️⃣ Proteção em ação!
   ✅ Criador não pode ser removido por ninguém
   ✅ Apenas admin pode fazer override (no futuro)
```

---

### Cenário 4: Admin gerenciando organizadores

```
1️⃣ Admin quer ver quem organiza evento 1
   GET /events/1/organizadores
   → Retorna lista de organizadores

2️⃣ Admin adiciona novo organizador
   POST /events/1/organizadores
   {"usuario_id": 2}
   → Sucesso mesmo que admin não seja organizador do evento

3️⃣ Admin remove organizador
   DELETE /events/1/organizadores/2
   → Sucesso, mesmo que seja criador (admin tem privilégio)
```

---

## Casos de Uso

### 📌 Caso 1: Torneio em Equipe
```
Cenário: Evento grande com 5 organizadores

1. Pedro cria evento "Liga Municipal 2025"
2. Pedro adiciona: Ana, Bruno, Carlos, Diana
3. Cada um vê o evento em sua lista
4. Cada um pode fazer ajustes
5. Pedro (criador) tem autoridade final

Segurança: Se alguém sair, Pedro remove
Proteção: Ninguém consegue remover Pedro
```

### 📌 Caso 2: Delegação Gradual
```
Cenário: Márcio quer sair, Jéssica toma conta

Problema: Márcio é criador, não pode ser removido por ele mesmo

Solução 1 (Futura): Admin cria novo criador
Solução 2 (Agora): Márcio fica registrado, mas Jéssica gerencia

Resultado: Jéssica é co-organizadora com permissões totais
```

### 📌 Caso 3: Auditoria
```
Cenário: Rastrear quem criou evento e quem foi adicionado

Query:
GET /events/5/organizadores

Resposta mostra:
- João (é_criador=1, adicionado_em: 2025-11-18)
- Maria (é_criador=0, adicionado_em: 2025-11-20)
- Pedro (é_criador=0, adicionado_em: 2025-11-21)

Conclusão: João criou dia 18, Maria dia 20, Pedro dia 21
```

---

## Troubleshooting

### ❌ "Você não é organizador deste evento"
**Causa**: Tentou adicionar/remover organizador sem ser organizador

**Solução**:
```json
// Verificar se está em evento_organizador
GET /events/{id}/organizadores
// Se seu email não aparecer, você não é organizador
```

**Ação**:
- Peça a um organizador que te adicione
- Ou peça ajuda a um admin

---

### ❌ "Organizador não encontrado neste evento"
**Causa**: Tentou remover alguém que não é organizador do evento

**Solução**:
```json
// Ver lista de organizadores
GET /events/{id}/organizadores
// Copiar o "id" exato do organizador
// Usar esse ID no DELETE
```

---

### ❌ "Não é possível remover o criador original do evento"
**Causa**: Tentou remover quem criou o evento (é_criador=1)

**Resposta**: Isto é esperado e correto!

**Soluções**:
1. Remova outros organizadores (não o criador)
2. Solicite a um admin para fazer override
3. Crie um novo evento e transfira responsabilidades

---

### ❌ "'admin@test.com' já é organizador deste evento"
**Causa**: Tentou adicionar alguém já registrado

**Solução**:
```json
// Verificar lista primeira
GET /events/{id}/organizadores
// Se já existe, não é necessário adicionar novamente
```

---

### ❌ "Evento não encontrado"
**Causa**: ID do evento inválido ou não existe

**Solução**:
```json
// Ver seus eventos
GET /events/meus-eventos
// Usar um ID da lista retornada
```

---

### ⚠️ "401 Unauthorized"
**Causa**: Token JWT inválido ou expirado

**Solução**:
```bash
// Fazer login novamente
POST /api/auth/login
{"email": "seu@email.com", "senha": "Senha123!"}
// Usar novo token
```

---

## Dúvidas Frequentes

### P: Jogador pode ver organizadores?
**R**: ❌ Não. Apenas organizadores e admins podem listar.

### P: Posso remover a mim mesmo?
**R**: ✅ Sim, desde que não seja o criador.

### P: Posso transferir criador para outro?
**R**: ❌ Ainda não. Será feature futura.

### P: Qual é a diferença entre é_criador=1 e é_criador=0?
**R**: é_criador=1 não pode ser removido (proteção). é_criador=0 pode ser removido.

### P: Um usuário pode estar em vários eventos?
**R**: ✅ Sim, pode ser organizador em 0, 1 ou vários eventos.

### P: O que acontece se deletarem um usuário?
**R**: Registros em evento_organizador ficarão órfãos. Seria necessário limpar.

---

## Resumo Rápido

| Ação | Endpoint | Método |
|------|----------|--------|
| Listar | `/events/{id}/organizadores` | GET |
| Adicionar | `/events/{id}/organizadores` | POST |
| Remover | `/events/{id}/organizadores/{org_id}` | DELETE |

**Exemplo**:
```bash
# Listar
curl GET http://localhost:8000/events/1/organizadores -H "Auth: Bearer ..."

# Adicionar
curl POST http://localhost:8000/events/1/organizadores \
  -d '{"usuario_id": 5}' -H "Auth: Bearer ..."

# Remover
curl DELETE http://localhost:8000/events/1/organizadores/5 -H "Auth: Bearer ..."
```

---

**Versão**: 1.0.0
**Data**: 18 de Novembro de 2025
**Status**: ✅ Completo
