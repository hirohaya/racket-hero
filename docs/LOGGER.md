# Logger - Sistema de Rastreamento de Eventos

## 📋 Visão Geral

Implementamos um sistema completo de logging para facilitar a depuração em desenvolvimento e produção.

### Componentes

#### 1. Backend Logger (Python)
- **Arquivo**: `backend/logger.py`
- **Recursos**:
  - Logging em console e arquivo simultaneamente
  - Arquivo de log rotativo (10 MB max, 5 backups)
  - 5 níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
  - Formatação padrão: `timestamp - name - level - message`

**Uso**:
```python
from logger import get_logger

log = get_logger("meu-modulo")
log.info("Mensagem de informação")
log.error("Erro ocorreu", extra={"user_id": 123})
```

#### 2. Frontend Logger (JavaScript/React)
- **Arquivo**: `frontend/src/services/logger.js`
- **Recursos**:
  - Logging em console com cores customizadas
  - Persistência em localStorage (máx. 500 logs)
  - Exportação de logs em JSON
  - Download de arquivo de logs

**Uso**:
```javascript
import logger from './services/logger';

logger.info('Login realizado', { email: user.email });
logger.error('Erro ao buscar dados', error.message);
```

#### 3. Página de Debug (Frontend)
- **Arquivo**: `frontend/src/pages/Debug.js`
- **Estilo**: `frontend/src/styles/Debug.css`
- **Rota**: `/debug`

**Funcionalidades**:
- Visualizar logs em tempo real
- Filtrar por nível (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Testar logger enviando mensagens customizadas
- Limpar todos os logs
- Baixar logs como JSON
- Interface responsiva com cores e formatação

## 🔧 Integração

### Backend
- Modificado `main.py` para usar logger no startup
- Logger está pronto para integração em routers e models

### Frontend
- Integrado em `api.js` (requisições e respostas)
- Integrado em `AuthContext.js` (login, registro, logout)
- Página de Debug para visualização e teste

## 📊 Exemplo de Log

```json
{
  "timestamp": "2025-11-14T17:00:54.123Z",
  "level": "INFO",
  "module": "RacketHero",
  "message": "Teste do logger com sucesso!",
  "data": null
}
```

## 🎨 Níveis de Log

| Nível | Cor | Uso |
|-------|-----|-----|
| DEBUG | Cinza | Informações de desenvolvimento |
| INFO | Azul | Eventos importantes |
| WARNING | Amarelo | Situações incomuns |
| ERROR | Vermelho | Erros |
| CRITICAL | Vermelho escuro | Erros críticos |

## 💾 Acesso aos Logs

### Frontend
```javascript
// Ver todos os logs
Logger.getLogs()

// Limpar logs
Logger.clearLogs()

// Exportar como JSON
Logger.exportLogs()

// Baixar como arquivo
Logger.downloadLogs()

// Via localStorage
localStorage.getItem('RACKET_HERO_LOGS')
```

### Backend
- Arquivo: `/backend/logs/app.log`
- Console: Output padrão do Uvicorn

## 📱 Página de Debug

Acesse `http://localhost:3000/debug` para:
1. Testar o logger com mensagens customizadas
2. Visualizar todos os logs em tempo real
3. Filtrar logs por nível
4. Gerenciar (limpar, baixar) logs

## 🚀 Próximas Etapas

1. Integrar logger em todos os routers (`/api/auth/*`, `/api/eventos/*`, etc)
2. Adicionar logging de exceções e erros de validação
3. Implementar níveis de log por ambiente (dev/prod)
4. Análise de logs para monitoramento

## 📝 Notas

- Logs ocupam espaço: máx. 500 no localStorage, 10 MB no arquivo
- Em produção, aumentar retenção de arquivos
- Considerar serviço de análise centralizado (ex: ELK Stack, Sentry)
