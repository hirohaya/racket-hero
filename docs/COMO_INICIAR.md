# 🏓 Como Inicializar o Racket Hero

## ✅ Forma Mais Simples

### **Opção 1: Iniciar Backend e Frontend Juntos**

```powershell
cd C:\Users\hiros\OneDrive\Documents\projetos\racket-hero
.\scripts\start-all-parallel.ps1
```

**Resultado:**
- Backend rodando em: http://127.0.0.1:8000
- Frontend rodando em: http://localhost:3000
- Ambos em paralelo como jobs do PowerShell

**Para verificar status:**
```powershell
Get-Job
```

**Para ver logs do backend:**
```powershell
Receive-Job -Name "RacketHero-Backend" -Keep
```

**Para ver logs do frontend:**
```powershell
Receive-Job -Name "RacketHero-Frontend" -Keep
```

**Para parar tudo:**
```powershell
Stop-Job -Name "RacketHero-*"
Remove-Job -Name "RacketHero-*"
```

---

### **Opção 2: Iniciar Separadamente**

**Backend apenas:**
```powershell
.\scripts\start-backend.ps1
```

**Frontend apenas (desenvolvimento):**
```powershell
.\scripts\start-frontend-dev.ps1
```

---

## 📍 URLs Úteis

| Serviço | URL |
|---------|-----|
| Backend API | http://127.0.0.1:8000 |
| Swagger Docs | http://127.0.0.1:8000/docs |
| Frontend App | http://localhost:3000 |
| Health Check | http://127.0.0.1:8000/health |

---

## 🧪 Testar Rápido

1. **Abrir o frontend:**
   ```
   http://localhost:3000
   ```

2. **Testar registro de usuário:**
   - Clique em "Register"
   - Preencha: email, nome, senha
   - Clique em "Registrar"

3. **Fazer login:**
   - Clique em "Login"
   - Preencha credenciais
   - Clique em "Entrar"

4. **Ver API docs:**
   ```
   http://127.0.0.1:8000/docs
   ```

---

### 📚 Estrutura de Scripts

| Script | Função |
|--------|--------|
| `scripts/start-all-parallel.ps1` | **Inicia backend e frontend juntos** |
| `scripts/start-backend.ps1` | Inicia só backend |
| `scripts/start-frontend-dev.ps1` | Inicia só frontend (desenvolvimento) |
| `scripts/start-frontend.ps1` | Build + serve frontend |
| `scripts/start-all.ps1` | Inicia em janelas separadas |

---

## 💡 Dicas PowerShell

```powershell
# Listar todos os jobs
Get-Job

# Ver output em tempo real
Get-Job -Name "RacketHero-Backend" | Wait-Job -Timeout 5

# Matar um job específico
Stop-Job -Name "RacketHero-Backend"

# Limpar todos os jobs
Get-Job | Remove-Job
```

---

## ⚙️ Se der problema...

### Porta já em uso
```powershell
# Matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Matar processo na porta 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Python/Node não encontrado
```powershell
python --version
node --version
npm --version
```

### Limpar jobs antigos
```powershell
Get-Job | Remove-Job
```

---

**Tudo funcionando? 🎉 Basta rodar:**

```powershell
.\scripts\start-all-parallel.ps1
```

E acessar http://localhost:3000
