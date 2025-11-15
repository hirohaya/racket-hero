# 🔐 Sistema de Permissões - Racket Hero

## Visão Geral

Racket Hero implementa um sistema granular de permissões baseado em **3 tipos de usuários**:

| Tipo | Descrição | Ícone |
|------|-----------|-------|
| **Jogador** | Jogador de torneios, participante | 🎯 |
| **Organizador** | Cria e gerencia eventos e partidas | 📋 |
| **Admin** | Acesso total ao sistema | 🔐 |

---

## Hierarquia de Acesso

```
🎯 Jogador (Nível 0)
    ↓
📋 Organizador (Nível 1)
    ↓
🔐 Admin (Nível 2)
```

**Regra**: Cada tipo tem acesso a todas as permissões do tipo anterior + permissões extras.

---

## Permissões Detalhadas

### 🎯 JOGADOR

Permissões disponíveis:
- ✅ **VER_EVENTOS** - Visualizar lista de eventos públicos
- ✅ **VER_PARTIDAS** - Visualizar partidas
- ✅ **VER_RANKING** - Consultar rankings e Elo

**Restrições**:
- ❌ Não pode criar eventos
- ❌ Não pode gerenciar partidas
- ❌ Não pode ver relatórios

**Use case**: Participante de torneios que quer acompanhar resultados e rankings.

---

### 📋 ORGANIZADOR

Permissões disponíveis:
- ✅ **VER_EVENTOS** - Visualizar eventos
- ✅ **CRIAR_EVENTO** - Criar novos eventos
- ✅ **EDITAR_EVENTO** - Modificar dados do evento
- ✅ **VER_PARTIDAS** - Visualizar partidas
- ✅ **CRIAR_PARTIDA** - Registrar novas partidas
- ✅ **EDITAR_PARTIDA** - Atualizar resultados de partidas
- ✅ **VER_RANKING** - Consultar rankings
- ✅ **VER_RELATORIOS** - Acessar relatórios gerenciais

**Restrições**:
- ❌ Não pode deletar eventos
- ❌ Não pode deletar partidas
- ❌ Não pode gerenciar usuários

**Use case**: Organizador de torneios que cria eventos, registra partidas e monitora resultados.

---

### 🔐 ADMIN

Permissões disponíveis:
- ✅ **TODAS AS PERMISSÕES** (ver lista completa abaixo)

**Permissões extras**:
- ✅ **DELETAR_EVENTO** - Deletar eventos permanentemente
- ✅ **DELETAR_PARTIDA** - Deletar partidas
- ✅ **VER_USUARIOS** - Listar todos os usuários
- ✅ **EDITAR_USUARIO** - Modificar dados de usuários
- ✅ **DELETAR_USUARIO** - Remover usuários do sistema

**Restrições**: Nenhuma 🚀

**Use case**: Administrador do sistema com controle total.

---

## Lista Completa de Permissões

```python
VER_EVENTOS        # Visualizar eventos
CRIAR_EVENTO       # Criar novo evento
EDITAR_EVENTO      # Editar evento existente
DELETAR_EVENTO     # Deletar evento (apenas ADMIN)

VER_PARTIDAS       # Visualizar partidas
CRIAR_PARTIDA      # Registrar nova partida
EDITAR_PARTIDA     # Editar resultado de partida
DELETAR_PARTIDA    # Deletar partida (apenas ADMIN)

VER_RANKING        # Visualizar rankings
VER_RELATORIOS     # Acessar relatórios (apenas ORGANIZADOR+)

VER_USUARIOS       # Listar usuários (apenas ADMIN)
EDITAR_USUARIO     # Editar usuário (apenas ADMIN)
DELETAR_USUARIO    # Deletar usuário (apenas ADMIN)
```

---

## Como Usar no Código

### Verificar Permissão em Rota

```python
from fastapi import Depends
from utils.permissions import require_permission, Permissao
from models.usuario import Usuario

@router.get("/eventos")
async def listar_eventos(
    usuario: Usuario = Depends(require_permission(Permissao.VER_EVENTOS))
):
    """Apenas usuários com permissão VER_EVENTOS"""
    return eventos
```

### Exigir Tipo Mínimo

```python
from utils.permissions import require_tipo
from models.usuario import TipoUsuario

@router.post("/eventos")
async def criar_evento(
    event_data: dict,
    usuario: Usuario = Depends(require_tipo(TipoUsuario.ORGANIZADOR))
):
    """Apenas ORGANIZADOR e ADMIN podem criar eventos"""
    return evento
```

### Verificar Permissão Manualmente

```python
from utils.permissions import tem_permissao, Permissao

if tem_permissao(usuario, Permissao.VER_EVENTOS):
    # Usuário tem permissão
    pass
else:
    # Negar acesso
    raise HTTPException(status_code=403, detail="Acesso negado")
```

---

## Fluxo de Autenticação e Autorização

```
1. Login
   ↓
2. Token JWT gerado com tipo de usuário
   ↓
3. Requisição com Bearer Token
   ↓
4. Middleware valida token e extrai usuário
   ↓
5. Rota verifica permissão/tipo
   ↓
6. ✅ Acesso concedido / ❌ Acesso negado
```

---

## Contas de Teste

Três contas pré-configuradas para testar permissões:

### 🔐 Admin
- **Email**: `admin@test.com`
- **Senha**: `Senha123!`
- **Tipo**: ADMIN
- **Permissões**: Todas

### 📋 Organizador
- **Email**: `organizador@test.com`
- **Senha**: `Senha123!`
- **Tipo**: ORGANIZADOR
- **Permissões**: Criar/editar eventos, registrar partidas, ver relatórios

### 🎯 Jogador
- **Email**: `jogador@test.com`
- **Senha**: `Senha123!`
- **Tipo**: JOGADOR
- **Permissões**: Ver eventos, partidas, rankings

---

## Mudanças Implementadas

### Backend

1. **models/usuario.py**
   - Adicionado `TipoUsuario` enum com 3 valores
   - Métodos helper: `is_admin()`, `is_organizador()`, `is_jogador()`

2. **utils/permissions.py** (NOVO)
   - Enum `Permissao` com todas as permissões
   - Matriz `PERMISSOES_POR_TIPO`
   - Função `obter_permissoes(tipo)`
   - Função `tem_permissao(usuario, permissao)`
   - Decorator `@require_permission(Permissao.X)`
   - Decorator `@require_tipo(TipoUsuario.X)`
   - Dependency `get_usuario_autenticado()`

3. **routers/events.py**
   - POST /events → requer ORGANIZADOR
   - GET /events → requer VER_EVENTOS
   - PUT /events/{id} → requer ORGANIZADOR
   - DELETE /events/{id} → requer ADMIN

4. **tests/create_test_accounts.py**
   - Atualizado para usar `TipoUsuario` enum
   - Cria 3 contas com tipos diferentes

### Frontend

- Login funciona para todos os tipos
- Navbar mostra nome do usuário
- Botão logout disponível

---

## Próximas Melhorias

- [ ] Criar página de gerenciamento de usuários (apenas para ADMIN)
- [ ] Implementar soft delete com field `deletado_em`
- [ ] Audit log de ações por usuário
- [ ] Endpoint para alterar tipo de usuário (apenas ADMIN)
- [ ] Página de permissões no frontend
- [ ] Testes de permissões para cada rota

---

## Testes Recomendados

```bash
# Teste com Admin
curl -H "Authorization: Bearer {admin_token}" http://localhost:8000/events

# Teste com Organizador (sem permissão DELETAR_EVENTO)
curl -X DELETE -H "Authorization: Bearer {org_token}" http://localhost:8000/events/1
# Esperado: 403 Forbidden

# Teste com Jogador (sem permissão CRIAR_EVENTO)
curl -X POST -H "Authorization: Bearer {jogador_token}" http://localhost:8000/events
# Esperado: 403 Forbidden
```

---

**Última atualização**: 15 de Novembro de 2025
