# Documentação - Racket Hero

Esta pasta contém toda a documentação do projeto Racket Hero. Os arquivos aqui são **referência local apenas** e não são versionados no Git para manter o repositório limpo.

## 📋 Índice de Documentação

### 🚀 Começar Rápido
- **COMECE_AQUI.md** - Guia inicial do projeto
- **COMECE_AQUI_AGORA.md** - Instruções rápidas de setup
- **DESENVOLVIMENTO_LOCAL.md** - Como rodar localmente

### 🎯 Deployment
- **RAILWAY.md** - Guias de deployment no Railway (em docs/railway/)
- **DEPLOY_RAILWAY_RAPIDO.md** - Deploy rápido no Railway
- **DEPLOY_AZURE_COMPLETO.md** - Deploy completo no Azure
- **DEPLOY_AZURE_VISUAL.md** - Guia visual Azure
- **AZURE_VS_RAILWAY.md** - Comparação de plataformas
- **CHECKLIST_PRODUCAO.md** - Checklist pré-produção

### 📚 Arquitetura & Design
- **ESPECIFICACAO.md** - Especificação do projeto
- **ARQUITETURA_MULTIPLOS_ORGANIZADORES.md** - Suporte multi-organizador
- **AUTENTICACAO_E_SEGURANCA.md** - Autenticação e segurança
- **PERMISSIONS.md** - Sistema de permissões
- **ROADMAP.md** - Roadmap do projeto

### 🔧 Implementação
- **GUIA_IMPLEMENTACAO.md** - Guia completo de implementação
- **IMPLEMENTATION_SUMMARY.md** - Resumo de implementação
- **MULTIPLOS_ORGANIZADORES.md** - Feature multi-organizador
- **STATUS_IMPLEMENTACAO.md** - Status das features

### 🧪 Testes & QA
- **TEST_ACCOUNTS.md** - Contas de teste disponíveis
- **CONTAS_TESTE_DISPONIVEIS.md** - Lista de contas para testing
- **QUICK_TEST_REFERENCE.md** - Referência rápida de testes
- **TEST_DATA_CREATED.md** - Dados de teste criados

### 📖 Referência
- **FAQ.md** - Perguntas frequentes
- **PROXIMOS_PASSOS.md** - Próximos passos de desenvolvimento
- **LOGGER.md** - Documentação de logging

### 📌 Fase 1 & Análises
- **FASE1_STATUS.md** - Status fase 1
- **RELATORIO_FASE1_FINAL.md** - Relatório final fase 1
- **ANALISE_ESPECIFICACAO_v2.md** - Análise de especificação
- **PLANO_DE_ACAO.md** - Plano de ação

### 🔄 Deployment Railways (em docs/railway/)
```
docs/railway/
├── README.md                      - Por que os arquivos Railway são ignorados
├── PROXIMOS_PASSOS.md            - Guia passo-a-passo
├── LEIA_ISTO.md                  - Visão geral 2 min
├── RESUMO_VISUAL.md              - Resumo visual 3 min
├── RESUMO_EXECUTIVO.md           - Resumo técnico 10 min
├── COMPLETO.txt                  - Status completo
├── STATUS_FINAL.txt              - Checklist final
├── START_HERE.md                 - Mapa de navegação
├── SETUP.md                      - Setup técnico
├── DEPLOY_COMPLETO.md            - Guia completo
├── INDICE.md                     - Índice de arquivos
└── PRONTO.txt                    - Status pronto
```

## 🚫 Por que os docs não estão no Git?

A pasta `docs/` é **ignorada pelo Git** (.gitignore) para:
- ✅ Manter o repositório limpo
- ✅ Evitar histórico poluído com documentação
- ✅ Focar versionamento em código e testes

**Arquivos essenciais no Git:**
- `README.md` (raiz) - Documentação principal do projeto
- `RAILWAY.md` (raiz) - Índice de deployment
- Código em `backend/` e `frontend/`
- Testes em `backend/tests/` e `frontend/src/__tests__/`
- Configuração em `.github/`, `railway.toml`, `Procfile`

## 📂 Estrutura

```
racket-hero/
├── README.md              ← Documentação principal
├── RAILWAY.md             ← Índice de deployment
├── backend/
├── frontend/
├── docs/
│   ├── README.md          ← Este arquivo
│   ├── railway/           ← Guias específicas do Railway (gitignored)
│   └── (outros .md)       ← Documentação local
└── .github/
```

## 💡 Como Usar

1. **Começar?** Abra `COMECE_AQUI.md`
2. **Deploy?** Veja `RAILWAY.md` na raiz ou `docs/railway/PROXIMOS_PASSOS.md`
3. **Desenvolver?** Consulte `DESENVOLVIMENTO_LOCAL.md`
4. **Dúvidas?** Verifique `FAQ.md`

---

**Nota:** Esta documentação é referência local. Para manter o código limpo, use esta pasta como referência durante o desenvolvimento, mas não adicione novos arquivos .md para versionamento no Git.
