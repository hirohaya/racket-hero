# Múltiplos Organizadores por Evento

## Resumo da Implementação

Implementado suporte para que **um evento pode ter múltiplos organizadores**. Um organizador pode adicionar outros organizadores ao seu evento.

## Estrutura do Banco de Dados

### Nova Tabela: `evento_organizador`
Tabela de associação muitos-para-muitos entre eventos e organizadores:

```
evento_organizador:
- id (PK)
- event_id (FK para event)
- usuario_id (FK para usuarios)
- criado_em (DATETIME)
- é_criador (INT: 1=criador original, 0=adicionado depois)
```

**Restrições:**
- UNIQUE(event_id, usuario_id) - Evita duplicatas
- Não permite remover o criador original (é_criador = 1)

## Endpoints Implementados

### 1. **GET** `/events/{event_id}/organizadores`
Lista todos os organizadores de um evento.

**Exemplo de Resposta:**
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

### 2. **POST** `/events/{event_id}/organizadores`
Adiciona um novo organizador ao evento.

**Payload:**
```json
{
  "usuario_id": 1
}
```

**Resposta (201):**
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

**Validações:**
- ✅ Verifica se evento existe
- ✅ Verifica se usuário atual é organizador do evento (ou admin)
- ✅ Verifica se novo organizador existe
- ✅ Verifica se já não é organizador (evita duplicatas)
- ❌ Retorna 403 se não é organizador
- ❌ Retorna 404 se evento/usuário não existe
- ❌ Retorna 400 se já é organizador

### 3. **DELETE** `/events/{event_id}/organizadores/{organizador_id}`
Remove um organizador do evento.

**Resposta (200):**
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

**Validações:**
- ✅ Verifica se evento existe
- ✅ Verifica se usuário atual é organizador (ou admin)
- ✅ Protege remoção do criador original (é_criador = 1)
- ❌ Retorna 403 se não é organizador
- ❌ Retorna 404 se evento/organizador não existe
- ❌ Retorna 400 se tenta remover criador

## Fluxo de Permissões

### Ao criar um evento (POST /events):
1. Evento é criado com `usuario_id` do criador
2. Automaticamente registrado na tabela `evento_organizador` com `é_criador = 1`
3. Apenas esse criador (e admins) podem gerenciar outros organizadores

### Ao listar eventos (GET /events/meus-eventos):
- **Jogadores**: Veem eventos onde estão registrados como Player
- **Organizadores**: Veem eventos onde estão registrados como Organizador (tabela evento_organizador)
- **Admins**: Veem todos os eventos

### Permissões no evento:
- **Criador original** (é_criador = 1): Pode gerenciar organizadores, não pode ser removido
- **Organizador adicional** (é_criador = 0): Pode adicionar/remover outros (exceto criador), pode ser removido

## Arquivos Criados/Modificados

### Novos Arquivos:
1. `backend/models/evento_organizador.py` - Modelo da tabela
2. `backend/routers/evento_organizadores.py` - Router com 3 endpoints
3. `backend/migrate_evento_organizador.py` - Script de migração

### Arquivos Modificados:
1. `backend/models/__init__.py` - Importar novo modelo
2. `backend/models/event.py` - Adicionado comentário sobre relacionamento
3. `backend/routers/events.py` - Registrar criador ao criar evento
4. `backend/routers/__init__.py` - Importar novo router
5. `backend/main.py` - Incluir novo router

## Testes Realizados

### Teste 1: Listar organizadores ✅
```
GET /events/1/organizadores
Status: 200
Retorna lista com organizador original + novos
```

### Teste 2: Adicionar novo organizador ✅
```
POST /events/1/organizadores {"usuario_id": 1}
Status: 200
Evento 1 agora tem 2 organizadores:
  - organizador@test.com (criador)
  - admin@test.com (adicionado)
```

### Teste 3: Remover organizador ✅
```
DELETE /events/1/organizadores/1
Status: 200
Evento 1 volta a ter 1 organizador
```

### Teste 4: Proteção de criador ✅
```
DELETE /events/1/organizadores/3
Status: 400
Retorna: "Não é possível remover o criador original do evento"
```

## Estado Atual do Banco

### Distribuição de Organizadores:
- **Evento 1**: 2 organizadores (organizador@test.com [criador], admin@test.com [adicionado])
- **Evento 2-5**: 1 organizador cada (organizador@test.com [criador])

### Próximos Passos (Sugestões):

1. **Frontend**: Criar página de "Gerenciar Organizadores" no detalhe do evento
2. **Frontend**: Adicionar UI com dropdown para selecionar usuários a adicionar
3. **Frontend**: Mostrar lista de organizadores com badges (criador vs adicional)
4. **API**: Endpoint GET /eventos para retornar lista de organizadores em cada evento
5. **API**: Validação de permissões no DELETE /events/{id} baseada em evento_organizador
6. **Database**: Adicionar índices compostos para melhor performance

## Exemplo de Uso

```python
# Login como organizador
POST /api/auth/login
{"email": "organizador@test.com", "senha": "Senha123!"}
# Retorna token

# Listar organizadores do evento 1
GET /events/1/organizadores
Authorization: Bearer {token}

# Adicionar novo organizador
POST /events/1/organizadores
{"usuario_id": 1}
Authorization: Bearer {token}

# Remover organizador
DELETE /events/1/organizadores/1
Authorization: Bearer {token}
```

---

**Status**: ✅ IMPLEMENTADO E TESTADO
**Data**: 18/11/2025
**Desenvolvedor**: GitHub Copilot
