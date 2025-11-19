# 🚀 Guia de Implementação - Próximos Passos Críticos

**Objetivo**: Integrar testes, logging, backup e validações ao sistema existente  
**Tempo estimado**: 2-3 horas  
**Prioridade**: CRÍTICA antes de produção

---

## 📝 Passo 1: Integrar Testes Existentes ao Backend

### 1.1 Instalar dependências
```bash
cd backend
pip install pytest pytest-asyncio httpx
```

### 1.2 Executar testes
```bash
# Rodar todos os testes
pytest tests/ -v

# Rodar com cobertura
pytest tests/ --cov=. --cov-report=html
```

### 1.3 Esperado
- Testes de models: ~12 testes
- Testes de API: ~15 testes
- Coverage: ~65-75%

---

## 🎨 Passo 2: Integrar Testes Frontend

### 2.1 Instalar dependências
```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom jest @babel/preset-react @babel/preset-env
```

### 2.2 Configurar Jest
Criar `frontend/jest.config.js`:
```javascript
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
};
```

### 2.3 Criar setup de testes
Criar `frontend/src/setupTests.js`:
```javascript
import '@testing-library/jest-dom';
```

### 2.4 Executar testes
```bash
npm test -- --coverage
```

---

## 📊 Passo 3: Integrar Logging Production

### 3.1 Atualizar `backend/main.py`

Adicionar no início:
```python
import logging
from logger_production import setup_logging

# Configurar logging
log = setup_logging(
    log_level=logging.INFO,
    log_dir='logs',
    json_format=True
)

log.info("Racket Hero iniciado")
```

### 3.2 Usar logging em routers

Exemplo em `backend/routers/events.py`:
```python
from logger_production import get_logger

logger = get_logger('events')

@router.post("/", status_code=201)
async def create_event(event_data: EventCreateSchema, db: Session = Depends(get_db)):
    logger.info(f"Criando evento: {event_data.name}")
    # ... criar evento
    logger.info(f"Evento criado com sucesso: {event.id}")
    return event
```

### 3.3 Criar diretório de logs
```bash
mkdir -p backend/logs
```

### 3.4 Verificar logs
```bash
# Logs em tempo real
tail -f backend/logs/app.log

# Ver erros
cat backend/logs/errors.log
```

---

## 💾 Passo 4: Integrar Backup Automático

### 4.1 Instalar dependência (opcional, para agendamento)
```bash
pip install apscheduler
```

### 4.2 Atualizar `backend/main.py`

Adicionar imports:
```python
from backup_manager import backup_endpoint_handler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
```

Adicionar no startup da app:
```python
# Agendar backups diários (3 da manhã)
scheduler = BackgroundScheduler()
scheduler.add_job(
    backup_endpoint_handler,
    trigger=CronTrigger(hour=3, minute=0),
    id='daily_backup',
    name='Daily database backup'
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

log.info("Backup agendador iniciado")
```

### 4.3 Criar endpoint de backup (admin only)
```python
# Em backend/routers/admin.py (novo arquivo)
from fastapi import APIRouter, Depends
from backup_manager import backup_endpoint_handler, BackupManager

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/backup")
async def manual_backup(current_user = Depends(get_current_admin_user)):
    """Criar backup manual do banco de dados"""
    return backup_endpoint_handler()

@router.get("/backups")
async def list_backups(current_user = Depends(get_current_admin_user)):
    """Listar todos os backups disponíveis"""
    manager = BackupManager()
    return {"backups": manager.list_backups()}

@router.post("/backups/{filename}/restore")
async def restore_backup(filename: str, current_user = Depends(get_current_admin_user)):
    """Restaurar banco de um backup"""
    manager = BackupManager()
    success, msg = manager.restore_backup(filename)
    return {"success": success, "message": msg}
```

### 4.4 Testar backup
```bash
# Criar backup manual
curl -X POST http://localhost:8000/api/admin/backup \
  -H "Authorization: Bearer TOKEN"

# Listar backups
curl http://localhost:8000/api/admin/backups \
  -H "Authorization: Bearer TOKEN"
```

---

## 🔐 Passo 5: Integrar Validações Robustas

### 5.1 Atualizar routers para usar schemas validados

Exemplo em `backend/routers/auth.py`:
```python
from validators import UsuarioRegisterSchema, UsuarioLoginSchema

@router.post("/register", status_code=201)
async def register(user: UsuarioRegisterSchema, db: Session = Depends(get_db)):
    """Registrar novo usuário (dados validados por Pydantic)"""
    # user já foi validado, pode usar diretamente
    usuario = Usuario(
        email=user.email,
        nome=user.nome,
        senha_hash=hash_password(user.password),
        tipo=user.tipo
    )
    # ... salvar
```

### 5.2 Atualizar routers de eventos
```python
from validators import EventCreateSchema

@router.post("/", status_code=201)
async def create_event(event: EventCreateSchema, db: Session = Depends(get_db)):
    """Criar evento (data/hora validadas)"""
    new_event = Event(
        name=event.name,
        date=event.date,
        time=event.time,
        active=event.active
    )
    # ... salvar
```

### 5.3 Atualizar routers de jogadores
```python
from validators import PlayerCreateSchema

@router.post("/", status_code=201)
async def create_player(player: PlayerCreateSchema, db: Session = Depends(get_db)):
    """Criar jogador (nome, Elo, club validados)"""
    new_player = Player(
        event_id=player.event_id,
        name=player.name,
        club=player.club,
        initial_elo=player.initial_elo
    )
    # ... salvar
```

### 5.4 Atualizar routers de partidas
```python
from validators import MatchCreateSchema, MatchUpdateSchema

@router.post("/", status_code=201)
async def create_match(match: MatchCreateSchema, db: Session = Depends(get_db)):
    """Criar partida (jogadores e winner validados)"""
    new_match = Match(
        event_id=match.event_id,
        player_1_id=match.player_1_id,
        player_2_id=match.player_2_id,
        winner_id=match.winner_id  # Pode ser None!
    )
    # ... salvar
```

---

## ✅ Passo 6: Checklist de Integração

- [ ] Testes backend rodando com sucesso
- [ ] Testes frontend rodando com sucesso
- [ ] Logging criando arquivos em `logs/`
- [ ] Backup criando arquivos em `backups/`
- [ ] Endpoints de admin protegidos (admin only)
- [ ] Validações retornando erro 422 em dados inválidos
- [ ] Todos os routers atualizados com schemas validados

---

## 🧪 Passo 7: Testar Tudo Junto

### 7.1 Iniciar backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### 7.2 Iniciar frontend
```bash
cd frontend
npm start
```

### 7.3 Teste manual (Postman/cURL)

**Registrar novo usuário (validação de senha)**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@test.com",
    "nome": "Teste User",
    "password": "Fraca",  # ❌ Deve falhar
    "tipo": "jogador"
  }'

# Resposta esperada: 422 Unprocessable Entity
```

**Criar evento com data no passado**:
```bash
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Torneio",
    "date": "2020-01-01",  # ❌ Data no passado
    "time": "14:00"
  }'

# Resposta esperada: 422 Unprocessable Entity
```

**Criar partida sem vencedor (deve funcionar)**:
```bash
curl -X POST http://localhost:8000/api/matches \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "player_1_id": 1,
    "player_2_id": 2,
    "winner_id": null  # ✅ Permitido!
  }'

# Resposta esperada: 201 Created
```

---

## 📊 Passo 8: Relatório Final

Após completar todos os passos:

```bash
# Coverage dos testes
pytest tests/ --cov=. --cov-report=term-missing

# Verificar logs criados
ls -lah backend/logs/

# Verificar backups criados
ls -lah backend/backups/

# Contar testes
grep -r "def test_" backend/tests/ frontend/src/__tests__/ | wc -l
```

---

## 🎯 Tempo Estimado

| Tarefa | Tempo |
|--------|-------|
| Passo 1-2: Testes | 30 min |
| Passo 3: Logging | 20 min |
| Passo 4: Backup | 20 min |
| Passo 5: Validações | 30 min |
| Passo 6-8: Integração e Testes | 30 min |
| **Total** | **~2.5 horas** |

---

## ⚠️ Troubleshooting

### Testes falhando
```bash
# Limpar cache de Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Logging não aparece
- Verificar permissões da pasta `logs/`
- Confirmar nível de log em logger_production.py
- Ver se há exceção ao criar arquivo

### Backup não funciona
- Verificar se arquivo `racket_hero.db` existe
- Confirmar permissões de escrita em `backups/`
- Testar manualmente: `python backend/backup_manager.py`

---

**Próximo Status**: Todos os 4 passos críticos implementados e testados  
**Recomendação**: Fazer deploy em staging antes de produção
