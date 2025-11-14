# 🏓 Racket Hero - Scripts de Inicialização

## 📌 Opções Disponíveis

### 1. **Iniciar Tudo em Paralelo (Recomendado)**
```powershell
.\start-all-parallel.ps1
```

**Características:**
- Backend e Frontend iniciam simultaneamente
- Ambos em jobs do PowerShell
- Melhor monitoramento
- Menos abas/janelas abertas

**Saída:**
```
✅ Backend:  http://127.0.0.1:8000
✅ Frontend: http://localhost:3000
✅ Docs:     http://127.0.0.1:8000/docs
```

---

### 2. **Iniciar Tudo em Janelas Separadas**
```powershell
.\start-all.ps1
```

**Características:**
- Backend em uma aba/janela separada
- Frontend em outra aba/janela separada
- Fácil visualizar logs de cada um

---

### 3. **Iniciar Backend Apenas**
```powershell
.\start-backend.ps1
```

Ou:
```bash
cd backend
python main.py
```

**Acesso:**
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/health

---

### 4. **Iniciar Frontend Apenas (Desenvolvimento)**
```powershell
.\start-frontend-dev.ps1
```

Ou:
```bash
cd frontend
npm start
```

**Características:**
- Hot reload ao salvar
- Mais lento para iniciar
- Melhor para desenvolvimento

**Acesso:**
- App: http://localhost:3000

---

### 5. **Build e Servir Frontend (Produção)**
```powershell
.\start-frontend.ps1
```

**Características:**
- Compila React para produção
- Serve com `serve`
- Mais rápido mas sem hot reload

---

## 🛠️ Gerenciar Jobs (PowerShell)

### Ver jobs em execução:
```powershell
Get-Job
```

### Ver logs do backend:
```powershell
Receive-Job -Name "RacketHero-Backend" -Keep
```

### Ver logs do frontend:
```powershell
Receive-Job -Name "RacketHero-Frontend" -Keep
```

### Parar backend:
```powershell
Stop-Job -Name "RacketHero-Backend"
```

### Parar tudo:
```powershell
Stop-Job -Name "RacketHero-*"
```

### Limpar jobs:
```powershell
Remove-Job -Name "RacketHero-*"
```

---

## 📋 URLs Úteis

| Serviço | URL | Descrição |
|---------|-----|-----------|
| Backend API | http://127.0.0.1:8000 | API raiz |
| Swagger UI | http://127.0.0.1:8000/docs | Documentação interativa |
| ReDoc | http://127.0.0.1:8000/redoc | Documentação alternativa |
| Health Check | http://127.0.0.1:8000/health | Status da API |
| Frontend | http://localhost:3000 | Aplicação React |

---

## 🧪 Testar Autenticação

### Registrar novo usuário:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "nome": "Seu Nome",
    "senha": "senha123"
  }'
```

### Login:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "senha": "senha123"
  }'
```

---

## ⚙️ Variáveis de Ambiente

### Backend (.env)
```
DATABASE_URL=sqlite:///./racket_hero.db
SECRET_KEY=sua-chave-secreta-aqui
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 🐛 Troubleshooting

### "Port already in use"
```powershell
# Matar processos na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Matar processos na porta 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Node/npm não encontrado
```powershell
# Verificar instalação
node --version
npm --version

# Reinstalar npm
npm install -g npm
```

### Python não encontrado
```powershell
# Verificar instalação
python --version

# Ativar venv (se existir)
.\venv\Scripts\Activate.ps1
```

---

## 📚 Estrutura do Projeto

```
racket-hero/
├── backend/
│   ├── main.py              # Aplicação FastAPI
│   ├── database.py          # Configuração SQLAlchemy
│   ├── models/              # Modelos SQLAlchemy
│   ├── routers/             # Endpoints da API
│   ├── utils/               # Funções utilitárias
│   └── requirements.txt     # Dependências Python
│
├── frontend/
│   ├── src/
│   │   ├── pages/           # Páginas React
│   │   ├── components/      # Componentes React
│   │   ├── services/        # Serviços (API calls)
│   │   ├── context/         # Context API
│   │   └── hooks/           # Hooks customizados
│   ├── public/              # Arquivos estáticos
│   ├── package.json         # Dependências npm
│   └── .env                 # Variáveis de ambiente
│
├── start-all-parallel.ps1   # Script para iniciar tudo
├── start-all.ps1            # Script alternativo
├── start-backend.ps1        # Iniciar só backend
├── start-frontend-dev.ps1   # Iniciar só frontend
└── README.md                # Este arquivo
```

---

## 🚀 Quick Start

```powershell
# Abrir PowerShell na raiz do projeto
cd C:\Users\hiros\OneDrive\Documents\projetos\racket-hero

# Iniciar tudo
.\start-all-parallel.ps1

# Abrir navegador
Start-Process http://localhost:3000
Start-Process http://127.0.0.1:8000/docs
```

---

## 📝 Notas

- ✅ Backend utiliza FastAPI + SQLite
- ✅ Frontend utiliza React + Context API
- ✅ Autenticação com JWT tokens
- ✅ CORS configurado para localhost:3000
- ⚠️ `.env` não commitado por segurança (usar `.env.example`)

---

**Última atualização:** 14 de Novembro de 2025
