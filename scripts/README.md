# 📁 Scripts do Racket Hero

Pasta com scripts PowerShell para inicializar o backend e frontend.

## 🚀 Uso Rápido

```powershell
# Iniciar tudo (backend + frontend)
.\start-all-parallel.ps1
```

## 📋 Scripts Disponíveis

### 1. `start-all-parallel.ps1` ⭐ **RECOMENDADO**
Inicia backend e frontend em paralelo como jobs do PowerShell.

```powershell
.\start-all-parallel.ps1
```

**Resultado:**
- Backend: http://127.0.0.1:8000
- Frontend: http://localhost:3000

### 2. `start-all.ps1`
Inicia backend e frontend em janelas/abas separadas.

```powershell
.\start-all.ps1
```

### 3. `start-backend.ps1`
Inicia apenas o servidor FastAPI.

```powershell
.\start-backend.ps1
```

### 4. `start-frontend-dev.ps1`
Inicia apenas o frontend em modo desenvolvimento (com hot reload).

```powershell
.\start-frontend-dev.ps1
```

### 5. `start-frontend.ps1`
Faz build e serve o frontend em modo produção.

```powershell
.\start-frontend.ps1
```

## 📖 Documentação Completa

Veja `SCRIPTS.md` para documentação detalhada, comandos úteis e troubleshooting.

## 💡 Gerenciar Jobs (PowerShell)

```powershell
# Ver status dos jobs
Get-Job

# Ver logs do backend
Receive-Job -Name "RacketHero-Backend" -Keep

# Ver logs do frontend
Receive-Job -Name "RacketHero-Frontend" -Keep

# Parar um job
Stop-Job -Name "RacketHero-Backend"

# Parar tudo
Stop-Job -Name "RacketHero-*"

# Limpar jobs
Get-Job | Remove-Job
```

## ⚙️ Se der problema

### Portas já em uso
```powershell
# Encontrar processo na porta 8000
netstat -ano | findstr :8000

# Matar processo
taskkill /PID <PID> /F
```

### Scripts não executam
Se receber erro de execução:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📂 Estrutura

```
scripts/
├── start-all-parallel.ps1     # Iniciar tudo (paralelo)
├── start-all.ps1              # Iniciar tudo (janelas separadas)
├── start-backend.ps1          # Só backend
├── start-frontend-dev.ps1     # Só frontend (dev)
├── start-frontend.ps1         # Só frontend (build+serve)
├── README.md                  # Este arquivo
└── SCRIPTS.md                 # Documentação detalhada
```

---

**Última atualização:** 14 de Novembro de 2025
