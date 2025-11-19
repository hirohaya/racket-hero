# SETUP.md - Instruções de Configuração

## 🔧 Setup Completo do Racket Hero

Guia passo-a-passo para rodar o projeto localmente.

---

## Pré-requisitos

- Python 3.9+
- Node.js 16+ (com npm)
- Git
- Editor de código (VS Code recomendado)

**Verificar instalação**:
```bash
python --version
node --version
npm --version
git --version
```

---

## 1️⃣ Clone do Repositório

```bash
# Clone o repositório
git clone https://github.com/hirohaya/racket-hero.git
cd racket-hero

# Verificar branch main
git branch -a
```

---

## 2️⃣ Setup Backend

### 2.1 Criar Virtual Environment

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Você deve ver `(venv)` no início da linha de comando.

### 2.2 Instalar Dependências

```bash
# Upgrade pip (importante!)
pip install --upgrade pip

# Instalar requirements
pip install -r requirements.txt
```

**Dependências instaladas**:
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- bcrypt
- python-jose
- email-validator
- python-dotenv
- slowapi

### 2.3 Configurar Variáveis de Ambiente

```bash
# Copiar template
cp .env.example .env

# Editar .env (abrir no editor)
# Linux/macOS
nano .env

# Windows
notepad .env
```

**Variáveis essenciais para MVP**:
```env
# JWT
JWT_SECRET_KEY=seu-secret-super-seguro-minimo-32-caracteres-aleatorio
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=sqlite:///./racket_hero.db

# Email (opcional para MVP, usar depois)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-app
```

### 2.4 Criar Banco de Dados

```bash
# Rodar Python interativo
python

# No prompt Python:
from database import Base, engine
Base.metadata.create_all(bind=engine)
exit()

# Você verá arquivo racket_hero.db criado
```

### 2.5 Testar Backend

```bash
# Rodar servidor
uvicorn main:app --reload --port 8000

# Em outro terminal, testar
curl http://localhost:8000/docs
```

**Sucesso!** Você deve ver a documentação Swagger em: http://localhost:8000/docs

---

## 3️⃣ Setup Frontend

### 3.1 Instalar Dependências

```bash
cd ../frontend

# Instalar packages
npm install

# Verificar instalação
npm list react react-router-dom axios
```

### 3.2 Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env.local
echo "REACT_APP_API_URL=http://localhost:8000" > .env.local

# Verificar (não deve conter valores sensíveis)
cat .env.local
```

### 3.3 Testar Frontend

```bash
# Rodar servidor dev
npm start

# Navegador deve abrir automaticamente em http://localhost:3000
```

---

## 4️⃣ Estrutura de Diretórios

Verificar que a estrutura está correta:

```bash
cd ..

# Visualizar estrutura
tree -L 2 -I 'node_modules|venv'

# Você deve ver:
# racket-hero/
# ├── backend/
# │   ├── venv/
# │   ├── main.py
# │   ├── database.py
# │   ├── requirements.txt
# │   ├── .env
# │   ├── .env.example
# │   ├── racket_hero.db
# │   ├── models/
# │   ├── routers/
# │   ├── schemas/
# │   ├── utils/
# │   └── tests/
# ├── frontend/
# │   ├── src/
# │   ├── package.json
# │   ├── .env.local
# │   └── public/
# ├── docs/
# ├── README.md
# ├── SETUP.md
# ├── .gitignore
# └── .git/
```

---

## 5️⃣ Rodar Projeto Completo

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate no Windows
uvicorn main:app --reload --port 8000
```

**Output esperado**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [12345]
```

### Terminal 2 - Frontend

```bash
cd frontend
npm start
```

**Output esperado**:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
```

### Terminal 3 - Testes (opcional)

```bash
cd backend
pytest
```

---

## 🧪 Testar Endpoints

### 1. Acessar Swagger (Recomendado)

```
http://localhost:8000/docs
```

Você pode testar todos os endpoints diretamente no Swagger UI.

### 2. Usar curl

```bash
# Teste health check
curl http://localhost:8000/

# Será adicionado após implementação de /auth/register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@example.com",
    "senha": "SenhaSegura123!",
    "nome": "João Teste",
    "tipo": "Jogador"
  }'
```

### 3. Usar Insomnia/Postman

1. Baixar [Insomnia](https://insomnia.rest/) ou [Postman](https://www.postman.com/)
2. Criar nova request
3. URL: `http://localhost:8000/auth/register`
4. Body (JSON):
```json
{
  "email": "teste@example.com",
  "senha": "SenhaSegura123!",
  "nome": "João Teste",
  "tipo": "Jogador"
}
```

---

## 🐛 Troubleshooting

### Backend não inicia

```bash
# Erro: "Address already in use"
# Solução: Mudar porta
uvicorn main:app --reload --port 8001

# Erro: "ModuleNotFoundError"
# Solução: Verificar venv ativado
which python  # macOS/Linux
where python  # Windows
```

### Frontend não inicia

```bash
# Erro: "port 3000 already in use"
# Solução: Kill processo ou mudar porta
npm start -- --port 3001

# Erro: "npm not found"
# Solução: Reinstalar Node.js
node --version
```

### Banco de dados corrompido

```bash
# Solução: Deletar e recriar
cd backend
rm racket_hero.db
python
from database import Base, engine
Base.metadata.create_all(bind=engine)
exit()
```

### JWT_SECRET_KEY inválido

```bash
# Solução: Gerar novo secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Copiar output para .env
JWT_SECRET_KEY=seu-output-aqui
```

---

## ✅ Checklist de Sucesso

- [ ] Git clone funcionou
- [ ] venv criado e ativado
- [ ] requirements.txt instalado
- [ ] .env configurado
- [ ] Banco de dados criado (racket_hero.db existe)
- [ ] Backend rodando em http://localhost:8000
- [ ] Swagger acessível em http://localhost:8000/docs
- [ ] Frontend rodando em http://localhost:3000
- [ ] Nenhum erro no console

---

## 🚀 Próximos Passos

Após setup bem-sucedido:

1. Ler [DESENVOLVIMENTO.md](./DEVELOPMENT.md)
2. Ler [ESPECIFICACAO.md](../ESPECIFICACAO.md)
3. Começar Feature 5: Autenticação
4. Ver [PLANO_DE_ACAO.md](../PLANO_DE_ACAO.md) para timeline

---

## 📞 Ajuda

Se encontrar problemas:

1. Verificar Python version: `python --version` (deve ser 3.9+)
2. Verificar Node version: `node --version` (deve ser 16+)
3. Verificar arquivo .env existe e tem valores corretos
4. Rodar setup novamente em ordem
5. Abrir issue em https://github.com/hirohaya/racket-hero/issues

---

**Sucesso no setup!** 🎉
