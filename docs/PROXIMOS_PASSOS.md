# Próximos Passos - Racket Hero

**Última Atualização:** 19 de Novembro de 2025  
**Status do Projeto:** MVP Concluído ✅  
**Testes:** 36/36 Passando  
**Branch:** main

---

## 📋 Visão Geral

O projeto Racket Hero está em fase **MVP (Produto Viável Mínimo)** com:
- ✅ Backend API completo (13 endpoints testados)
- ✅ Frontend funcional (23 componentes testados)
- ✅ Sistema de autenticação (JWT + roles)
- ✅ Cálculo de Elo implementado
- ✅ Gerenciamento de eventos e partidas
- ✅ Suporte a múltiplos organizadores

---

## 🚀 Próximos Passos Prioritários

### Fase 1: Preparação para Produção (1-2 semanas)

#### 1.1 Migração Pydantic V1 → V2
**Prioridade:** 🔴 CRÍTICA  
**Arquivo:** `backend/schemas/auth.py`

**O que fazer:**
```python
# ANTES (V1 - Deprecado):
from pydantic import BaseModel, validator

class RegistroRequest(BaseModel):
    class Config:
        schema_extra = {...}
    
    @validator('nome')
    def validate_nome(cls, v):
        ...

# DEPOIS (V2 - Novo):
from pydantic import BaseModel, field_validator, ConfigDict

class RegistroRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={...})
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v):
        ...
```

**Arquivos afetados:**
- `backend/schemas/auth.py` (13 warnings)
- `backend/schemas/matches.py` (2 warnings)

**Estimado:** 30 minutos

---

#### 1.2 Remover `datetime.utcnow()` Deprecado
**Prioridade:** 🟡 ALTA  
**Arquivos:** `backend/logger_production.py`, `backend/utils/security.py`

**O que fazer:**
```python
# ANTES:
import datetime
'timestamp': datetime.datetime.utcnow().isoformat()

# DEPOIS:
from datetime import datetime, timezone
'timestamp': datetime.now(timezone.utc).isoformat()
```

**Estimado:** 15 minutos

---

#### 1.3 Adicionar Health Check Endpoint
**Prioridade:** 🟡 ALTA  
**Arquivo:** `backend/main.py`

**O que fazer:**
```python
@app.get("/health")
async def health_check():
    """Verificar status da aplicação"""
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health/db")
async def health_check_db(db: Session = Depends(get_db)):
    """Verificar conexão com banco de dados"""
    try:
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}, 503
```

**Estimado:** 20 minutos

---

### Fase 2: Melhorias de Código (2-3 semanas)

#### 2.1 Implementar Logging Estruturado
**Prioridade:** 🟡 ALTA

**Ações:**
1. Adicionar IDs de rastreamento (trace ID) em todas as requisições
2. Implementar middleware de logging
3. Estruturar logs em JSON (já temos `logger_production.py`)

**Exemplo:**
```python
@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = str(uuid4())
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    return response
```

**Estimado:** 2 horas

---

#### 2.2 Implementar Validação de Entrada Robusta
**Prioridade:** 🟡 ALTA

**Ações:**
1. Adicionar validação de email (já existe em `schemas/auth.py`)
2. Adicionar rate limiting
3. Sanitizar entrada de usuário

**Ferramentas:**
```bash
pip install python-multipart email-validator slowapi
```

**Estimado:** 3 horas

---

#### 2.3 Adicionar Tratamento de Erros Centralizado
**Prioridade:** 🟡 MÉDIA

**Ações:**
1. Criar `backend/utils/exceptions.py` com exceções customizadas
2. Implementar global exception handler

**Exemplo:**
```python
class ResourceNotFoundError(Exception):
    def __init__(self, resource: str, resource_id: int):
        self.message = f"{resource} with ID {resource_id} not found"

class InsufficientPermissionsError(Exception):
    def __init__(self, required_permission: str):
        self.message = f"Required permission: {required_permission}"
```

**Estimado:** 2 horas

---

### Fase 3: Funcionalidades Adicionais (3-4 semanas)

#### 3.1 Sistema de Notificações
**Prioridade:** 🟠 MÉDIA

**O que fazer:**
- [ ] Implementar WebSocket para notificações em tempo real
- [ ] Notificar quando partida é criada/atualizada
- [ ] Notificar quando ranking é atualizado

**Bibliotecas:**
```bash
pip install websockets python-socketio aioredis
```

**Estimado:** 1 semana

---

#### 3.2 Relatórios e Análises
**Prioridade:** 🟠 MÉDIA

**Endpoints a adicionar:**
```
GET /api/events/{event_id}/analytics
  - Número de partidas por dia
  - Jogador mais ativo
  - Taxa de vitória por jogador

GET /api/events/{event_id}/export
  - Exportar dados em CSV/Excel
  - Gerar relatório em PDF
```

**Bibliotecas:**
```bash
pip install openpyxl reportlab pandas
```

**Estimado:** 1 semana

---

#### 3.3 Integrações Externas
**Prioridade:** 🟠 BAIXA

**Opções:**
- [ ] Integração com Discord/Slack (notificações)
- [ ] Integração com Google Calendar (agendar eventos)
- [ ] Integração com Cloud Storage (backup de dados)

**Estimado:** 2 semanas

---

### Fase 4: Infraestrutura e Deploy (2-3 semanas)

#### 4.1 Containerização (Docker)
**Prioridade:** 🔴 CRÍTICA (para produção)

**O que fazer:**
1. Criar `Dockerfile` para backend
2. Criar `Dockerfile` para frontend
3. Criar `docker-compose.yml` para orquestração

**Exemplo Dockerfile (Backend):**
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Estimado:** 2 horas

---

#### 4.2 CI/CD Pipeline
**Prioridade:** 🔴 CRÍTICA (para produção)

**Usar GitHub Actions:**

**Arquivo:** `.github/workflows/tests.yml`
```yaml
name: Tests
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest tests/ -v

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: cd frontend && npm install
      - run: cd frontend && npm test -- --watchAll=false
```

**Estimado:** 3 horas

---

#### 4.3 Deploy em Produção
**Prioridade:** 🔴 CRÍTICA

**Opções:**
1. **Railway** (Recomendado para MVP)
   - Fácil de usar
   - Suporte a GitHub Actions
   - PostgreSQL incluído

2. **Heroku** (Alternativa)
   - Simples de fazer deploy
   - Scaling automático

3. **AWS/Google Cloud** (Enterprise)
   - Mais controle
   - Mais caro

**Estimado:** 1-2 horas (Railway)

---

#### 4.4 Monitoramento e Observabilidade
**Prioridade:** 🟡 ALTA (pós-deploy)

**Ferramentas:**
```bash
pip install prometheus-client sentry-sdk
```

**O que monitorar:**
- Disponibilidade da API
- Tempo de resposta
- Taxa de erro
- Uso de banco de dados

**Estimado:** 3 horas

---

### Fase 5: Otimizações (Contínuo)

#### 5.1 Otimização de Performance
**Prioridade:** 🟠 MÉDIA

**Ações:**
- [ ] Adicionar índices no banco de dados
- [ ] Implementar cache (Redis)
- [ ] Otimizar queries N+1
- [ ] Compressão de assets frontend

**Estimado:** 1 semana

---

#### 5.2 Segurança
**Prioridade:** 🔴 CRÍTICA

**Checklist:**
- [ ] HTTPS obrigatório em produção
- [ ] CORS configurado corretamente
- [ ] Rate limiting implementado
- [ ] SQL injection prevenido (já feito com SQLAlchemy)
- [ ] XSS prevenido (já feito com React)
- [ ] CSRF tokens em formulários
- [ ] Dados sensíveis não logados
- [ ] Senhas hasheadas (já feito com bcrypt)

**Ferramentas:**
```bash
pip install python-multipart secure
```

**Estimado:** 1 semana

---

#### 5.3 Testes de Carga
**Prioridade:** 🟠 MÉDIA (pré-deploy)

**Ferramentas:**
```bash
pip install locust
```

**O que testar:**
- 100 usuários simultâneos
- 1000 requisições/segundo
- Tempo de resposta sob carga

**Estimado:** 1 dia

---

## 📊 Timeline Recomendado

```
Semana 1: Fase 1 (Produção Ready)
  ├─ Pydantic V2
  ├─ datetime.utcnow() fix
  ├─ Health check endpoint
  └─ Testes passando

Semana 2-3: Fase 2 (Código de Qualidade)
  ├─ Logging estruturado
  ├─ Validação robusta
  └─ Tratamento de erros

Semana 4: Fase 4.1-4.3 (Deploy)
  ├─ Docker
  ├─ CI/CD GitHub Actions
  └─ Deploy em Railway

Semana 5+: Fase 3 + Otimizações
  ├─ Notificações (WebSocket)
  ├─ Relatórios
  └─ Monitoramento
```

---

## 🔍 Checklist de Produção

### Antes de Deploy

- [ ] Todos os testes passando (36/36)
- [ ] Migração Pydantic V1 → V2
- [ ] Sem warnings de deprecação
- [ ] Health check endpoint funcional
- [ ] Logging estruturado
- [ ] HTTPS configurado
- [ ] Rate limiting implementado
- [ ] Backup automático do banco de dados
- [ ] Variáveis de ambiente configuradas
- [ ] Database pronto em produção
- [ ] Secrets seguros (não em git)

### Após Deploy

- [ ] Monitoramento configurado
- [ ] Alertas definidos
- [ ] Logs centralizados
- [ ] Backup testado
- [ ] Plano de disaster recovery
- [ ] SLA documentado

---

## 📚 Recursos Úteis

### Documentação
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Pydantic V2](https://docs.pydantic.dev/latest/)
- [React Docs](https://react.dev/)

### Ferramentas
- [Railway](https://railway.app/)
- [GitHub Actions](https://github.com/features/actions)
- [Sentry](https://sentry.io/)
- [Prometheus](https://prometheus.io/)

### Segurança
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

---

## 🎯 KPIs de Sucesso

- [ ] Tempo de resposta < 200ms (p95)
- [ ] Taxa de erro < 0.1%
- [ ] Uptime > 99.5%
- [ ] Cobertura de testes > 80%
- [ ] Latência de deploy < 5 minutos

---

## 📞 Suporte

Para dúvidas ou blockers:
1. Verificar documentação existente
2. Consultar código de exemplo
3. Abrir issue no GitHub

---

**Criado por:** GitHub Copilot  
**Data:** 19 de Novembro de 2025  
**Versão:** 1.0
