# Especificação - Racket Hero

Plataforma de gerenciamento de eventos de tênis de mesa com suporte a diferentes formatos de torneio, ranking por ELO e controle granular de permissões.

## Índice

- [Feature 1 - Estrutura e Organização de Grupos e Eventos](#feature-1---estrutura-e-organização-de-grupos-e-eventos)
- [Feature 2 - Estrutura de Partidas e Jogos](#feature-2---estrutura-de-partidas-e-jogos)
- [Feature 3 - Estrutura de Usuários](#feature-3---estrutura-de-usuários)
- [Feature 4 - Ranking](#feature-4---ranking)
- [Feature 5 - Autenticação e Segurança](#feature-5---autenticação-e-segurança)

---

## Feature 1 - Estrutura e Organização de Grupos e Eventos

### Hierarquia

```
Grupo: {
    Evento 1: {...},
    Evento 2: {...},
    ...
    Evento N: {...}
}
```

### Grupos

- Um Grupo tem dois status: **Ativo** e **Inativo**.
- Um Grupo criado terá seu status como **Ativo** por padrão.
- Um Grupo deve ser criado e editado por Organizadores e Administradores.
- Um Grupo contém uma lista de jogadores e o ranking desses jogadores.
- Um Grupo contém Eventos criados pelos seus Organizadores.
- Um Grupo pode ter mais de um Organizador.
- Um Grupo só pode ser visto pelos seus Organizadores, Jogadores nele incluído e Administradores.
- Um Grupo não pode ser apagado por um Organizador, somente inativado.
- Um Grupo inativo não permite criação de novos eventos.
- Um Grupo inativo permite a visualização de seu histórico.
- Um Grupo inativo não permite a inclusão de novos jogadores.
- Um Grupo inativo pode ser ativado novamente.

### Eventos

- Um Evento tem quatro status: **Agendado**, **Em Progresso**, **Concluído** e **Inativo**.

#### Transições de Status Permitidas

| De | Para | Condição |
|----|------|----------|
| Agendado | Em Progresso | Quando o evento é iniciado |
| Em Progresso | Concluído | Quando o evento termina |
| Agendado/Em Progresso/Concluído | Inativo | Manualmente, a qualquer hora |
| Inativo | Agendado | Reativação |

**Nota**: Uma vez Concluído, não pode retornar a Em Progresso.

#### Outras Regras

- Um Evento só pode pertencer a um Grupo.
- Apenas jogadores cadastrados no grupo que o Evento pertence podem participar do Evento.
- Um Evento é único, não podendo ser repetido.
- Um Evento deve ser definido, no momento de sua criação, como **Ranqueado** ou **Não Ranqueado**.
- Um Evento deve ter seu formato decidido entre:
  - Partidas simples.
  - Torneio eliminatório simples por chaves.
  - Fase de grupos seguido por eliminatório simples.
  - Rodada suíça.
  - (Baseado nos formatos Single elimination, Swiss System e Group + Knockout Hybrid - [ref](https://mycup.me/blog/tournament-types/))
- O status Ranqueado/Não Ranqueado é **IMUTÁVEL** após criação do evento.
  - **Validação**: "Não é permitido alterar tipo de evento após criação".

#### Estados de Jogadores em um Evento

Um Evento terá jogadores com os seguintes estados: **Inscrito**, **Ativo**, **Suspenso** e **Retirado**.

| Estado | Descrição |
|--------|-----------|
| Inscrito (padrão) | Pode jogar partidas futuras |
| Ativo (em andamento) | Participando do evento |
| Suspenso | Não pode participar de novas partidas (apenas Admin/Organizador podem suspender) |
| Retirado | Saiu voluntariamente ou foi removido (estado final) |

#### Regras de Transição de Estados de Jogadores

- Um Jogador pode se retirar se `Evento.status = "Agendado"` ou `"Em Progresso"`.
- Um Organizador pode remover jogador a qualquer momento.
- Uma vez retirado, o jogador sai do ranking/placar daquele evento.

#### Restrições por Status do Evento

| Status | Pode criar partidas | Pode adicionar jogadores | Pode suspender jogadores |
|--------|-------------------|------------------------|--------------------------|
| Agendado | ✅ Sim | ✅ Sim | ❌ Não |
| Em Progresso | ✅ Sim | ❌ Não | ✅ Sim (apenas suspender) |
| Concluído | ❌ Não | ❌ Não | ❌ Não |
| Inativo | ❌ Não | ❌ Não | ❌ Não |

---

## Feature 2 - Estrutura de Partidas e Jogos

### Partidas

- Uma Partida é um confronto entre dois jogadores dentro de um evento.
- Uma Partida pertence a exatamente um Evento.
- Uma Partida tem os seguintes status: **Agendada**, **Em Progresso**, **Concluída** e **Cancelada**.
- Uma Partida deve registrar:  jogador 1, jogador 2, vencedor e placar (sets e games).
- Uma Partida é iniciada se o Evento estiver com status **"Em Progresso"**.
- Uma Partida pode ser criada por um Organizador do grupo ou pelo sistema (automaticamente em torneios).
- Uma Partida é criada no status **"Agendada"** por padrão.
- Uma Partida só pode ter seu resultado registrado se estiver com status **"Em Progresso"**.

### Jogos (Sets/Games)

- Um Jogo é a unidade mínima de competição em tênis de mesa (um set).
- Uma Partida é composta por um ou mais Jogos (número de sets é flexível, não necessitando de definição prévia).
- Um Jogo deve registrar: número do jogo, pontos de cada jogador e vencedor do jogo.

### Resultados e Placar

- O placar deve ser registrado de forma granular (ponto a ponto).
- O sistema não precisa validar automaticamente a conclusão de um Jogo/Partida conforme as regras.
- Uma vez que uma Partida é marcada como Concluída, seu resultado pode ser alterado por Organizadores.

#### Fluxo de Validação de Resultados

- Organizador/Admin sempre pode registrar resultado diretamente, sem necessidade de confirmação.

### Agendamento

- Organizadores podem visualizar todas as partidas de seus eventos.
- Jogadores podem visualizar todas as partidas do Evento.
- O sistema deve permitir busca/filtro de partidas por evento, data e jogador.

---

## Feature 3 - Estrutura de Usuários

### Tipos de Usuários

- **Administrador**
- **Organizador**
- **Jogador**

**Observação**: Jogadores e Organizadores devem se registrar e ter contas na plataforma.

### Definição de Papéis

O papel do usuário (Jogador ou Administrador) deve ser definido no momento do registro da conta do usuário.

### Organizadores

- Um Organizador é um jogador, além de seus privilégios administrativos.
- Um Organizador pode criar grupos, sendo o dono de todos os grupos que criou.
- Um Organizador só poderá ver grupos que ele criou (ou eventos que lhe foram delegados por Admin).
- Um Organizador poderá adicionar jogadores aos seus grupos.
- Um Organizador poderá adicionar jogadores aos eventos de seu grupo (somente jogadores com contas registradas).
- Um Organizador pode criar e administrar eventos dentro do grupo.

#### Permissões de Múltiplos Organizadores em um Grupo

- Todos os Organizadores de um Grupo têm permissão idêntica (editar eventos uns dos outros).
- Ao remover um Organizador: Seus eventos não são apagados, permanecem no grupo.
- Admin pode transferir propriedade de um evento para outro Organizador.

### Jogadores

- Um Jogador deve ser colocado em um grupo por um Organizador.
- Um Jogador pode se inscrever em qualquer evento dentro do grupo que ele pertence.
- Um Jogador pode se retirar de um evento seguindo as regras de transição de estado.
- Um Jogador pode ver suas partidas em andamento, concluídas e futuras.
- Um Jogador poderá ver seu ranking no grupo, incluindo sua pontuação.
- Um Jogador terá seu ranking atrelado a um grupo (isolado por grupo).
  - **Exemplo**: O ranking do jogador A no grupo 1 é calculado apenas com eventos do grupo 1. Eventos do jogador A no grupo 1 não afetam seu ranking no grupo 2.
- Um Jogador pode visualizar o ranking completo do grupo que pertence.
- Um Jogador não pode ver rankings de grupos que não pertence.
- Um Jogador não pode criar eventos.
- Um Jogador terá seu status como **Inscrito** quando adicionado a um evento, por padrão.

### Administradores

- Um Administrador terá todos os privilégios de Organizadores.
- Um Administrador poderá ver e editar todos os grupos e eventos.
- Um Administrador poderá ver e editar todos os usuários (Organizadores e Jogadores).

---

## Feature 4 - Ranking

### Conceitos Gerais

- O ranking funcionará pelo sistema de **ELO**.
- O ranking de cada jogador será atrelado a um grupo (isolado por grupo).
  - **Exemplo**: O ranking do jogador A no grupo 1 é calculado apenas com eventos do grupo 1. Eventos do jogador A no grupo 1 não afetam seu ranking no grupo 2.
- O ranking deve incluir: colocação, nome, rating ELO, vitórias, derrotas e taxa de vitória.
- Somente partidas de eventos definidos como **Ranqueados** devem influenciar no ranking dos jogadores nele presente.
- Partidas de eventos definidos como **Não Ranqueados** não devem influenciar no ranking dos jogadores.
- Ao definir se um evento será **Ranqueado** ou **Não Ranqueado**, essa definição não poderá ser alterada.

### Cálculo de ELO

- **K-factor**: 32 (padrão), pode ser 16 ou 48 por tipo de evento.
- **Fórmula**: `E_novo = E_antigo + K * (Resultado - Probabilidade_esperada)`
- **Resultado**: 1 se venceu, 0 se perdeu.
- **ELO inicial padrão**: 1600 (ou configurável por evento).
- **Mínimo ELO**: 400 (ou configurável).

### Atualização de ELO

- ELO é recalculado **IMEDIATAMENTE** após validação de partida.
- Se partida é revertida: ELO recalculado retroativamente.
- Manter histórico de mudanças ELO (auditoria).

### Visualização do Ranking

- Um Jogador pode visualizar o ranking completo do grupo que pertence.
- Um Jogador não pode ver rankings de grupos que não pertence.
- Um Organizador pode visualizar e exportar o ranking de seus eventos/grupos.

---

## Feature 5 - Autenticação e Segurança

### 1. Registro de Usuário (Sign Up)

#### Fluxo

```
Usuário submete: email + senha + tipo (Jogador ou Organizador)
    ↓
Validação (email único, senha força)
    ↓
Gerar hash bcrypt da senha
    ↓
Criar usuário no banco (status: ATIVO)
    ↓
Retornar JWT token automaticamente
```

#### Validação de Entrada

| Campo | Regra | Exemplo |
|-------|-------|---------|
| **Email** | RFC 5322, único no sistema | `joao@example.com` |
| **Senha** | Mín. 8 caracteres, >= 3 tipos | `SecurePass123!` ✅ / `abc123` ❌ |
| **Tipo** | Enum: `Jogador`, `Organizador` | `Jogador` |
| **Nome** | 2-100 caracteres | `João Silva` |

**Força de Senha**: Deve conter mínimo 3 dos 4 tipos:
- Letra maiúscula (A-Z)
- Letra minúscula (a-z)
- Número (0-9)
- Caractere especial (!@#$%^&*)

#### Endpoint

```
POST /auth/register
Content-Type: application/json

{
  "email": "joao@example.com",
  "senha": "SecurePass123!",
  "nome": "João Silva",
  "tipo": "Jogador"
}

Response 201:
{
  "id": "uuid",
  "email": "joao@example.com",
  "nome": "João Silva",
  "tipo": "Jogador",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### 2. Login

#### Fluxo

```
Usuário submete: email + senha
    ↓
Buscar usuário por email
    ├─ Não encontrado → 401 "Credenciais inválidas"
    └─ Encontrado
        ↓
        Comparar hash bcrypt
        ├─ Mismatch → 401 "Credenciais inválidas"
        └─ Match
            ↓
            Gerar JWT token + refresh token
            ↓
            Log de login (auditoria)
            ↓
            Retornar tokens
```

#### Tokens JWT

| Token | Duração | Escopo |
|-------|---------|--------|
| **Access Token** | 15 minutos | Acesso à API |
| **Refresh Token** | 7 dias | Renovar access token |

#### Rate Limiting

Proteger contra brute force:
- **Limite**: Máximo 5 tentativas por IP em 15 minutos
- **Ação**: Aguardar 15 minutos antes de nova tentativa
- **Log**: Registrar todas as tentativas falhadas

#### Endpoint

```
POST /auth/login
Content-Type: application/json

{
  "email": "joao@example.com",
  "senha": "SecurePass123!"
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}

Response 401:
{
  "detail": "Credenciais inválidas"
}
```

### 3. Refresh Token

Permitir renovação do access token sem fazer login novamente:

#### Endpoint

```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}

Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### 4. Recuperação de Senha (Forgot Password)

#### Fluxo

```
Usuário acessa /recover-password com email
    ↓
Buscar usuário por email
    ├─ Não encontrado → 200 "Se email existe, enviaremos link"
    └─ Encontrado
        ↓
        Gerar token único (32+ chars) + expiração 30min
        ↓
        Armazenar token no banco
        ↓
        Enviar email com link de reset
        ↓
        Retornar 200 "Email enviado"
```

**Importante**: Retornar a mesma resposta se email existe ou não (por segurança)

#### Endpoint

```
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "joao@example.com"
}

Response 200:
{
  "message": "Se o email está registrado, enviaremos um link de recuperação"
}
```

### 5. Reset de Senha

Usuário clica no link do email e cria nova senha:

#### Fluxo

```
Usuário clica link: /reset-password?token=XXX&email=XXX
    ↓
Validar token (existe, não expirado)
    ├─ Inválido → "Link expirado ou inválido"
    └─ Válido
        ↓
        Mostrar form: nova senha + confirmação
        ↓
        Usuário submete nova senha
        ↓
        Validar força (mesma regra do registro)
        ↓
        Hash bcrypt nova senha
        ↓
        Invalidar token de reset
        ↓
        Logout de todos os dispositivos
        ↓
        Retornar 200 "Senha alterada com sucesso"
```

#### Endpoint

```
POST /auth/reset-password
Content-Type: application/json

{
  "email": "joao@example.com",
  "token": "abc123def456...",
  "nova_senha": "NewSecurePass123!"
}

Response 200:
{
  "message": "Senha alterada com sucesso. Você será desconectado de todos os dispositivos."
}

Response 400:
{
  "detail": "Link expirado ou inválido"
}
```

### 6. Logout

#### Fluxo

```
Usuário clica logout com access_token válido
    ↓
Frontend: Limpar localStorage (tokens)
    ↓
Redirecionar para /login
```

#### Endpoint

```
POST /auth/logout
Authorization: Bearer {access_token}

Response 200:
{
  "message": "Desconectado com sucesso"
}
```

### 7. Boas Práticas de Segurança

#### Hash de Senha

- ✅ **Usar bcrypt** (algoritmo robusto, com salt automático)
- ❌ **Nunca** usar MD5, SHA-1, SHA-256 simples
- ❌ **Nunca** armazenar senha em plano

#### Configuração JWT

```python
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Mín. 32 caracteres
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

#### HTTPS Obrigatório

- ✅ **Produção**: HTTPS/TLS (Let's Encrypt gratuito)
- ✅ **Desenvolvimento**: HTTP em localhost é aceitável

#### CORS Configurado

- ✅ Whitelist de origens explícita
- ✅ Permitir credentials
- ✅ Limitar métodos HTTP

#### Rate Limiting

- ✅ `/auth/login`: 5 tentativas por 15 minutos
- ✅ `/auth/forgot-password`: 3 tentativas por 1 hora

#### SQL Injection Prevention

- ✅ Usar ORM (SQLAlchemy com query parameterized)
- ❌ Nunca usar string interpolation em queries

#### XSS Prevention

- ✅ React sanitiza por padrão
- ✅ Validar e escapar dados no backend

### 8. Modelo de Dados

```
Usuário:
- id (UUID, PK)
- email (String, unique, index)
- nome (String)
- senha_hash (String)
- tipo (Enum: Jogador, Organizador, Admin)
- ativo (Boolean, default: True)
- reset_token (String, nullable)
- reset_token_expires (DateTime, nullable)
- criado_em (DateTime)
- atualizado_em (DateTime)
- ultimo_login (DateTime, nullable)

LoginLog (para auditoria):
- id (UUID, PK)
- usuario_id (FK)
- ip_address (String)
- sucesso (Boolean)
- criado_em (DateTime)
```

### 9. Checklist de Implementação (MVP)

#### Backend (FastAPI)

- [ ] Model Usuario (email, senha_hash, tipo, reset_token)
- [ ] POST /auth/register (validação, bcrypt, JWT)
- [ ] POST /auth/login (credenciais, rate limit, JWT)
- [ ] POST /auth/refresh (refresh token → new access token)
- [ ] POST /auth/logout (clear tokens client-side)
- [ ] POST /auth/forgot-password (gera token, envia email)
- [ ] POST /auth/reset-password (valida token, atualiza senha)
- [ ] Middleware: verificar JWT em rotas protegidas
- [ ] Rate limiting (5/15min login, 3/1h forgot)
- [ ] Log de login/logout

#### Frontend (React)

- [ ] Página: /register (form, validação, mensagens)
- [ ] Página: /login (form, credenciais)
- [ ] Página: /forgot-password (input email)
- [ ] Página: /reset-password (form nova senha)
- [ ] Armazenar tokens (localStorage)
- [ ] Interceptor de requisições (adicionar JWT)
- [ ] Interceptor de resposta (handle 401, refresh)
- [ ] Logout (limpar tokens, redirecionar)
- [ ] Proteção de rotas (PrivateRoute)

#### Testes

- [ ] Register com email válido
- [ ] Register com email duplicado
- [ ] Register com senha fraca
- [ ] Login com credenciais corretas
- [ ] Login com credenciais erradas
- [ ] Rate limiting (5+ tentativas)
- [ ] Refresh token expirado
- [ ] Forgot password + reset
- [ ] Reset token expirado
- [ ] E2E completo (register → login → logout)

---

## Referências

- [Tournament Types - MyCup](https://mycup.me/blog/tournament-types/)
- [JWT.io - JSON Web Tokens](https://jwt.io)
- [bcrypt - Password Hashing](https://github.com/pyca/bcrypt)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
