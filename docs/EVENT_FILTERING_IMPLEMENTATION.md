# 🔧 Implementação: Filtro de Eventos por Usuário

**Data**: 15 de Novembro de 2025
**Status**: ✅ IMPLEMENTADO (Aguardando reinicialização do backend)

---

## 📋 Problema Identificado

O jogador de teste podia ver **TODOS os 5 eventos** da aplicação, mas:
- ❌ **NÃO estava registrado em nenhum deles**
- Deve ver apenas os eventos em que está inscrito como jogador

**Dados Encontrados:**
- Total de eventos: 5
- Total de jogadores: 15 + 3 "Jogador Teste"
- Jogador de teste registrado em: Eventos ID 1, 3, 5

---

## ✅ Solução Implementada

### 1. **Modelo de Dados** (`backend/models/player.py`)

Adicionado novo campo para vincular Jogador → Usuário:

```python
usuario_id = Column(Integer, ForeignKey("usuarios.id"), index=True, nullable=True)
```

**Migração executada**: ✅ Campo adicionado com sucesso

### 2. **Database** (Estrutura)

- ✅ Coluna `usuario_id` adicionada à tabela `player`
- ✅ Registros de "Jogador Teste" vinculados ao usuário ID 2
- ✅ Jogador inscrito em 3 eventos: ID 1, 3, 5

**Antes:**
```
EVENTOS: 5 (todos visíveis para jogador)
PLAYERS: 15 (nenhum vinculado ao usuário)
```

**Depois:**
```
EVENTOS: 5 (filtrável por usuário)
PLAYERS: 18 (3 registros do jogador teste vinculados)
```

### 3. **Novo Endpoint** (`backend/routers/events.py`)

Criado `GET /events/meus-eventos` com lógica:

```python
@router.get("/meus-eventos", response_model=List[dict])
async def list_my_events(usuario: Usuario = ...):
    if usuario.tipo in ['organizador', 'admin', ...]:
        # Organizadores/admins veem todos eventos
        return session.query(Event).filter(Event.active == True).all()
    else:
        # Jogadores veem apenas eventos onde estão registrados
        return session.query(Event).join(
            Player, Event.id == Player.event_id
        ).filter(
            Event.active == True,
            Player.usuario_id == usuario.id
        ).all()
```

**Importante**: Esta rota deve estar ANTES de `/{event_id}` para evitar conflito de match.

### 4. **Frontend** (`frontend/src/pages/Events.js`)

Alterado método de carregamento:

**Antes:**
```javascript
const data = await eventsAPI.list();  // GET /events (todos)
```

**Depois:**
```javascript
const data = await eventsAPI.listMyEvents();  // GET /events/meus-eventos (filtrado)
```

### 5. **Service de API** (`frontend/src/services/events.js`)

Adicionado novo método:

```javascript
async listMyEvents() {
  const response = await api.get('/events/meus-eventos');
  return response.data;
}
```

---

## 🧪 Testes Necessários (APÓS REINICIAR BACKEND)

### Teste 1: Jogador vê apenas seus eventos

```
Usuário: jogador@test.com
URL: /eventos
Esperado: 3 eventos (IDs 1, 3, 5)
Status: PRONTO PARA TESTAR
```

### Teste 2: Organizador vê todos eventos

```
Usuário: organizador@test.com
URL: /eventos
Esperado: 5 eventos (todos)
Status: PRONTO PARA TESTAR
```

### Teste 3: Admin vê todos eventos

```
Usuário: admin@test.com
URL: /eventos
Esperado: 5 eventos (todos)
Status: PRONTO PARA TESTAR
```

---

## 🚀 Como Reactivar

### Passo 1: Reiniciar Backend

O backend **DEVE** ser reiniciado para carregar o novo código:

```bash
# Terminal do backend
cd backend/
python main.py
# OU
uvicorn main:app --reload
```

**Status Atual**: Backend ainda está carregando código antigo (reload=False em main.py)

### Passo 2: Testar Endpoint

Após reiniciar, o endpoint estará disponível:

```bash
curl -H "Authorization: Bearer TOKEN" http://localhost:8000/events/meus-eventos
```

### Passo 3: Testar Frontend

Após reiniciar backend, testar no navegador:

1. Login como jogador@test.com
2. Navegar para /eventos
3. Verificar se aparecem apenas 3 eventos

---

## 📊 Matriz de Resultados

| Cenário | Antes | Depois | Status |
|---------|-------|--------|--------|
| Jogador vê 5 eventos | ❌ (problema) | ✅ 3 eventos | Implementado |
| Organizador vê 5 eventos | ✅ | ✅ | Preservado |
| Admin vê 5 eventos | ✅ | ✅ | Preservado |
| Jogador não registrado | Vê eventos | Não vê | ✅ Resolvido |

---

## 📝 Arquivos Modificados

1. **backend/models/player.py**
   - Adicionado campo `usuario_id` com FK

2. **backend/routers/events.py**
   - Novo endpoint `/meus-eventos`
   - Lógica de filtro por usuário
   - Posicionado antes de `/{event_id}`

3. **backend/migrate_player.py**
   - Script de migração (executado ✅)

4. **backend/add_test_player.py**
   - Script para adicionar jogador em eventos (executado ✅)

5. **backend/link_test_player.py**
   - Script para vincular usuário aos registros (executado ✅)

6. **frontend/src/services/events.js**
   - Novo método `listMyEvents()`

7. **frontend/src/pages/Events.js**
   - Alterado para usar `listMyEvents()` em vez de `list()`

---

## ⚠️ Próximas Implementações Recomendadas

- [ ] Adicionar campo `usuario_id` obrigatório (nullable=False)
- [ ] Criar endpoint para registrar jogador em evento (POST /events/:id/register)
- [ ] Adicionar UI para "Inscrever-se em evento"
- [ ] Implementar permissões por proprietário de evento
- [ ] Adicionar filtro de "Eventos que não sou membro" para organizar convites

---

## ✅ Checklist de Implementação

- [x] Adicionar campo `usuario_id` ao modelo Player
- [x] Migrar banco de dados
- [x] Registrar jogador de teste em eventos
- [x] Vincular registros ao usuário
- [x] Criar endpoint `/meus-eventos`
- [x] Atualizar frontend para usar novo endpoint
- [x] Documentar mudanças
- [ ] **PRÓXIMO**: Reiniciar backend
- [ ] Testar com jogador
- [ ] Testar com organizador
- [ ] Testar com admin

---

## 🔐 Segurança

✅ **Backend seguro**:
- Permissão `VER_EVENTOS` obrigatória
- Jogadores filtrados por `usuario_id`
- Organizadores/admins sem filtro

✅ **Frontend seguro**:
- Chamada ao endpoint correto
- Sem hard-coding de IDs

---

**Status Final**: ✅ Implementação completa, aguardando reinicialização do backend para testes
