# 📁 Scripts do Racket Hero

Pasta com scripts PowerShell para inicializar o backend e frontend em terminais separados.

## 🚀 Uso Rápido

```powershell
# Iniciar tudo (backend + frontend em terminais separados)
.\start-all-new.ps1
```

## 📋 Scripts Disponíveis

### 1. `start-all-new.ps1` ⭐ **RECOMENDADO**
Inicia backend e frontend em terminais separados (foreground).
- Cada servidor roda em seu próprio terminal
- Você vê os logs em tempo real
- Sem jobs em background

```powershell
.\start-all-new.ps1
```

**Resultado:**
- Backend: http://127.0.0.1:8000 (Terminal 1)
- Frontend: http://localhost:3000 (Terminal 2)

### 2. `start-backend.ps1`
Abre o backend em um novo terminal (foreground).

```powershell
.\start-backend.ps1
```

### 3. `start-frontend-dev.ps1`
Abre o frontend em um novo terminal em modo desenvolvimento (foreground).

```powershell
.\start-frontend-dev.ps1
```

### ⚠️ Scripts Antigos (não recomendados)

#### `start-all-parallel.ps1`
Inicia em paralelo como jobs (background) - pode causar conflitos de porta.

#### `start-all.ps1`
Alternativa antiga de terminais separados.

#### `start-frontend.ps1`
Build + serve em modo produção.

## 📖 Documentação Completa

Veja `SCRIPTS.md` para documentação detalhada, troubleshooting e comandos úteis.

## 💡 Acompanhar os servidores

Cada servidor roda em seu próprio terminal, você vê todos os logs em tempo real!

## ⚙️ Se der problema

### Verificar se servidores estão rodando
```powershell
# Checar porta 8000 (backend)
netstat -ano | findstr ":8000.*LISTENING"

# Checar porta 3000 (frontend)
netstat -ano | findstr ":3000.*LISTENING"
```

### Portas já em uso
```powershell
# Encontrar processo na porta 8000
netstat -ano | findstr :8000

# Matar processo (substitua <PID>)
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
├── start-all-new.ps1          # Iniciar tudo (NOVO - recomendado)
├── start-backend.ps1          # Só backend em novo terminal
├── start-frontend-dev.ps1     # Só frontend em novo terminal
├── start-all-parallel.ps1     # Iniciar tudo (jobs - antigo)
├── start-all.ps1              # Iniciar tudo (janelas - antigo)
├── start-frontend.ps1         # Build + serve (antigo)
├── README.md                  # Este arquivo
└── SCRIPTS.md                 # Documentação detalhada
```

---

**Última atualização:** 14 de Novembro de 2025
