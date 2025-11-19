# 🧪 Contas de Teste - Racket Hero

## Contas Disponíveis

Na página de **Login** (`/login`), há um painel especial com botões para contas de teste. Clique em qualquer uma para preencher automaticamente o email e senha:

### 1. 🔐 Admin
- **Email**: `admin@test.com`
- **Senha**: `Senha123!`
- **Função**: Administrador do sistema

### 2. 🎯 Jogador
- **Email**: `jogador@test.com`
- **Senha**: `Senha123!`
- **Função**: Jogador de torneios

### 3. 📋 Organizador
- **Email**: `organizador@test.com`
- **Senha**: `Senha123!`
- **Função**: Organizador de eventos

## Como Usar

### No Frontend
1. Navegue para `http://localhost:3000/login`
2. Veja o painel "🧪 Contas de Teste" abaixo do formulário de login
3. Clique em qualquer conta
4. Os campos **Email** e **Senha** serão preenchidos automaticamente
5. Clique em **"Entrar"** para fazer login

### Via Script (Criar Contas no Banco)

Para criar essas contas no banco de dados:

```bash
cd C:\Users\hiros\OneDrive\Documents\projetos\racket-hero
python.exe tests/create_test_accounts.py
```

**Output esperado**:
```
======================================================================
CRIANDO CONTAS DE TESTE
======================================================================
[OK] Conta criada:
    Email: admin@test.com
    Senha: Senha123!
    Nome: Admin Teste
...
```

## Estrutura do Arquivo

### `frontend/src/pages/Login.js`
- Adiciona seção com botões de contas de teste
- Buttons chamam `onClick` que preenchem campos automaticamente
- Valores não são alterados se já houver conteúdo no formulário principal

### `frontend/src/pages/Auth.css`
- Estilos para `.test-accounts` (container)
- Estilos para `.test-account-btn` (botões individuais)
- Hover effects para melhor UX
- Estilos responsivos

### `tests/create_test_accounts.py`
- Script Python para popular banco com contas de teste
- Usa SQLAlchemy ORM
- Hash de senha com bcrypt (importado de `utils.security`)
- Verifica contas duplicadas antes de criar

## Fluxo de Teste

### Fluxo 1: Teste com Contas Seeded
```
1. Iniciar backend e frontend
2. Executar: python tests/create_test_accounts.py
3. Ir para http://localhost:3000/login
4. Clicar em "🔐 Admin"
5. Clicar em "Entrar"
6. ✅ Login bem-sucedido
```

### Fluxo 2: Teste com Registro
```
1. Ir para http://localhost:3000/register
2. Preencher formulário com dados únicos
3. Clicar em "Registrar"
4. ✅ Usuário criado e autenticado
5. Home page exibe nome do usuário
```

### Fluxo 3: Teste de Logout/Re-login
```
1. Fazer login com qualquer conta
2. Clicar em "Sair" no menu
3. Voltar para http://localhost:3000/login
4. Clicar em outra conta de teste
5. Clicar em "Entrar"
6. ✅ Login com nova conta bem-sucedido
```

## Variáveis de Ambiente

Se precisar alterar a senha das contas de teste, edite o array `TEST_ACCOUNTS` em `tests/create_test_accounts.py`:

```python
TEST_ACCOUNTS = [
    {
        "name": "Admin Teste",
        "email": "admin@test.com",
        "password": "SuaSenha123!",  # ← Altere aqui
        "role": "admin"
    },
    ...
]
```

E execute o script novamente.

## Notas

- ✅ Interface de contas de teste está completa
- ✅ Botões preenchem campos automaticamente
- ✅ Script de criação funciona (salva contas no banco)
- ⚠️ Login com contas seeded pode ter problemas de hash - preferir criar via registro na UI

## Próximos Passos

1. Validar hash de senha nas contas seeded
2. Adicionar função/role às contas de teste
3. Documentar diferentes permissões por tipo de usuário
4. Adicionar dados de teste para cada tipo de usuário (eventos, partidas, etc)

