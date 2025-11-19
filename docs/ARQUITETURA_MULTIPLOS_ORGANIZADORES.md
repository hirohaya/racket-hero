# Arquitetura de Múltiplos Organizadores

## Diagrama de Relacionamento

```
usuarios (id, email, tipo)
    ↓
    ├→ event (id, name, usuario_id*)
    │   ↓
    │   └→ evento_organizador (event_id FK, usuario_id FK)
    │
    └→ evento_organizador (usuario_id FK, event_id FK)

* usuario_id em event é mantido para backward compatibility
  mas agora é redundante com evento_organizador (criador)
```

## Fluxo de Dados

### Criar Evento:
```
Organizador (ID 3) → POST /events
  ↓
1. Criar registro em table event (usuario_id = 3)
2. Criar registro em evento_organizador (usuario_id=3, é_criador=1)
  ↓
Resultado: Evento com 1 organizador (criador)
```

### Adicionar Organizador:
```
Organizador (ID 3) → POST /events/1/organizadores {"usuario_id": 1}
  ↓
1. Verificar se ID 3 é organizador do evento 1 ✓
2. Verificar se ID 1 é um usuário válido ✓
3. Verificar se ID 1 já não é organizador do evento 1 ✓
4. Criar registro em evento_organizador (usuario_id=1, é_criador=0)
  ↓
Resultado: Evento 1 tem 2 organizadores
```

### Listar Organizadores:
```
GET /events/1/organizadores
  ↓
SELECT * FROM evento_organizador WHERE event_id=1
JOIN usuarios ON evento_organizador.usuario_id = usuarios.id
  ↓
Retorna lista com nome, email, é_criador, data_adicionado
```

### Remover Organizador:
```
Organizador (ID 3) → DELETE /events/1/organizadores/1
  ↓
1. Verificar se ID 3 é organizador do evento 1 ✓
2. Verificar se ID 1 é organizador do evento 1 ✓
3. Verificar se ID 1 é criador (é_criador=1) ❌ PROTEGIDO
4. Deletar registro de evento_organizador
  ↓
Resultado: Evento 1 volta a ter 1 organizador
```

## Modelo de Dados

```sql
CREATE TABLE evento_organizador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    usuario_id INTEGER NOT NULL,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    é_criador INTEGER DEFAULT 0,
    FOREIGN KEY (event_id) REFERENCES event(id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    UNIQUE(event_id, usuario_id)
);
```

## Permissões por Tipo de Usuário

### Jogador (tipo=0):
- ❌ Criar evento
- ✅ Ver eventos em que está registrado
- ❌ Editar/deletar eventos
- ❌ Gerenciar organizadores

### Organizador (tipo=1):
- ✅ Criar evento (vira criador)
- ✅ Ver apenas seus eventos
- ✅ Editar/deletar seus eventos
- ✅ Adicionar organizadores
- ✅ Remover organizadores (exceto ele mesmo se criador)
- ❌ Remover criador original

### Admin (tipo=2):
- ✅ Ver TODOS eventos
- ✅ Pode atuar como organizador em qualquer evento
- ✅ Gerenciar organizadores de qualquer evento
- ✅ Remover criadores (com cuidado)

## Casos de Uso

### Caso 1: Evento com múltiplos organizadores
```
1. João (org) cria evento "Campeonato XYZ"
   → João vira criador (é_criador=1)

2. João adiciona Maria e Pedro como organizadores
   → Maria e Pedro têm (é_criador=0)

3. Maria vê o evento em sua lista
4. Maria pode adicionar outro organizador
5. Maria NÃO pode remover João (proteção ao criador)
6. João pode remover Maria ou Pedro quando quiser
```

### Caso 2: Organização em equipe
```
1. Evento grande precisa de 5 organizadores
2. Criador adiciona os 4 outros
3. Cada um vê o evento em sua lista
4. Cada um pode fazer ajustes
5. Criador tem controle final
```

### Caso 3: Transferência de responsabilidade
```
1. João (criador) não quer mais gerenciar
2. Solução: Remover outros, deixar só Maria
3. Problema: Não consegue remover ele mesmo
4. Alternativa: Admin pode transferir criador (future)
```

## Queries Úteis

```sql
-- Todos os organizadores de um evento
SELECT u.email, eo.é_criador, eo.criado_em
FROM evento_organizador eo
JOIN usuarios u ON eo.usuario_id = u.id
WHERE eo.event_id = 1
ORDER BY eo.é_criador DESC, eo.criado_em ASC;

-- Todos os eventos que um usuário organiza
SELECT e.id, e.name, eo.é_criador
FROM evento_organizador eo
JOIN event e ON eo.event_id = e.id
WHERE eo.usuario_id = 3
AND e.active = 1;

-- Contar organizadores por evento
SELECT e.id, e.name, COUNT(eo.id) as total_orgs
FROM event e
LEFT JOIN evento_organizador eo ON e.id = eo.event_id
WHERE e.active = 1
GROUP BY e.id;

-- Eventos com múltiplos organizadores
SELECT e.id, e.name, COUNT(eo.id) as total_orgs
FROM event e
JOIN evento_organizador eo ON e.id = eo.event_id
WHERE e.active = 1
GROUP BY e.id
HAVING COUNT(eo.id) > 1;
```

## Performance

- **Índices**: event_id, usuario_id, (event_id, usuario_id)
- **UNIQUE**: (event_id, usuario_id) - Evita duplicatas
- **Sugestão**: Adicionar índice composto para queries frequentes

## Segurança

- ✅ Verificação de permissões em cada endpoint
- ✅ Proteção ao criador original
- ✅ Validação de usuário/evento existente
- ✅ Proteção contra duplicatas (UNIQUE constraint)
- ⚠️ TODO: Auditoria de mudanças em organizadores

## Compatibilidade Backward

A coluna `usuario_id` na tabela `event` foi mantida para não quebrar código antigo:
- ✅ Ao criar evento, vincula em `event.usuario_id` E `evento_organizador`
- ✅ Ao listar, usa `evento_organizador` como fonte da verdade
- ⚠️ Futuro: Considerar deprecar `event.usuario_id` quando todas queries migrarem

---

**Última Atualização**: 18/11/2025
