# Autenticação e Segurança - Racket Hero

**Data**: 14 de Novembro de 2025  
**Escopo**: MVP - Pequeno Projeto  
**Tech Stack**: FastAPI + React + SQLite

---

## 📋 Resumo Executivo

Para um projeto de **pequeno escopo em MVP**, recomenda-se abordagem **pragmática mas segura**:
- ✅ **Autenticação**: JWT (simples, eficiente, stateless)
- ✅ **Senha**: bcrypt (industry standard, seguro)
- ✅ **Recuperação**: Email com token único + expiração
- ✅ **2FA**: Opcional (v1.1+)
- ✅ **HTTPS/CORS**: Obrigatório
- ✅ **Rate Limiting**: Essencial contra brute force

**Tempo de implementação**: ~3-5 dias para MVP completo

---

## 🔐 Feature 5 - Autenticação e Segurança

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
Enviar email de confirmação (opcional para MVP)
    ↓
Retornar JWT token automaticamente
```

#### Regras de Validação

| Campo | Regra | Exemplo |
|-------|-------|---------|
| **Email** | RFC 5322, único no sistema | `joao@example.com` |
| **Senha** | Mín. 8 caracteres, >= 3 tipos | `SecurePass123!` ✅ / `abc123` ❌ |
| **Tipo** | Enum: `Jogador`, `Organizador` | `Jogador` |
| **Nome** | 2-100 caracteres, alfanuméricos | `João Silva` |

#### Validação de Força de Senha

```python
# Exemplo de regra
def validar_senha(senha: str) -> bool:
    if len(senha) < 8:
        return False
    
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_especial = any(c in "!@#$%^&*()_+-=" for c in senha)
    
    tipos = sum([tem_maiuscula, tem_minuscula, tem_numero, tem_especial])
    return tipos >= 3  # Mínimo 3 tipos
```

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

---

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

#### Resposta de Erro

**Importante**: Retornar mensagem genérica para segurança
- ❌ Não faça: `Usuário não encontrado`
- ✅ Faça: `Credenciais inválidas`

#### Tokens JWT

**Access Token**:
- Duração: **15 minutos**
- Escopo: Acesso à API
- Informação: `{user_id, email, tipo, exp}`

**Refresh Token**:
- Duração: **7 dias**
- Escopo: Renovar access token
- Informação: `{user_id, exp, type: "refresh"}`

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
  "expires_in": 900  # segundos
}
```

#### Rate Limiting

Proteger contra brute force:
```
POST /auth/login → Máximo 5 tentativas por IP em 15 minutos
Após 5 tentativas: Aguardar 15 minutos antes de nova tentativa
Log: Registrar todas as tentativas falhadas
```

---

### 3. Refresh Token

#### Fluxo

```
Usuário com access_token expirado submete refresh_token
    ↓
Validar refresh_token (assinatura, expiração)
    ├─ Inválido → 401 "Refresh token expirado, faça login novamente"
    └─ Válido
        ↓
        Gerar novo access_token
        ↓
        Retornar novo access_token
```

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

---

### 4. Recuperação de Senha

#### Fluxo

```
Usuário acessa /recover-password com email
    ↓
Buscar usuário por email
    ├─ Não encontrado → 200 "Se email existe, enviaremos link"
    └─ Encontrado
        ↓
        Gerar token único + expiração 30min
        ↓
        Armazenar token no banco (reset_token, reset_expires)
        ↓
        Enviar email com link:
        https://app.com/reset-password?token=xxx&email=xxx
        ↓
        Retornar 200 "Email enviado"
```

#### Importante

- **Nunca revelar se email existe** (por segurança)
- **Token de 32+ caracteres aleatórios** (criptograficamente seguro)
- **Expiração de 30 minutos** (não muito longo)
- **Token de uso único** (após uso, invalidar)
- **Email com HTTPS** (link seguro)

#### Reset de Senha

```
Usuário clica link, acessa /reset-password?token=xxx&email=xxx
    ↓
Validar token (existe, não expirado, matches email)
    ├─ Inválido → "Link expirado ou inválido"
    └─ Válido
        ↓
        Mostrar form: nova senha + confirmação
        ↓
        Usuário submete: nova_senha
        ↓
        Validar força (same rules as signup)
        ↓
        Hash bcrypt nova senha
        ↓
        Invalidar token de reset (reset_token = null)
        ↓
        Logout de todos os devices (limpar refresh tokens)
        ↓
        Retornar 200 "Senha alterada com sucesso"
```

#### Endpoints

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

---

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
```

---

### 5. Logout

#### Fluxo

```
Usuário clica logout com access_token válido
    ↓
Invalidar refresh_token do usuário (se DB-backed)
    OU adicionar token à blacklist (se verificação por token)
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

#### Implementação

Duas opções:

**Opção A: JWT sem estado (Stateless) - RECOMENDADO PARA MVP**
- ✅ Simples, sem BD queries
- ✅ Escalável (sem sessão no servidor)
- ❌ Logout = apenas cliente limpa token
- ❌ Token pode ser usado até expiração
- **Solução**: Usar short-lived tokens (15min)

**Opção B: JWT com Blacklist (Stateful)**
- ✅ Logout imediato e eficiente
- ❌ Requer tabela de blacklist no BD
- ❌ Menos escalável
- **Solução**: Para v1.1+

---

### 6. Senha Esquecida - Fluxo Completo

```
┌─────────────────────────────────────────────────────────┐
│                   RECUPERAÇÃO DE SENHA                   │
└─────────────────────────────────────────────────────────┘

1. PÁGINA: /forgot-password
   - Input: email
   - Botão: "Enviar link de recuperação"

2. USUÁRIO SUBMETE EMAIL
   POST /auth/forgot-password
   
   Backend:
   - Gera: reset_token (32 chars aleatório)
   - Armazena: reset_token, reset_expires (30min)
   - Envia EMAIL com link:
     https://app.com/reset-password?token=XXX&email=joao@example.com
   
   Resposta: "Se email existe, enviaremos link" (mesmo se não existe)

3. USUÁRIO CLICA EMAIL
   - Link expira em 30 minutos
   - Acessa: /reset-password?token=XXX&email=XXX

4. PÁGINA: /reset-password
   - Valida token (frontend + backend)
   - Se inválido: "Link expirado"
   - Se válido: Mostra form
   
   Inputs:
   - Nova senha (mínimo 8 chars, 3 tipos)
   - Confirmar senha
   - Botão: "Alterar Senha"

5. USUÁRIO SUBMETE NOVA SENHA
   POST /auth/reset-password
   
   Backend:
   - Valida token (força de senha)
   - Gera hash bcrypt
   - Atualiza: senha, reset_token=null, reset_expires=null
   - LOGOUT DE TODOS OS DEVICES (invalida refresh tokens)
   
   Resposta: "Senha alterada. Você será desconectado"

6. USUÁRIO FAZ LOGIN NOVAMENTE
   POST /auth/login
   - Email + nova senha
   - Recebe novo access_token + refresh_token
```

---

## 🔒 Boas Práticas de Segurança

### 1. Hash de Senha

**Usar bcrypt SEMPRE**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash
hashed = pwd_context.hash(senha_plano)

# Verify
is_valid = pwd_context.verify(senha_plano, hashed)
```

**Nunca**:
- ❌ MD5, SHA-1, SHA-256 simples
- ❌ Armazenar senha em plano
- ❌ Usar salt fraco

### 2. JWT Configuration

**Configurar variables de ambiente**:
```python
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Mín. 32 caracteres, complexo
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

**Exemplo .env**:
```
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=app-password-do-gmail
```

### 3. HTTPS Obrigatório

**Em Produção**:
- ✅ HTTPS/TLS para todas as requisições
- ✅ Certificado válido (Let's Encrypt gratuito)
- ✅ Redirect HTTP → HTTPS

**Em Desenvolvimento**:
- HTTP é aceitável (localhost)
- Use http://localhost:3000

### 4. CORS Configurado

```python
# FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # Frontend dev
    "https://app.racket-hero.com",  # Frontend produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Rate Limiting

**Proteger endpoints sensíveis**:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Endpoint
@app.post("/auth/login")
@limiter.limit("5/15 minutes")
async def login(request: Request, credentials: LoginRequest):
    ...

@app.post("/auth/forgot-password")
@limiter.limit("3/1 hour")
async def forgot_password(request: Request, email: str):
    ...
```

### 6. SQL Injection Prevention

**Usar ORM (SQLAlchemy)**:
```python
# ✅ BOM: Parameterized query
user = db.query(Usuario).filter(Usuario.email == email).first()

# ❌ RUIM: String interpolation
user = db.query(f"SELECT * FROM usuario WHERE email = '{email}'")
```

### 7. XSS Prevention

**React já faz sanitização**:
```jsx
// ✅ React sanitiza por padrão
<div>{userData.name}</div>

// ❌ Evitar dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{__html: userData.html}} />
```

**Backend**: Validar e escapar dados
```python
from html import escape

nome_safe = escape(nome_usuario)
```

### 8. CSRF Protection (Optional para MVP)

Para APIs JSON + CORS (JWT):
- ✅ CSRF natural (não precisa de token adicional)
- Cookies same-site ajudam
- Para v1.1+ considerar adicionar

---

## 🗄️ Modelo de Dados

```python
# backend/models/usuario.py

from sqlalchemy import Column, String, DateTime, Enum
from datetime import datetime, timedelta
import enum

class TipoUsuario(str, enum.Enum):
    JOGADOR = "Jogador"
    ORGANIZADOR = "Organizador"
    ADMIN = "Administrador"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False)
    
    # Status
    ativo = Column(Boolean, default=True)  # Soft delete
    email_verificado = Column(Boolean, default=False)
    
    # Recuperação de senha
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    # Auditoria
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_login = Column(DateTime, nullable=True)
    
    # Logs de login (relacionamento)
    logs_login = relationship("LoginLog", back_populates="usuario")

class LoginLog(Base):
    __tablename__ = "login_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    usuario_id = Column(UUID, ForeignKey("usuarios.id"), nullable=False)
    ip_address = Column(String)
    user_agent = Column(String)
    sucesso = Column(Boolean)
    motivo_falha = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    usuario = relationship("Usuario", back_populates="logs_login")
```

---

## 📧 Email de Recuperação

### Exemplo de Template

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .button { background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
        .footer { color: #666; font-size: 12px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Recuperação de Senha - Racket Hero</h2>
        
        <p>Olá {{ nome }},</p>
        
        <p>Você solicitou uma recuperação de senha. Clique no botão abaixo para criar uma nova senha:</p>
        
        <p>
            <a href="https://app.com/reset-password?token={{ token }}&email={{ email }}" class="button">
                Redefinir Senha
            </a>
        </p>
        
        <p>Ou copie e cole este link no navegador:</p>
        <p>https://app.com/reset-password?token={{ token }}&email={{ email }}</p>
        
        <p><strong>⏱️ Este link expira em 30 minutos</strong></p>
        
        <p>Se você não solicitou esta recuperação, ignore este email.</p>
        
        <div class="footer">
            <p>Racket Hero © 2025</p>
            <p>Este é um email automático, não responda.</p>
        </div>
    </div>
</body>
</html>
```

---

## 🧪 Checklist de Implementação MVP

### Feature 5 - Autenticação (v1.0)

- [ ] **Backend (FastAPI)**
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

- [ ] **Frontend (React)**
  - [ ] Página: /register (form, validação, mensagens)
  - [ ] Página: /login (form, credenciais, remember me)
  - [ ] Página: /forgot-password (input email)
  - [ ] Página: /reset-password (form nova senha)
  - [ ] Armazenar tokens (localStorage)
  - [ ] Interceptor de requisições (adicionar JWT)
  - [ ] Interceptor de resposta (handle 401, refresh)
  - [ ] Logout (limpar tokens, redirecionar)
  - [ ] Proteção de rotas (PrivateRoute)

- [ ] **Testes**
  - [ ] Test: Register com email válido
  - [ ] Test: Register com email duplicado
  - [ ] Test: Register com senha fraca
  - [ ] Test: Login com credenciais corretas
  - [ ] Test: Login com credenciais erradas
  - [ ] Test: Rate limiting (5+ tentativas)
  - [ ] Test: Refresh token expirado
  - [ ] Test: Forgot password + reset
  - [ ] Test: Reset token expirado
  - [ ] Test: E2E completo (register → login → logout)

- [ ] **Deployment**
  - [ ] Variaveis de ambiente configuradas
  - [ ] HTTPS em produção
  - [ ] JWT secret seguro (32+ chars)
  - [ ] Email SMTP configurado
  - [ ] CORS whitelist correto

---

## 📊 Comparação: Abordagens

| Aspecto | MVP (Recomendado) | Alternativa Simples | Alternativa Robusta |
|---------|-------------------|-------------------|-------------------|
| **Autenticação** | JWT (15min) | Session (servidor) | OAuth2 + JWT |
| **Recuperação** | Email token (30min) | SMS código | Authenticator App |
| **2FA** | Não (v1.1+) | N/A | TOTP/SMS |
| **Senha** | bcrypt | argon2 | argon2 + pepper |
| **Email** | SMTP básico | SendGrid API | AWS SES |
| **Rate Limit** | Manual | slowapi | nginx |
| **Implementação** | 3-5 dias | 2-3 dias | 10+ dias |
| **Segurança** | ✅ Boa | ⚠️ Média | ✅✅ Excelente |

---

## 🚀 Próximas Fases (v1.1+)

### v1.1 - Autenticação Avançada

```markdown
- [ ] Email Verification (confirmar email ao registrar)
- [ ] Password Strength Meter (mostrar força em tempo real)
- [ ] Login History (usuário vê lista de dispositivos)
- [ ] Logout de todos os dispositivos
- [ ] Change Password (dentro da app, quando logado)
- [ ] Account Deactivation (self-service)
```

### v1.2 - 2FA

```markdown
- [ ] TOTP (Google Authenticator, Authy)
- [ ] SMS Code (Twilio)
- [ ] Backup Codes (em caso de perda do 2FA)
```

### v1.3 - OAuth

```markdown
- [ ] Login com Google
- [ ] Login com Discord
- [ ] Sincronização de perfil
```

---

## 🔍 Testes de Segurança Recomendados

### Antes de Produção

1. **OWASP Top 10**
   - [ ] SQL Injection (use ORM)
   - [ ] XSS (React sanitiza)
   - [ ] CSRF (JWT não é vulnerável)
   - [ ] Broken Auth (validação forte)
   - [ ] Sensitive Data Exposure (HTTPS)

2. **Teste de Penetração Básico**
   ```bash
   # Brute force
   for i in {1..10}; do
     curl -X POST http://localhost:8000/auth/login \
       -H "Content-Type: application/json" \
       -d '{"email":"test@test.com","senha":"wrong'$i'"}'
   done
   # Deve retornar 429 após 5 tentativas
   ```

3. **Verificação de Senha**
   ```bash
   # Testar força
   echo -n "abc" | curl -X POST http://localhost:8000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","senha":"abc"}'
   # Deve rejeitar (< 8 chars)
   ```

---

## 📚 Referências

- **JWT**: https://jwt.io
- **bcrypt**: https://github.com/pyca/bcrypt
- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
- **OWASP**: https://owasp.org/www-project-top-ten/
- **Password Guidelines**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

---

## 📝 Conclusão

**Recomendação Final para MVP**:

```markdown
✅ IMPLEMENTAR:
1. JWT + Refresh Token (15min + 7 dias)
2. bcrypt (password hashing)
3. Email recovery (token 30min)
4. Rate limiting (brute force)
5. HTTPS + CORS
6. Validação de força de senha (8+ chars, 3 tipos)

⏸️ ADIAR PARA v1.1+:
1. Email verification
2. 2FA (TOTP)
3. Login history
4. OAuth (Google, Discord)
5. Account deactivation

⚠️ NUNCA FAZER:
1. Armazenar senha em plano
2. Usar MD5/SHA-1 simples
3. Compartilhar JWT com usuário antes de HTTPS
4. Deixar secrets no código
5. Permitir bruteforce (sem rate limit)
```

**Tempo para MVP**: ~4-5 dias com testes

---

**Documentação completa e pronta para implementação! 🔐**
