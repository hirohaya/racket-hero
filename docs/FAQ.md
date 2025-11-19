# FAQ - Perguntas Frequentes

**Data:** 19 de Novembro de 2025  
**Versão:** 1.0

---

## 🤔 Desenvolvimento

### P: Como começo a desenvolver?
**R:** Veja [DESENVOLVIMENTO_LOCAL.md](DESENVOLVIMENTO_LOCAL.md) para instruções passo a passo.

```bash
git clone https://github.com/hirohaya/racket-hero.git
cd racket-hero/backend && pip install -r requirements.txt
cd ../frontend && npm install
```

---

### P: Onde coloco minhas variáveis de ambiente?
**R:** Crie um arquivo `.env` na pasta apropriada:

```
backend/.env           # Configurações backend
frontend/.env          # Configurações frontend
```

**IMPORTANTE:** Nunca faça commit de `.env`, apenas do `.env.example`.

---

### P: Como executo os testes?
**R:** 
```bash
# Backend
cd backend && pytest tests/test_api.py -v

# Frontend
cd frontend && npm test -- --watchAll=false
```

Todos os 36 testes devem passar (13 backend + 23 frontend).

---

### P: Como contribuo com código?
**R:** 
1. Crie feature branch: `git checkout -b feature/minha-feature`
2. Faça suas mudanças
3. Teste: `pytest` (backend) ou `npm test` (frontend)
4. Commit: `git commit -m "feat: descrição clara"`
5. Push: `git push origin feature/minha-feature`
6. Abra Pull Request no GitHub

---

### P: Qual padrão de código devo seguir?
**R:**
- **Backend:** Python com PEP 8 (use `black` e `pylint`)
- **Frontend:** JavaScript/React (use `prettier` e `eslint`)
- **Nomes:** camelCase (JS), snake_case (Python)
- **Componentes React:** PascalCase
- **Funções:** camelCase
- **Constantes:** UPPER_SNAKE_CASE

---

## 🐛 Bugs & Troubleshooting

### P: Backend não inicia com "ModuleNotFoundError"
**R:** 
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

Se persistir, delete `venv/` e recrie:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### P: Frontend não encontra API (CORS error)
**R:** Verifique se backend está rodando:
```bash
curl http://localhost:8000/health
```

Se der erro, inicie backend:
```bash
cd backend && python -m uvicorn main:app --reload
```

Se CORS ainda falhar, verifique `backend/.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

---

### P: Testes falhando aleatoriamente
**R:** Pode ser problema com banco de dados em estado ruim. Limpe e recrie:
```bash
cd backend
rm racket_hero.db
python -c "from database import Base, engine; Base.metadata.create_all(engine)"
pytest tests/test_api.py -v
```

---

### P: Database "locked" error
**R:** Significa que a database está sendo acessada por múltiplos processos. Para SQLite:
```bash
cd backend
rm -f racket_hero.db-wal racket_hero.db-shm  # Remove lock files
```

---

### P: "ImportError: cannot import name 'X'"
**R:** Arquivo não encontrado ou não exposto em `__init__.py`. Verifique:
1. Arquivo existe em `backend/models/`
2. É importado em `backend/models/__init__.py`

Exemplo:
```python
# backend/models/__init__.py
from models.usuario import Usuario
from models.event import Event
from models.player import Player
from models.match import Match
```

---

## 🚀 Deployment & Produção

### P: Como faço deploy para produção?
**R:** Veja [CHECKLIST_PRODUCAO.md](CHECKLIST_PRODUCAO.md) para guia completo. Resumo:

1. Testes passam: `pytest` (backend) + `npm test` (frontend)
2. Docker pronto: `docker-compose up`
3. Variáveis de ambiente configuradas
4. Backup feito
5. Deploy com `docker push` + `docker-compose pull && up -d`

---

### P: Como faço rollback de deployment?
**R:**
```bash
# Volta para versão anterior
docker-compose up -d app:v1.0

# Se tiver mudança de database, restaura backup
docker exec db psql -U user < backup.sql
```

---

### P: Como monitoro a aplicação em produção?
**R:** Configure os endpoints health check:
```bash
# Status básico
curl https://api.example.com/health

# Status com database
curl https://api.example.com/health/db

# Monitorar a cada 1 minuto
watch curl https://api.example.com/health
```

---

### P: Como faço backup do database?
**R:**
```bash
# Backup manual
docker exec db pg_dump -U user > backup.sql

# Restaurar
docker exec db psql -U user < backup.sql

# Backup automático (cron)
0 2 * * * /scripts/backup.sh  # Todos os dias às 2 AM
```

---

## 📊 Dados & Database

### P: Como populo dados de teste?
**R:** Use script de seed em desenvolvimento:
```bash
cd backend
python scripts/seed_dev.py
```

Contas de teste criadas:
- admin@test.com / Admin123!
- org@test.com / Org123!
- player@test.com / Player123!

---

### P: Como acesso o database diretamente?
**R:**
```bash
# SQLite
sqlite3 backend/racket_hero.db

# Exemplo: Ver usuários
SELECT * FROM usuarios;

# Sair
.quit
```

---

### P: Como resetar o database para estado limpo?
**R:**
```bash
cd backend
rm racket_hero.db
python -c "from database import Base, engine; Base.metadata.create_all(engine)"
python scripts/seed_dev.py  # Opcional: dados de teste
```

---

### P: Como faço uma migration de database?
**R:** Atualmente não usamos Alembic, mudanças são aplicadas diretamente. Para mudanças futuras:
```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Add new table"
alembic upgrade head
```

---

## 🔐 Segurança

### P: Como gerencio senhas/API keys?
**R:** NUNCA coloque em código ou .env versionado. Use variáveis de ambiente:

```python
# ✅ CORRETO
from os import getenv
SECRET_KEY = getenv("SECRET_KEY")

# ❌ ERRADO
SECRET_KEY = "minha-senha-aqui"
```

Em produção, use:
- GitHub Secrets (CI/CD)
- AWS Secrets Manager (AWS)
- HashiCorp Vault (Enterprise)

---

### P: Como reset password de usuário?
**R:** Atualmente não implementado. Para v1.1 será adicionado. Temporariamente:

```bash
# Acessar database e atualizar
sqlite3 backend/racket_hero.db

-- Hash nova senha
UPDATE usuarios SET senha = '$2b$12$...' WHERE email='user@test.com';
```

---

### P: Como verifico se token JWT é válido?
**R:**
```bash
# Decode JWT online
# https://jwt.io/

# Ou via Python
import jwt
token = "seu-token-aqui"
decoded = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
print(decoded)
```

---

## 📱 Frontend

### P: Como adiciono um novo componente?
**R:** 
```bash
# Criar arquivo
touch frontend/src/components/MeuComponente.js

# Template
export default function MeuComponente() {
  return (
    <div>
      {/* Seu conteúdo */}
    </div>
  );
}
```

Depois importe em outra página:
```javascript
import MeuComponente from '../components/MeuComponente';
```

---

### P: Como faço uma chamada à API?
**R:** Use service já criado ou crie novo:
```javascript
// frontend/src/services/api.js
export const fetchData = async (endpoint) => {
  const response = await fetch(`${API_URL}${endpoint}`);
  return response.json();
};

// Usar em componente
import { fetchData } from '../services/api';

useEffect(() => {
  fetchData('/api/events').then(data => {
    // Processar dados
  });
}, []);
```

---

### P: Como estilo componentes?
**R:**
1. **CSS Modules** (recomendado):
   ```css
   /* MeuComponente.module.css */
   .container { ... }
   ```
   ```javascript
   import styles from './MeuComponente.module.css';
   return <div className={styles.container}>...</div>;
   ```

2. **Inline styles**:
   ```javascript
   const styles = { color: 'red' };
   return <div style={styles}>...</div>;
   ```

3. **Tailwind** (se configurado):
   ```javascript
   return <div className="bg-red-500">...</div>;
   ```

---

## 🆘 Suporte

### P: Onde reporto um bug?
**R:** Abra issue no GitHub: https://github.com/hirohaya/racket-hero/issues

Inclua:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado
- Logs/screenshots

---

### P: Como solicito uma feature?
**R:** Abra discussion: https://github.com/hirohaya/racket-hero/discussions

Descreva:
- Caso de uso
- Benefício
- Exemplos de uso

---

### P: Quem contacto com dúvidas?
**R:** 
- GitHub Issues: Bugs e problemas
- GitHub Discussions: Dúvidas e features
- Email: (se configurado)
- Slack: (se tiver)

---

## 📚 Recursos Adicionais

- **Documentação:** `/docs/README.md`
- **API Docs:** http://localhost:8000/docs (Swagger)
- **Código:** GitHub
- **Tests:** `backend/tests/` e `frontend/src/__tests__/`

---

**Última Atualização:** 19 de Novembro de 2025  
**Mantido por:** Equipe de Desenvolvimento

---

## 📝 Feedback

Se esta FAQ não respondeu sua pergunta, abra issue ou discussion no GitHub!
