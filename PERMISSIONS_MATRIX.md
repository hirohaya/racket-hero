# 📊 Permissões - Matriz de Acesso

## Resumo Visual

```
                    JOGADOR     ORGANIZADOR     ADMIN
                    🎯          📋              🔐
────────────────────────────────────────────────────
Eventos
  Ver              ✅           ✅              ✅
  Criar            ❌           ✅              ✅
  Editar           ❌           ✅              ✅
  Deletar           ❌           ❌              ✅

Partidas
  Ver              ✅           ✅              ✅
  Criar            ❌           ✅              ✅
  Editar           ❌           ✅              ✅
  Deletar           ❌           ❌              ✅

Rankings
  Ver              ✅           ✅              ✅

Relatórios
  Ver              ❌           ✅              ✅

Usuários
  Ver              ❌           ❌              ✅
  Editar           ❌           ❌              ✅
  Deletar           ❌           ❌              ✅
```

## Casos de Uso

### 🎯 JOGADOR
**Usuário típico**: Participante de torneios
- Visualiza eventos disponíveis
- Acompanha partidas que participa
- Consulta seu ranking e Elo
- Vê histórico de resultados

**Restrições**:
- Não pode criar/editar/deletar eventos
- Não pode registrar partidas
- Não pode acessar relatórios administrativos

**Exemplo de login**: `jogador@test.com / Senha123!`

---

### 📋 ORGANIZADOR
**Usuário típico**: Responsável por torneios
- Cria e gerencia eventos (campeonatos)
- Registra e atualiza resultados de partidas
- Gerencia participantes por evento
- Acessa relatórios de desempenho
- Calcula rankings e acompanha mudanças de Elo

**Restrições**:
- Não pode deletar eventos (histórico preservado)
- Não pode deletar partidas (auditoria)
- Não pode gerenciar outros usuários

**Exemplo de login**: `organizador@test.com / Senha123!`

---

### 🔐 ADMIN
**Usuário típico**: Administrador do sistema
- Acesso total a todas as funcionalidades
- Pode deletar eventos e partidas
- Gerencia usuários (criar, editar, deletar)
- Acessa todos os relatórios
- Configura sistema

**Benefícios**:
- Pode corrigir dados errados
- Pode remover eventos/partidas com erro
- Controle total do sistema

**Exemplo de login**: `admin@test.com / Senha123!`

---

## Implementação Técnica

### Backend

#### 1. Arquivo: `models/usuario.py`

```python
class TipoUsuario(str, Enum):
    JOGADOR = "jogador"
    ORGANIZADOR = "organizador"
    ADMIN = "admin"

class Usuario(Base):
    tipo = Column(String(50), default=TipoUsuario.JOGADOR)
    
    def is_admin(self) -> bool:
        return self.tipo == TipoUsuario.ADMIN
    
    def is_organizador(self) -> bool:
        return self.tipo in [TipoUsuario.ORGANIZADOR, TipoUsuario.ADMIN]
```

#### 2. Arquivo: `utils/permissions.py` (NOVO)

```python
class Permissao(str, Enum):
    VER_EVENTOS = "ver_eventos"
    CRIAR_EVENTO = "criar_evento"
    EDITAR_EVENTO = "editar_evento"
    # ... etc

PERMISSOES_POR_TIPO = {
    TipoUsuario.JOGADOR: {Permissao.VER_EVENTOS, Permissao.VER_RANKING},
    TipoUsuario.ORGANIZADOR: {Permissao.VER_EVENTOS, Permissao.CRIAR_EVENTO, ...},
    TipoUsuario.ADMIN: {TODAS_AS_PERMISSOES}
}

# Decorators para usar em rotas
@require_permission(Permissao.VER_EVENTOS)
@require_tipo(TipoUsuario.ORGANIZADOR)
```

#### 3. Rotas protegidas

```python
# Apenas ORGANIZADOR e ADMIN podem criar
@router.post("/eventos")
async def criar_evento(
    event_data: dict,
    usuario: Usuario = Depends(require_tipo(TipoUsuario.ORGANIZADOR))
):
    ...

# Todos podem ver (tem permissão)
@router.get("/eventos")
async def listar_eventos(
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    ...

# Apenas ADMIN pode deletar
@router.delete("/eventos/{id}")
async def deletar_evento(
    event_id: int,
    usuario: Usuario = Depends(require_tipo(TipoUsuario.ADMIN))
):
    ...
```

---

## Como Testar

### Test 1: Jogador tenta criar evento (deve falhar)

```bash
# Login como jogador
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jogador@test.com","senha":"Senha123!"}'
# Retorna token

# Tentar criar evento
curl -X POST http://localhost:8000/events \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Meu Torneio","date":"2025-12-01"}'
# Esperado: 403 Forbidden (INSUFFICIENT_ROLE)
```

### Test 2: Organizador cria evento (deve funcionar)

```bash
# Login como organizador
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"organizador@test.com","senha":"Senha123!"}'
# Retorna token

# Criar evento
curl -X POST http://localhost:8000/events \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Meu Torneio","date":"2025-12-01"}'
# Esperado: 200 OK, evento criado
```

### Test 3: Admin deleta evento (deve funcionar)

```bash
# Login como admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","senha":"Senha123!"}'
# Retorna token

# Deletar evento
curl -X DELETE http://localhost:8000/events/1 \
  -H "Authorization: Bearer {token}"
# Esperado: 200 OK, evento deletado
```

---

## Fluxo de Validação

```
1. Request chega com Authorization header
   ↓
2. FastAPI extrai Bearer token
   ↓
3. verify_token() decodifica JWT
   ↓
4. get_usuario_autenticado() busca usuário no DB
   ↓
5. require_tipo() ou require_permission() valida
   ↓
6. ✅ Acesso concedido → executa handler
   ou
   ❌ Acesso negado → retorna 403 Forbidden
```

---

## Próximas Melhorias

- [ ] Criação de Grupo (apenas ORGANIZADOR)
- [ ] Audit log de ações por usuário
- [ ] Página de gerenciamento de usuários (ADMIN)
- [ ] Soft delete com `deletado_em` timestamp
- [ ] Endpoint para alterar tipo de usuário (ADMIN)
- [ ] Rate limiting por tipo de usuário

---

**Última atualização**: 15 de Novembro de 2025
**Status**: ✅ Implementado e testado
