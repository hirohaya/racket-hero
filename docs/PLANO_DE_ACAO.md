# Plano de Ação - Racket Hero

**Data**: 14 de Novembro de 2025  
**Status**: MVP v1.0 - Pronto para Iniciar  
**Duração Estimada**: 6-8 semanas  
**Tech Stack**: FastAPI + React + SQLite

---

## 📊 Visão Geral do Projeto

### Objetivo
Criar plataforma MVP de gerenciamento de eventos de tênis de mesa com ranking por ELO, suportando 3 tipos de usuários (Admin, Organizador, Jogador) com autenticação segura.

### Escopo MVP v1.0

| Feature | Status | Prioridade |
|---------|--------|-----------|
| Feature 1: Grupos/Eventos | ✅ Especificado | 🔴 Crítica |
| Feature 2: Partidas/Jogos | ✅ Especificado | 🔴 Crítica |
| Feature 3: Usuários | ✅ Especificado | 🔴 Crítica |
| Feature 4: Ranking/ELO | ✅ Especificado | 🔴 Crítica |
| Feature 5: Autenticação | ✅ Especificado | 🔴 Crítica |
| Notificações (v1.1) | 📋 Futuro | 🟡 Alta |
| Relatórios (v1.1) | 📋 Futuro | 🟡 Alta |
| 2FA (v1.2) | 📋 Futuro | 🟢 Média |

---

## 🚀 Primeiros Passos (Semana 1)

### Dia 1-2: Configuração do Ambiente

#### Backend (FastAPI)

```bash
# 1. Criar estrutura de pastas
mkdir racket-hero && cd racket-hero
mkdir backend frontend

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências essenciais
pip install fastapi uvicorn sqlalchemy pydantic bcrypt python-jose email-validator python-dotenv slowapi

# 4. Criar arquivo requirements.txt
pip freeze > requirements.txt
```

**Estrutura Backend**:
```
backend/
├── venv/
├── main.py                  # Aplicação principal FastAPI
├── database.py              # Configuração SQLAlchemy
├── requirements.txt
├── .env                     # Variáveis de ambiente (não commitar)
├── .env.example             # Template de .env
├── models/
│   ├── __init__.py
│   ├── usuario.py           # Modelo Usuario
│   ├── grupo.py             # Modelo Grupo
│   ├── evento.py            # Modelo Evento
│   ├── partida.py           # Modelo Partida
│   └── jogo.py              # Modelo Jogo
├── routers/
│   ├── __init__.py
│   ├── auth.py              # Auth routes (register, login, etc)
│   ├── grupos.py            # Grupo CRUD
│   ├── eventos.py           # Evento CRUD
│   ├── partidas.py          # Partida CRUD
│   ├── jogadores.py         # Jogador enrollment
│   └── ranking.py           # Ranking ELO
├── schemas/
│   ├── __init__.py
│   ├── usuario.py           # Pydantic models (request/response)
│   ├── grupo.py
│   └── evento.py
└── utils/
    ├── __init__.py
    ├── security.py          # JWT, password hashing
    ├── email.py             # Email sending
    └── elo.py               # ELO calculations
```

#### Frontend (React)

```bash
# 1. Criar app React
cd ../frontend
npx create-react-app .

# 2. Instalar dependências
npm install axios react-router-dom

# 3. Estrutura de pastas
mkdir src/components src/pages src/services src/hooks src/utils
```

**Estrutura Frontend**:
```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── PrivateRoute.jsx         # Proteção de rotas
│   │   ├── Navbar.jsx
│   │   └── ...
│   ├── pages/
│   │   ├── Register.jsx
│   │   ├── Login.jsx
│   │   ├── ForgotPassword.jsx
│   │   ├── ResetPassword.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Grupos.jsx
│   │   ├── Eventos.jsx
│   │   ├── Partidas.jsx
│   │   └── Ranking.jsx
│   ├── services/
│   │   ├── api.js               # Axios config com interceptors
│   │   ├── authService.js
│   │   ├── grupoService.js
│   │   └── ...
│   ├── hooks/
│   │   ├── useAuth.js           # Hook para autenticação
│   │   └── useApiCall.js
│   ├── utils/
│   │   ├── tokenStorage.js      # localStorage de tokens
│   │   └── validators.js
│   ├── App.jsx
│   └── index.js
├── package.json
└── .env.local                   # Variáveis de ambiente
```

### Dia 3-4: Banco de Dados

#### 1. Criar Models (SQLAlchemy)

**backend/database.py**:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./racket_hero.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**backend/models/usuario.py**:
```python
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from database import Base

class TipoUsuario(str, enum.Enum):
    JOGADOR = "Jogador"
    ORGANIZADOR = "Organizador"
    ADMIN = "Administrador"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    nome = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False)
    
    ativo = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_login = Column(DateTime, nullable=True)
    
    grupos = relationship("Grupo", back_populates="organizadores", secondary="grupo_organizador")
```

#### 2. Executar Migrations

```bash
cd backend
python
from database import Base, engine
from models import usuario  # Import all models

Base.metadata.create_all(bind=engine)
exit()
```

### Dia 5-7: Autenticação (Priority #1)

#### 1. Setup de Segurança

**backend/utils/security.py**:
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

#### 2. Criar Rotas de Autenticação

**backend/routers/auth.py**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from database import get_db
from models.usuario import Usuario, TipoUsuario
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/register", status_code=201)
@limiter.limit("5/1 hour")
async def register(request: Request, email: str, senha: str, nome: str, tipo: TipoUsuario, db: Session = Depends(get_db)):
    # Validar email único
    if db.query(Usuario).filter(Usuario.email == email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Validar força de senha
    if not validar_senha(senha):
        raise HTTPException(status_code=400, detail="Senha fraca")
    
    # Criar usuário
    usuario = Usuario(
        email=email,
        nome=nome,
        senha_hash=hash_password(senha),
        tipo=tipo
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    # Gerar tokens
    access_token = create_access_token({"sub": usuario.id, "tipo": usuario.tipo})
    refresh_token = create_access_token({"sub": usuario.id, "type": "refresh"}, expires_delta=timedelta(days=7))
    
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nome": usuario.nome,
        "tipo": usuario.tipo,
        "token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/login")
@limiter.limit("5/15 minutes")
async def login(request: Request, email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    
    if not usuario or not verify_password(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    access_token = create_access_token({"sub": usuario.id, "tipo": usuario.tipo})
    refresh_token = create_access_token({"sub": usuario.id, "type": "refresh"}, expires_delta=timedelta(days=7))
    
    usuario.ultimo_login = datetime.utcnow()
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 900
    }

# Implementar: forgot-password, reset-password, refresh, logout
```

#### 3. Frontend - Serviço de Autenticação

**frontend/src/services/authService.js**:
```javascript
import api from './api';

const authService = {
  register: async (email, senha, nome, tipo) => {
    const response = await api.post('/auth/register', {
      email,
      senha,
      nome,
      tipo
    });
    localStorage.setItem('access_token', response.data.token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
    return response.data;
  },

  login: async (email, senha) => {
    const response = await api.post('/auth/login', {
      email,
      senha
    });
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  isLoggedIn: () => {
    return !!localStorage.getItem('access_token');
  }
};

export default authService;
```

---

## 📅 Timeline Detalhada (6-8 semanas)

### **Sprint 1: Autenticação + Setup (Semana 1-2)**

**Semana 1**:
- [ ] Dia 1-2: Setup ambiente (Backend + Frontend)
- [ ] Dia 3-4: Banco de dados (Models SQLAlchemy)
- [ ] Dia 5-7: Auth endpoints (register, login, logout)

**Semana 2**:
- [ ] Seg-Qua: Forgot/Reset password + Email
- [ ] Qui: Frontend Auth pages (Login, Register, Reset)
- [ ] Sex: Testes unitários autenticação

**Entregável**: Usuários podem registrar, fazer login, recuperar senha

---

### **Sprint 2: Core Features (Semana 3-4)**

**Semana 3**:
- [ ] Seg-Ter: Feature 1 - Grupos (CRUD backend)
- [ ] Qua-Qui: Feature 1 - Grupos (Frontend)
- [ ] Sex: Testes Grupos

**Semana 4**:
- [ ] Seg-Ter: Feature 2 - Partidas (CRUD backend)
- [ ] Qua-Qui: Feature 2 - Partidas (Frontend)
- [ ] Sex: Testes Partidas + E2E

**Entregável**: Criar grupos, eventos, partidas

---

### **Sprint 3: Ranking + Jogadores (Semana 5-6)**

**Semana 5**:
- [ ] Seg-Ter: Feature 4 - ELO (cálculo + algoritmo)
- [ ] Qua-Qui: Feature 4 - Ranking (backend + frontend)
- [ ] Sex: Testes ELO

**Semana 6**:
- [ ] Seg-Ter: Feature 3 - Jogadores (enrollment, states)
- [ ] Qua-Qui: Feature 3 - Permissões (Org, Jogador, Admin)
- [ ] Sex: Testes permissões

**Entregável**: Ranking funcional, estados de jogador

---

### **Sprint 4: Validação + Deploy (Semana 7-8)**

**Semana 7**:
- [ ] Seg-Ter: Testes E2E completos
- [ ] Qua-Qui: Bug fixes + refinamentos
- [ ] Sex: Deploy staging

**Semana 8**:
- [ ] Seg: Testes em produção
- [ ] Ter-Qui: Documentação final
- [ ] Sex: MVP v1.0 release 🎉

**Entregável**: MVP funcional e deployado

---

## 🎯 Próximos Passos Imediatos (Hoje/Amanhã)

### **TODO - Hora 0 (Preparação)**

- [ ] **1. Criar repositório Git**
  ```bash
  git init
  git remote add origin https://github.com/seu-user/racket-hero.git
  ```

- [ ] **2. Setup .env (Backend)**
  ```
  JWT_SECRET_KEY=seu-secret-key-aqui-minimo-32-caracteres
  DATABASE_URL=sqlite:///./racket_hero.db
  SMTP_SERVER=smtp.gmail.com
  SMTP_PORT=587
  SMTP_USER=seu-email@gmail.com
  SMTP_PASSWORD=app-password
  ```

- [ ] **3. Setup .env (Frontend)**
  ```
  REACT_APP_API_URL=http://localhost:8000
  ```

- [ ] **4. Criar arquivo initial commit**
  ```
  README.md (instruções de setup)
  .gitignore
  docker-compose.yml (opcional para v1.1)
  ```

### **TODO - Amanhã (Dia 1)**

#### Backend
- [ ] Criar venv e instalar dependências
- [ ] Configurar main.py (FastAPI app, CORS, rate limiting)
- [ ] Criar models Usuario
- [ ] Criar database.py com SQLAlchemy
- [ ] Testar conexão com BD

#### Frontend
- [ ] Criar app React
- [ ] Instalar dependências (axios, react-router)
- [ ] Setup de rotas básicas
- [ ] Criar página Login (mock)

#### Documentação
- [ ] Criar SETUP.md (instruções para rodar projeto)
- [ ] Criar DEVELOPMENT.md (guia de desenvolvimento)

---

## 🔍 Checklist de Verificação (Diário)

### **Dia 1 Final**
- [ ] Backend roda em localhost:8000
- [ ] Frontend roda em localhost:3000
- [ ] BD criado com tabela usuarios
- [ ] Repositório Git com 3 commits

### **Semana 1 Final**
- [ ] POST /auth/register funciona
- [ ] POST /auth/login funciona
- [ ] JWT validado em rotas protegidas
- [ ] Frontend Login/Register telas criadas
- [ ] 5+ testes passando

### **Semana 2 Final**
- [ ] POST /auth/forgot-password funciona
- [ ] POST /auth/reset-password funciona
- [ ] Email de reset envia
- [ ] Frontend Reset password tela funciona
- [ ] 10+ testes passando (auth completo)

### **Semana 4 Final**
- [ ] CRUD Grupos (Create, Read, Update, Deactivate)
- [ ] CRUD Eventos (Create, Read, Update, State transitions)
- [ ] CRUD Partidas (Create, Read, Update)
- [ ] Frontend Grupos/Eventos/Partidas páginas
- [ ] 25+ testes passando

### **Semana 6 Final**
- [ ] ELO cálculo funciona
- [ ] Ranking atualiza em tempo real
- [ ] Estados de jogador funcionam
- [ ] Permissões validadas
- [ ] 40+ testes passando

### **Semana 8 Final**
- [ ] MVP completo funciona
- [ ] 50+ testes passando
- [ ] Deployado em staging
- [ ] Documentação 100% completa
- [ ] README pronto para usuários finais

---

## 🛠️ Tech Stack Detalhado

### Backend

```
Framework: FastAPI 0.104+
Database: SQLite (SQLAlchemy)
Auth: JWT (python-jose)
Password: bcrypt
Email: SMTP (smtplib)
Rate Limit: slowapi
Validation: Pydantic
Testing: pytest, pytest-asyncio
```

### Frontend

```
Framework: React 18+
Routing: React Router v6
HTTP: Axios
UI: CSS/Tailwind (opcional)
Testing: Jest, React Testing Library
```

### DevOps

```
Backend Server: Uvicorn
Frontend Build: npm/Webpack
DB: SQLite (no venv)
Deployment: Heroku/Render/DigitalOcean (v1.1)
```

---

## 📚 Documentação a Criar

### Fase 1 (Esta semana)
- [ ] **SETUP.md** - Como rodar projeto localmente
- [ ] **DEVELOPMENT.md** - Guia para contribuidores
- [ ] **API.md** - Documentação de endpoints (auto-gerado pelo Swagger)
- [ ] **.env.example** - Template de variáveis

### Fase 2 (Sprint 2+)
- [ ] **ARCHITECTURE.md** - ER diagram, fluxos de dados
- [ ] **TESTING.md** - Como rodar testes
- [ ] **DEPLOYMENT.md** - Como fazer deploy
- [ ] **CHANGELOG.md** - Histórico de releases

---

## 🚨 Possíveis Bloqueadores

| Problema | Solução |
|----------|---------|
| Email SMTP não funciona | Usar SendGrid free tier ou Gmail app password |
| CORS errors | Verificar origem em FastAPI CORS middleware |
| JWT token inválido | Garantir SECRET_KEY é mesmo em .env |
| SQLite locking | Usar WAL mode ou migrate para PostgreSQL (v1.1) |
| React build muito lento | Lazy load componentes, otimizar assets |

---

## 💡 Dicas de Produtividade

### Backend
```bash
# Rodar servidor com reload automático
uvicorn main:app --reload --port 8000

# Acessar Swagger docs
http://localhost:8000/docs

# Testar endpoints
python -m pytest tests/
```

### Frontend
```bash
# Rodar servidor dev
npm start

# Build para produção
npm run build

# Testar
npm test
```

### Git Workflow
```bash
# Feature branch
git checkout -b feature/auth-registro

# Commit frequente
git commit -m "feat: implementar registro de usuários"

# Push
git push origin feature/auth-registro

# PR → merge → delete branch
```

---

## 📊 Métricas de Sucesso

### MVP v1.0 Completo
- ✅ 50+ testes unitários passando
- ✅ E2E workflow: register → login → criar evento → partida → ranking
- ✅ 0 bugs críticos
- ✅ Documentação 100% completa
- ✅ Deploy em staging funcionando
- ✅ Tempo < 8 semanas

### Qualidade de Código
- ✅ Code coverage > 80%
- ✅ Sem warnings de lint
- ✅ Senha validada (bcrypt)
- ✅ Todos endpoints com autenticação

---

## 🎓 Recursos de Aprendizado

Se precisar revisar tecnologias:

- **FastAPI**: https://fastapi.tiangolo.com/tutorial/
- **React Hooks**: https://react.dev/reference/react
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **JWT**: https://jwt.io/
- **pytest**: https://docs.pytest.org/

---

## 📞 Suporte e Decisões

### Durante o desenvolvimento

Se encontrar decisões sobre:
- **Banco de Dados**: SQLite é suficiente para MVP, migrar para PostgreSQL em v1.1
- **UI/UX**: Priorizar funcionalidade sobre design em MVP
- **Autenticação**: 2FA adiar para v1.2
- **Notificações**: Adiar para v1.1

### Comunicação
- Manter documento ESPECIFICACAO.md como fonte da verdade
- Documentar decisões em decisões/
- Commit messages em português (ou padrão do time)

---

## ✅ Conclusão

**Pronto para começar?**

1. **Hoje**: Setup do ambiente ✅
2. **Amanhã**: Começar autenticação
3. **Semana 1**: Auth completo
4. **Semana 2-8**: Features core
5. **Fim de Semana 8**: MVP release 🚀

**Tempo estimado**: 6-8 semanas (full-time)  
**Esforço estimado**: 240-320 horas  
**Resultado**: MVP funcional e testado

---

**Boa sorte! 💪**

Para dúvidas durante desenvolvimento, consulte:
- ESPECIFICACAO.md (o que fazer)
- AUTENTICACAO_E_SEGURANCA.md (como fazer segurança)
- Este documento (quando começar)
