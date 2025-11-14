# README.md - Racket Hero

## 🏓 Racket Hero - Gerenciador de Eventos de Tênis de Mesa

Plataforma de gerenciamento de eventos de tênis de mesa com suporte a diferentes formatos de torneio, ranking por ELO e controle granular de permissões.

### 📋 Sobre o Projeto

**Racket Hero** é uma aplicação web para:
- ✅ Criar e gerenciar grupos de jogadores
- ✅ Organizar eventos de tênis de mesa
- ✅ Registrar partidas e resultados
- ✅ Calcular rankings usando sistema de ELO
- ✅ Controlar permissões (Jogador, Organizador, Admin)

### 🎯 Status

**MVP v1.0** - Em desenvolvimento  
**Duração estimada**: 6-8 semanas  
**Tech Stack**: FastAPI + React + SQLite

### 🚀 Quick Start

#### Forma Mais Rápida (Windows PowerShell)

```powershell
cd C:\Users\hiros\OneDrive\Documents\projetos\racket-hero
.\scripts\start-all-parallel.ps1
```

Ambos rodando:
- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:3000
- **Docs**: http://127.0.0.1:8000/docs

Veja `COMO_INICIAR.md` para mais opções de inicialização.

---

#### Backend

```bash
# Clone o repositório
git clone https://github.com/hirohaya/racket-hero.git
cd racket-hero/backend

# Criar virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com seus valores

# Rodar servidor
uvicorn main:app --reload --port 8000
```

**Servidor estará em**: http://localhost:8000  
**Documentação API (Swagger)**: http://localhost:8000/docs

#### Frontend

```bash
cd ../frontend

# Instalar dependências
npm install

# Rodar servidor dev
npm start
```

**Frontend estará em**: http://localhost:3000

### 📚 Documentação

- **[ESPECIFICACAO.md](../ESPECIFICACAO.md)** - Especificação completa do projeto (5 Features)
- **[SETUP.md](./SETUP.md)** - Instruções detalhadas de setup
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Guia para desenvolvimento
- **[PLANO_DE_ACAO.md](../PLANO_DE_ACAO.md)** - Timeline e roadmap

### 🔧 Tecnologias

**Backend**:
- FastAPI 0.104+
- SQLAlchemy + SQLite
- JWT (python-jose)
- bcrypt (password hashing)
- Pydantic (validation)

**Frontend**:
- React 18+
- React Router v6
- Axios (HTTP client)

### 📝 Features (MVP v1.0)

| Feature | Status | Semana |
|---------|--------|--------|
| Feature 1: Grupos & Eventos | 📋 Planejado | 3-4 |
| Feature 2: Partidas & Jogos | 📋 Planejado | 3-4 |
| Feature 3: Usuários & Papéis | 📋 Planejado | 5-6 |
| Feature 4: Ranking (ELO) | 📋 Planejado | 5-6 |
| Feature 5: Autenticação | 🚀 Começando | 1-2 |

### 🧪 Testes

```bash
# Backend
cd backend
pytest

# Frontend
cd ../frontend
npm test
```

### 🎓 Estrutura de Pastas

```
racket-hero/
├── backend/
│   ├── venv/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .gitignore
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── utils/
│   └── tests/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── .env.local (não commitar)
└── docs/
    ├── ESPECIFICACAO.md
    ├── SETUP.md
    ├── DEVELOPMENT.md
    └── PLANO_DE_ACAO.md
```

### 🤝 Contribuindo

1. Crie uma feature branch: `git checkout -b feature/sua-feature`
2. Commit suas mudanças: `git commit -m "feat: descrição"`
3. Push para branch: `git push origin feature/sua-feature`
4. Abra um Pull Request

### 📧 Contato

Para dúvidas ou sugestões, abra uma issue no [GitHub](https://github.com/hirohaya/racket-hero/issues).

### 📄 Licença

Este projeto está sob a licença MIT.

---

**Pronto para começar?** Veja [SETUP.md](./SETUP.md) para instruções detalhadas.
