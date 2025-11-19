# Checklist de Produção - Racket Hero

**Documento:** Validação antes de colocar em produção  
**Data:** 19 de Novembro de 2025  
**Status:** Pré-Produção (v1.1 em desenvolvimento)

---

## ✅ Phase 0: Validação Básica (FAZER AGORA)

### Código
- [x] Todos os 36 testes passando
- [ ] Sem warnings de deprecação (Pydantic V1, datetime.utcnow)
- [ ] Sem console.error() no frontend
- [ ] Sem console.log() em código de produção
- [ ] Sem hardcoded credentials/API keys
- [ ] Sem TODO/FIXME não resolvidos (críticos)

### Documentação
- [x] README.md atualizado
- [x] GUIA_IMPLEMENTACAO.md existe
- [x] API documentation completa
- [ ] Procedimento de deploy documentado
- [ ] Guia de troubleshooting
- [ ] Diagrama de arquitetura

### Git
- [x] Código em branch `main`
- [x] Historia clara de commits
- [x] .gitignore configurado
- [ ] README de segurança existe
- [ ] CHANGELOG.md começado
- [ ] Tags de versão (v1.0)

---

## ✅ Phase 1: Validação Técnica (SEMANA 1)

### Backend
- [ ] **CRÍTICA:** Pydantic V2 migration completa
- [ ] **CRÍTICA:** datetime.utcnow() deprecation fix
- [ ] **CRÍTICA:** Health check endpoints implementados
  - [ ] GET /health (status básico)
  - [ ] GET /health/db (conexão BD)
  - [ ] GET /health/deep (verificação completa)
- [ ] Logging estruturado implementado
  - [ ] JSON logging em produção
  - [ ] Trace IDs em requisições
  - [ ] Sem logs de dados sensíveis
- [ ] Tratamento de erros centralizado
- [ ] Rate limiting configurado
  - [ ] 1000 req/min por IP padrão
  - [ ] 100 req/min para auth endpoints
- [ ] CORS configurado corretamente
  - [ ] Whitelist de domínios
  - [ ] Credenciais seguras

### Frontend
- [ ] Build de produção otimizado
- [ ] Sem console logs (exceto erros críticos)
- [ ] Environment variables configuradas
- [ ] API base URL dinâmica (não hardcoded)
- [ ] Error boundaries implementados
- [ ] Fallback para conexão perdida
- [ ] Service workers (se PWA)

### Database
- [ ] Backup automático configurado
- [ ] Recovery procedure testado
- [ ] Índices otimizados criados
- [ ] Queries lentas identificadas
- [ ] Conexão pool configurada

### Infraestrutura
- [ ] **CRÍTICA:** Docker setup completo
  - [ ] Dockerfile backend
  - [ ] Dockerfile frontend (nginx)
  - [ ] docker-compose.yml
  - [ ] .dockerignore configurado
- [ ] **CRÍTICA:** CI/CD pipeline funcional
  - [ ] GitHub Actions para testes
  - [ ] Linting automático
  - [ ] Build automático
  - [ ] Deploy automático (opcional)

---

## ✅ Phase 2: Validação de Segurança (SEMANA 1)

### Autenticação & Autorização
- [ ] JWT tokens com expiração apropriada
  - [ ] Access token: 15 minutos
  - [ ] Refresh token: 7 dias
- [ ] Refresh token rotation implementado
- [ ] Logout invalida tokens
- [ ] Roles/permissions funcionando
- [ ] Admin endpoints protegidos
- [ ] Cross-site scripting (XSS) prevenido
- [ ] Cross-site request forgery (CSRF) prevenido (se needed)

### Dados & Privacidade
- [ ] Senhas hasheadas (bcrypt)
- [ ] Sem dados sensíveis em logs
- [ ] Sem dados sensíveis em errors
- [ ] Database credentials em variáveis de ambiente
- [ ] API keys em variáveis de ambiente
- [ ] Secrets não estão no git
- [ ] Dados PII (Personally Identifiable) protegidos

### Rede & APIs
- [ ] HTTPS obrigatório (em produção)
- [ ] SSL/TLS certificado válido
- [ ] Headers de segurança configurados
  - [ ] Strict-Transport-Security
  - [ ] X-Content-Type-Options
  - [ ] X-Frame-Options
  - [ ] Content-Security-Policy
- [ ] CORS restritivo (não `*`)
- [ ] SQL injection prevenido (SQLAlchemy)
- [ ] NoSQL injection prevenido
- [ ] Command injection prevenido
- [ ] Path traversal prevenido

### Validação de Entrada
- [ ] Todos os inputs validados
- [ ] Pydantic schemas em todas as rotas
- [ ] Email validation
- [ ] Phone validation (se applicable)
- [ ] File upload validation (se applicable)
- [ ] Max request size limitado
- [ ] Max file size limitado

### Rate Limiting & DDoS
- [ ] Rate limiting por IP
- [ ] Rate limiting por usuário
- [ ] Rate limiting por endpoint
- [ ] Captcha (se aplicável)
- [ ] Detecção de bot

### Auditoria & Logging
- [ ] Eventos críticos logados
  - [ ] Login/logout
  - [ ] Mudanças de permissão
  - [ ] Exclusão de dados
  - [ ] Mudanças de config
- [ ] Logs mantidos por 90 dias
- [ ] Logs protegidos contra modificação
- [ ] Alertas para eventos suspeitos

---

## ✅ Phase 3: Testes (SEMANA 1)

### Testes Unitários
- [x] Backend: 13/13 testes passando
- [x] Frontend: 23/23 testes passando
- [ ] Cobertura > 80% (backend)
- [ ] Cobertura > 70% (frontend)
- [ ] Testes de edge cases
- [ ] Testes de error paths

### Testes de Integração
- [ ] API endpoints funcionam end-to-end
- [ ] Frontend → Backend → Database ciclo completo
- [ ] Autenticação funciona
- [ ] Permissões funcionam
- [ ] Elo calculation correto
- [ ] Rankings atualizados corretamente

### Testes de Carga
- [ ] Load test com 100 usuários simultâneos
- [ ] Load test com 1000 req/min
- [ ] Resposta < 200ms (p95)
- [ ] Erro rate < 0.1%
- [ ] Database não trava

### Testes de Segurança
- [ ] SQL injection test
- [ ] XSS test
- [ ] CSRF test
- [ ] Token expiration test
- [ ] Permission bypass test
- [ ] Rate limiting test

### Teste de Recuperação
- [ ] Banco de dados restaura corretamente
- [ ] Aplicação relança sem problemas
- [ ] Cache invalida corretamente
- [ ] Sessões recuperam

---

## ✅ Phase 4: Operacionalização (SEMANA 2)

### Monitoramento
- [ ] Health check executado a cada 1 min
- [ ] Alertas para status != "ok"
- [ ] Alertas para erro rate > 1%
- [ ] Alertas para resposta > 2s (p95)
- [ ] Alertas para database não acessível
- [ ] Alerts enviados para Slack/Email

### Logging & Observabilidade
- [ ] Logs centralizados (se possível)
- [ ] Search em logs funciona
- [ ] Alertas para padrões suspeitos
- [ ] Retenção de logs: 90 dias
- [ ] Backup de logs

### Performance Monitoring
- [ ] Tempo de resposta por endpoint
- [ ] Query database performance
- [ ] Cache hit rate
- [ ] Memory usage
- [ ] CPU usage
- [ ] Disk space

### Uptime & SLA
- [ ] Uptime target: 99.5%
- [ ] RTO (Recovery Time Objective): < 1 hora
- [ ] RPO (Recovery Point Objective): < 1 hora
- [ ] Notificação de downtime: < 15 min

### Backup & Disaster Recovery
- [ ] Backup automático diário
- [ ] Backup armazenado em local diferente
- [ ] Backup testado a cada semana
- [ ] Procedimento de restore documentado
- [ ] Procedimento de failover documentado

### Escalabilidade
- [ ] Load balancer configurado (se needed)
- [ ] Auto-scaling configurado (se needed)
- [ ] Database replicação (se needed)
- [ ] Cache distribuído (se needed)

---

## ✅ Phase 5: Planejamento de Incidentes (SEMANA 2)

### Incident Response
- [ ] Processo de escalation definido
- [ ] Contatos de emergência listados
- [ ] Procedimento post-mortem definido
- [ ] Runbook para problemas comuns

### Comunicação
- [ ] Status page pública (se aplicável)
- [ ] Notificação de downtime automática
- [ ] SLA de resposta: < 15 minutos
- [ ] SLA de resolução: < 4 horas

### Documentação de Operação
- [ ] Procedimento de deploy
- [ ] Procedimento de rollback
- [ ] Procedimento de scaling
- [ ] Procedimento de backup/restore
- [ ] Checklist de manutenção

---

## ✅ Phase 6: Pré-Deploy (DIA 1)

### 24 horas antes do Deploy

#### Código
```bash
# Verificar testes
cd backend && pytest tests/ -v
cd frontend && npm test

# Verificar build
npm run build

# Verificar security
cd backend && bandit -r . -ll
```

- [ ] Todos os testes passando
- [ ] Build sem warnings
- [ ] Security scanning sem críticos

#### Aprovações
- [ ] Code review completado
- [ ] Security review completado
- [ ] Performance review completado
- [ ] Operações aprovado
- [ ] Product manager aprovado (se aplicável)

#### Preparação
- [ ] Backup do database feito
- [ ] Backup testado
- [ ] Plano de rollback pronto
- [ ] Comunicação pronta
- [ ] Equipe on-call confirmada

---

## ✅ Phase 7: Deploy (DIA 1)

### Janela de Deploy
- [ ] Horário escolhido (low-traffic time)
- [ ] Duração estimada < 30 minutos
- [ ] Rollback time < 10 minutos

### Antes de Deploy
```bash
# 1. Backup
docker exec db pg_dump -U user > backup.sql

# 2. Verificar health atual
curl https://api.example.com/health

# 3. Log em servidor
ssh deploy@server
```

- [ ] Database backed up
- [ ] Current logs arquivo
- [ ] Servidores check status

### Deploy
```bash
# 1. Build imagens
docker build -t app:v1.1 .

# 2. Push para registry
docker push app:v1.1

# 3. Atualizar compose
docker-compose up -d app:v1.1

# 4. Verificar logs
docker logs -f app

# 5. Teste health
curl http://localhost:8000/health
```

- [ ] Build sucesso
- [ ] Push sucesso
- [ ] Containers started
- [ ] Logs sem erros
- [ ] Health check ok

### Pós-Deploy
```bash
# 1. Verificar endpoints
curl https://api.example.com/health
curl https://api.example.com/api/auth/login -X OPTIONS

# 2. Teste fluxo completo
# - Fazer login
# - Criar evento
# - Registrar partida
# - Verificar ranking

# 3. Monitorar
watch 'curl http://localhost:8000/health'
```

- [ ] Todos endpoints respondendo
- [ ] Fluxo completo funcionando
- [ ] Sem erros nos logs
- [ ] Métricas normais
- [ ] Usuários não reportam issues

### Rollback (se needed)
```bash
# 1. Voltar versão anterior
docker-compose up -d app:v1.0

# 2. Restaurar database (se migration)
docker exec db psql -U user < backup.sql

# 3. Verificar saúde
curl http://localhost:8000/health
```

---

## ✅ Phase 8: Pós-Deploy (Primeiros 7 dias)

### Monitoramento Intensivo
- [ ] Health checks a cada 5 minutos
- [ ] Verificar logs a cada 30 minutos
- [ ] Acompanhar métricas
- [ ] Estar disponível para problemas

### Validação Funcional
- [ ] Testar cada feature manualmente
- [ ] Testar com dados reais
- [ ] Verificar performance
- [ ] Verificar security

### Feedback de Usuários
- [ ] Responder issues rapidamente
- [ ] Documentar bugs encontrados
- [ ] Preparar hotfixes se needed
- [ ] Planejar v1.1.1 se critical

### Estabilização (Dia 7)
- [ ] 0 erros críticos
- [ ] Performance estável
- [ ] Usuários satisfeitos
- [ ] Passar para sustentação

---

## 🔄 Checklist de Manutenção (Mensal)

- [ ] Executar security scanning
- [ ] Testar backup/restore
- [ ] Revisar logs de erro
- [ ] Atualizar dependências (patch)
- [ ] Otimizar queries lentas
- [ ] Revisar storage usage
- [ ] Testar procedimento de escalabilidade

---

## 📋 Assinaturas de Aprovação

**Pronto para produção quando todos os itens estão marcados como [x]**

| Função | Nome | Data | Assinatura |
|--------|------|------|-----------|
| Tech Lead | _____________ | ___/___/___ | ____________ |
| DevOps | _____________ | ___/___/___ | ____________ |
| Security | _____________ | ___/___/___ | ____________ |
| Product | _____________ | ___/___/___ | ____________ |

---

**Documento Criado:** 19 de Novembro de 2025  
**Próxima Revisão:** Após v1.1 deploy  
**Responsável:** Tech Lead
