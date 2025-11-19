# Contas de Teste Disponíveis

## Resumo
- **Total de usuários**: 13
- **Admins**: 1
- **Organizadores**: 2
- **Jogadores**: 10

---

## Todas as Contas (Senha: `Senha123!`)

### 🔐 ADMINISTRADOR
| Email | Nome | Tipo |
|-------|------|------|
| admin@test.com | Admin Teste | admin |

### 📋 ORGANIZADORES
| Email | Nome | Tipo |
|-------|------|------|
| organizador@test.com | Organizador Teste | organizador |
| org2@test.com | Organizador 2 | organizador |

### 🎯 JOGADORES
| Email | Nome | Tipo |
|-------|------|------|
| jogador@test.com | Jogador Teste | usuario |
| joao@test.com | Joao Silva | usuario |
| maria@test.com | Maria Santos | usuario |
| pedro@test.com | Pedro Oliveira | usuario |
| ana@test.com | Ana Costa | usuario |
| carlos@test.com | Carlos Mendes | usuario |
| patricia@test.com | Patricia Lima | usuario |
| roberto@test.com | Roberto Alves | usuario |
| fernanda@test.com | Fernanda Souza | usuario |
| lucas@test.com | Lucas Martins | usuario |

---

## Como Usar

### Na Página de Login
1. Clique em um dos 3 botões de teste (Admin, Jogador ou Organizador)
2. Os campos serão preenchidos automaticamente
3. Clique em "Entrar"

### No Frontend
Todos os usuários têm senha: `Senha123!`

### Para Testes Manuais com cURL
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","senha":"Senha123!"}'
```

---

## Notas Importantes

- **Senha padrão**: Todos os usuários usam `Senha123!`
- **Tipos de usuário**: 
  - `admin`: Acesso total
  - `organizador`: Pode criar e gerenciar eventos
  - `usuario`: Jogador padrão (pode participar de eventos)
- **Dados persistem**: Todas as contas foram criadas no banco de dados SQLite

---

## Próximos Passos

Você pode usar essas contas para:
- Testar o sistema completo
- Criar eventos e gerenciar jogadores
- Testar diferentes níveis de acesso
- Simular torneiros com múltiplos jogadores
