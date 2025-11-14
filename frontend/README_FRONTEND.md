# Racket Hero - Frontend

Frontend React para o sistema de gerenciamento de torneios de tênis de mesa.

## Instalação

```bash
npm install
```

## Configuração

Crie um arquivo `.env` na raiz do frontend:

```
REACT_APP_API_URL=http://localhost:8000/api
```

## Executar em Desenvolvimento

```bash
npm start
```

A aplicação abrirá em [http://localhost:3000](http://localhost:3000)

## Estrutura do Projeto

```
src/
├── components/          # Componentes reutilizáveis
│   ├── Header.js       # Cabeçalho com navegação
│   ├── Header.css
│   └── ProtectedRoute.js # Rota protegida por autenticação
├── context/
│   └── AuthContext.js  # Context de autenticação
├── hooks/
│   └── useAuth.js      # Hook customizado para autenticação
├── pages/              # Páginas/telas
│   ├── Home.js        # Página inicial
│   ├── Home.css
│   ├── Login.js       # Página de login
│   ├── Register.js    # Página de registro
│   └── Auth.css       # Estilos compartilhados
├── services/
│   ├── api.js         # Configuração do axios com interceptors
│   └── authService.js # Serviço de autenticação
├── App.js             # Componente principal
└── index.js           # Entrada da aplicação
```

## Funcionalidades Implementadas

✅ **Autenticação**
- Registro de novos usuários
- Login com email e senha
- Recuperação de senha
- Gerenciamento de tokens (access e refresh)
- Logout

✅ **Componentes**
- Header com navegação
- Rotas protegidas
- Context de autenticação
- Interceptor de requisições

✅ **UI/UX**
- Design responsivo
- Feedback visual (loading, errors)
- Validação de formulários
- Armazenamento de tokens no localStorage

## Proximas Funcionalidades

- [ ] Página de Eventos
- [ ] Página de Partidas
- [ ] Sistema de Rankings
- [ ] Página de Grupos
- [ ] Editar perfil de usuário

## Desenvolvimento

### Adicionar Nova Página

1. Criar componente em `src/pages/NomePagina.js`
2. Importar em `App.js`
3. Adicionar rota em `<Routes>`
4. Se protegida, envolver com `<ProtectedRoute>`

### Usar Autenticação

```javascript
import { useAuth } from '../hooks/useAuth';

function MinhaComponente() {
  const { user, login, logout, isAuthenticated } = useAuth();
  
  // Usar os dados de autenticação...
}
```

### Fazer Requisição à API

```javascript
import api from '../services/api';

// GET
const data = await api.get('/endpoint');

// POST
const response = await api.post('/endpoint', { data });
```

O token é adicionado automaticamente nos headers!
