# Por que os eventos criados são perdidos em cada deploy?

## Problema

Toda vez que você faz um novo deploy no Railway, os dados criados (eventos, partidas, etc.) são **perdidos**. Isso acontece porque:

1. ❌ O arquivo SQLite (`racket_hero.db`) é **deletado** quando o container é recriado
2. ❌ O script `seed_dev.py` **executava toda vez** que a app iniciava, resetando os dados
3. ❌ Não havia **persistência de volume** configurada no Railway

## Soluções Implementadas

### ✅ Solução 1: Flag de Seed (já implementada)

O script `seed_dev.py` agora verifica se já foi executado:
- Cria arquivo `.seed_initialized` após primeira execução
- Não executa seed novamente no **mesmo container**
- **Limitação:** Ainda perde dados se o container reiniciar (deploy novo)

### ✅ Solução 2: Persistência de Volume (RECOMENDADO)

Para **Railway**, configure um **Volume Persistente**:

**Via Railway Dashboard:**
1. Vá para seu projeto → Variables
2. Adicione o volume: `/app/backend` → `/data/racket-hero`
3. Redeploy

**Via `railway.toml`:**
```toml
[build]
  builder = "dockerfile"

[deploy]
  startCommand = "bash start.sh"
  
[[services.volumes]]
  path = "/app/backend"
  mount = "/data/racket-hero"
```

**Via Docker Compose (local):**
```yaml
services:
  backend:
    volumes:
      - ./backend/data:/app/backend  # Persistir dados
```

### ✅ Solução 3: Usar PostgreSQL (Melhor para Produção)

Ao invés de SQLite, use um banco de dados gerenciado:

```bash
# Criar instância PostgreSQL no Railway
railway add postgresql

# Configurar DATABASE_URL
DATABASE_URL=postgresql://user:pass@host:5432/racket_hero

# Deploy
railway up
```

## Como Testar

### Teste Local:
```bash
# Fazer seed uma vez
python backend/seed_dev.py

# Criar um evento manualmente
# Reiniciar o servidor
python backend/main.py

# ✅ Evento ainda está lá
```

### Teste no Railway:
1. Fazer deploy (seed é executado UMA VEZ)
2. Criar um evento no dashboard
3. Fazer deploy novamente
4. ❌ Evento foi perdido (esperado sem volume persistente)

## Recomendação

**Para desenvolvimento imediato:**
- Implemente o Volume Persistente (Solução 2)

**Para produção:**
- Use PostgreSQL ou outro banco gerenciado (Solução 3)
- Configure backups automáticos
- Monitore a saúde da aplicação

## Próximos Passos

- [ ] Configurar volume persistente no Railway
- [ ] Testar persistência entre deploys
- [ ] Documentar processo de reset manual (quando necessário)
- [ ] Considerar migração para PostgreSQL
