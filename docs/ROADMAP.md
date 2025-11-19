# Roadmap Técnico - Racket Hero

**Versão:** 1.0  
**Data:** 19 de Novembro de 2025  
**Owner:** Equipe de Desenvolvimento

---

## 📌 Versões Planejadas

### v1.0 - MVP (ATUAL - Concluído ✅)
**Data de Release:** 19 de Novembro de 2025

**Features Implementadas:**
- [x] Autenticação JWT com roles
- [x] CRUD de eventos
- [x] CRUD de jogadores
- [x] CRUD de partidas
- [x] Cálculo de Elo
- [x] Rankings
- [x] Múltiplos organizadores
- [x] Frontend funcional
- [x] Testes unitários (36/36)
- [x] Documentação

**Database Schema:** v1.0

---

### v1.1 - Estabilidade em Produção (2 semanas)
**Meta:** Pronto para produção

**Tasks:**
```
CRÍTICA (Deve fazer antes de deploy):
  [x] Pydantic V2 migration
  [x] datetime.utcnow() deprecation fix
  [ ] Health check endpoints
  [ ] Docker setup
  [ ] CI/CD pipeline
  
ALTA (Deve fazer na 1ª semana pós-MVP):
  [ ] Logging estruturado com trace IDs
  [ ] Validação de entrada robusta
  [ ] Tratamento de erros centralizado
  [ ] Rate limiting
  [ ] CORS configurado
  
MÉDIA (Nice-to-have):
  [ ] Documentação OpenAPI melhorada
  [ ] Database indexes otimizados
  [ ] Request/response logging
```

**Timeline:** Semana 1-2

---

### v1.2 - Notificações em Tempo Real (4 semanas)
**Meta:** Sistema de notificações funcional

**Features:**
```
Backend:
  [ ] WebSocket support (Socket.IO)
  [ ] Event stream para notificações
  [ ] Fila de mensagens (Redis)
  [ ] Histórico de notificações

Frontend:
  [ ] Toast notifications
  [ ] Real-time updates no ranking
  [ ] Alertas quando partida é criada
  [ ] Alertas quando você é jogador da partida
```

**Database Changes:**
```sql
CREATE TABLE notifications (
  id INTEGER PRIMARY KEY,
  user_id INTEGER,
  event_id INTEGER,
  type VARCHAR(50),
  data JSON,
  read BOOLEAN,
  created_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES usuarios(id)
);

CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read);
```

**Estimado:** 1 semana

---

### v1.3 - Relatórios e Análises (4 semanas)
**Meta:** Dashboard com insights

**Features:**
```
Endpoints:
  GET /api/events/{event_id}/analytics
    - Total de partidas
    - Partidas por dia (gráfico)
    - Jogador mais ativo
    - Taxa de vitória por jogador
    - Distribuição de Elo

  GET /api/events/{event_id}/export
    - CSV com todas as partidas
    - Excel com múltiplas sheets
    - PDF com relatório formatado

  GET /api/users/{user_id}/statistics
    - Histórico de Elo
    - Win rate
    - Streaks (vitórias/derrotas)

Frontend:
  [ ] Dashboard de analytics
  [ ] Gráficos interativos (Chart.js)
  [ ] Exportar dados
```

**Libraries:**
```
Backend:
  openpyxl (Excel)
  reportlab (PDF)
  pandas (Data analysis)
  plotly (Gráficos)

Frontend:
  Chart.js
  react-csv
```

**Estimado:** 1-2 semanas

---

### v1.4 - Integrações Externas (4 semanas)
**Meta:** Conectar com plataformas externas

**Features (selecionar 2-3):**

#### Opção 1: Discord Integration
```python
@router.post("/events/{event_id}/sync/discord")
async def sync_to_discord(event_id: int):
    """Sincronizar evento com canal Discord"""
    return {"status": "synced", "url": "discord_webhook_url"}
```

#### Opção 2: Google Calendar
```python
@router.post("/events/{event_id}/google-calendar")
async def create_calendar_event(event_id: int, user_id: int):
    """Criar evento no Google Calendar do usuário"""
    return {"status": "created", "calendar_url": "..."}
```

#### Opção 3: Cloud Storage (Backup)
```python
@router.post("/admin/backup")
async def backup_to_cloud():
    """Fazer backup do banco de dados para S3/GCS"""
    return {"status": "backed_up", "location": "s3://bucket/backup"}
```

**Escolhido para v1.4:** Aguardando feedback do usuário

**Estimado:** 1-2 semanas cada

---

## 🏗️ Arquitetura Planejada

### v1.0 - Arquitetura Atual
```
┌─────────────┐
│   React     │
│  Frontend   │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌──────────────────────┐
│    FastAPI Server    │
├──────────────────────┤
│  Routers:            │
│  ├─ auth.py         │
│  ├─ events.py       │
│  ├─ players.py      │
│  ├─ matches.py      │
│  └─ ranking.py      │
├──────────────────────┤
│  SQLAlchemy ORM      │
└──────────┬───────────┘
           │
           ▼
    ┌────────────┐
    │  SQLite    │
    │  Database  │
    └────────────┘
```

### v1.2 - Com WebSocket
```
┌─────────────┐
│   React     │
│  Frontend   │
└──────┬──────┘
       │ HTTP/REST + WebSocket
       ▼
┌──────────────────────┐
│    FastAPI Server    │
├──────────────────────┤
│  WebSocket Handler   │
│  Socket.IO Server    │
└──────────┬───────────┘
       ┌───┴────┬────────┐
       ▼        ▼        ▼
    SQLite  Redis    File System
```

### v2.0 - Microserviços (Futuro)
```
┌─────────────┐
│   React     │
│  Frontend   │
└──────┬──────┘
       │
   ┌───┴──────────────┬─────────────┐
   ▼                  ▼             ▼
┌──────────┐    ┌──────────┐   ┌──────────┐
│  Auth    │    │  Events  │   │ Matches  │
│ Service  │    │ Service  │   │ Service  │
└──────┬───┘    └────┬─────┘   └────┬─────┘
       │             │              │
       └─────┬───────┴──────────────┘
             ▼
       ┌──────────────┐
       │  API Gateway │
       └──────────────┘
             │
    ┌────────┴────────┐
    ▼                 ▼
  DB1              DB2
```

---

## 📈 Métricas de Sucesso

### v1.1
- [ ] 0 warnings de deprecação
- [ ] Health check endpoint: resposta < 50ms
- [ ] Rate limit: 1000 req/min por IP
- [ ] Erro rate < 0.1%

### v1.2
- [ ] Notificação entregue < 500ms
- [ ] 99.5% de uptime
- [ ] Suportar 100 conexões WebSocket simultâneas

### v1.3
- [ ] Analytics carregam < 2s
- [ ] Relatório PDF gerado < 5s
- [ ] CSV com 10k partidas < 1s

### v1.4
- [ ] Integração sincronizando < 1s
- [ ] 0 falhas de autenticação com plataforma externa

---

## 🔐 Requisitos de Segurança por Versão

### v1.0 (Atual)
- [x] Autenticação JWT
- [x] Senhas hasheadas
- [x] Validação de entrada (Pydantic)
- [x] SQL injection prevenido (SQLAlchemy)
- [x] XSS prevenido (React)
- [ ] HTTPS (em produção)
- [ ] Rate limiting (TODO v1.1)
- [ ] CORS configurado (TODO v1.1)

### v1.1
- [ ] Rate limiting implementado
- [ ] CORS restritivo
- [ ] Logging de segurança
- [ ] Secrets em variáveis de ambiente
- [ ] HTTPS obrigatório
- [ ] Helmet.js (frontend)

### v1.2+
- [ ] 2FA (Two-Factor Authentication)
- [ ] OAuth2 (login com Google/GitHub)
- [ ] Audit log de ações críticas
- [ ] Data encryption at rest
- [ ] IP whitelisting (opcional)

---

## 📦 Dependências Planejadas

### v1.1
```
Backend:
  - Será removida deprecação, sem novas deps principais

Frontend:
  - Sem mudanças significativas
```

### v1.2
```
Backend:
  + python-socketio[asyncio_client] (WebSocket)
  + redis (Cache/Message Queue)
  + aioredis (Async Redis)

Frontend:
  + socket.io-client (WebSocket client)
```

### v1.3
```
Backend:
  + openpyxl (Excel export)
  + reportlab (PDF generation)
  + pandas (Data analysis)
  + plotly (Visualization)

Frontend:
  + recharts or Chart.js (Charts)
  + react-csv (CSV export)
```

### v1.4
```
Backend:
  - Depende da integração escolhida
  + discord.py (se Discord)
  + google-auth-oauthlib (se Google Calendar)
  + boto3 (se AWS S3)
```

---

## 🗄️ Evolução do Database

### v1.0 (Atual)
```sql
Tables: usuarios, event, player, match, evento_organizador
Indices: PK, FK
Backup: Manual
```

### v1.1
```sql
+ Adicionar indices para:
  - event.usuario_id
  - match.created_at
  - player.event_id
+ Backup automático diário
+ Auditoria via LOG table
```

### v1.2
```sql
+ notifications table
+ notification_preferences table
+ Replicação para hot-standby
```

### v1.3
```sql
+ Particionamento de match (por mês)
+ Agregações pré-computadas para analytics
+ Cache queries em Redis
```

---

## 👥 Roadmap por Stakeholder

### Usuário (Organizador/Jogador)
- v1.0: Criar eventos, registrar partidas ✅
- v1.1: Notificações quando partida criada
- v1.2: Ver ranking em tempo real
- v1.3: Relatórios de desempenho
- v1.4: Sincronizar com Discord

### Admin
- v1.0: Gerenciar usuários ✅
- v1.1: Health check dashboard
- v1.2: Monitoring alerts
- v1.3: Analytics administrativo
- v1.4: Backup automático

### Desenvolvedor
- v1.0: API REST funcional ✅
- v1.1: Docker + CI/CD
- v1.2: WebSocket support
- v1.3: Performance optimization
- v1.4: Microserviços ready

---

## 🚨 Riscos e Mitigação

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Performance degrada com dados grandes | MÉDIA | ALTO | Índices v1.1, Cache v1.2 |
| WebSocket instável em produção | MÉDIA | ALTO | Load testing v1.2 |
| Migração Pydantic V2 quebra código | BAIXA | ALTO | Testes completos antes v1.1 |
| Integração externa falha | MÉDIA | BAIXO | Fallback, retry logic v1.4 |
| Database migration quebra | BAIXA | CRÍTICO | Backup antes cada migration |

---

## 📅 Timeline Estimada

```
Novembro 2025:
  Semana 1: v1.0 MVP concluído ✅
  Semana 2: v1.1 iniciado (Pydantic, Docker, CI/CD)

Dezembro 2025:
  Semana 1: v1.1 completo (Deploy)
  Semana 2-3: v1.2 WebSocket iniciado
  Semana 4: v1.2 concluído

Janeiro 2026:
  Semana 1-2: v1.3 Analytics iniciado
  Semana 3-4: v1.3 concluído

Fevereiro 2026:
  Semana 1-2: v1.4 Integrações
  Semana 3: Revisão + planejamento v2.0

v2.0 (Q2 2026): Microserviços + Escalabilidade
```

---

**Documento Criado:** 19 de Novembro de 2025  
**Próxima Revisão:** Após deploy v1.1  
**Responsável:** Equipe de Desenvolvimento
