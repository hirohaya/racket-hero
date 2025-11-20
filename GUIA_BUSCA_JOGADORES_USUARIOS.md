# 📖 GUIA DE USO - BUSCA DINÂMICA DE JOGADORES

## 🎯 Para Organizadores

### Como Adicionar Jogadores Usando a Busca

#### **Passo 1: Acesse o Evento**
1. Clique em "Eventos" no menu superior
2. Clique em "Ver Detalhes" no evento desejado
3. Você verá a seção "👥 Jogadores Inscritos"

#### **Passo 2: Abra o Modal de Adicionar**
4. Clique no botão **"➕ Adicionar Jogador"**
5. O modal será aberto com a caixa de busca

#### **Passo 3: Procure o Jogador**
6. Comece a digitar o **nome** do jogador no campo de busca
7. Exemplos:
   - Digite "João" → retorna todos com "João" no nome
   - Digite "silva" → retorna todos com "silva"
   - Digite "jo" → retorna resultados que começam com "jo"

#### **Passo 4: Selecione da Lista**
8. Veja os resultados aparecer dinamicamente
9. Cada resultado mostra:
   - 👤 Nome do jogador
   - 📧 Email
   - 🏷️ Tipo (Jogador/Organizador/Admin)

10. **Clique em "Selecionar →"** no resultado desejado

#### **Passo 5: Confirme**
11. O formulário será preenchido automaticamente com:
    - **Nome**: Do jogador selecionado
    - **Clube**: Deixado em branco (você pode preencher)
    - **Pontuação**: 1600 (padrão, você pode ajustar)

12. Clique **"Adicionar Jogador"**

✅ **Pronto!** O jogador foi adicionado ao evento!

---

## 🆕 Adicionar Novo Jogador Manualmente

### Quando Usar
- O jogador não aparece na busca
- Quer adicionar alguém que não tem cadastro

### Passos

1. Abra o modal de adicionar jogador (ver acima, passo 1-2)

2. **Opção A**: Procure e não encontre
   - Digite na busca
   - Veja "Nenhum jogador encontrado"
   - Clique **"➕ Adicionar Novo Jogador"**

3. **Opção B**: Direto para entrada manual
   - Após selecionar da lista (ou não), clique **"← Voltar para busca"**
   - Clique **"➕ Adicionar Novo Jogador"**

4. Preencha os campos:
   - **Nome do Jogador** *(obrigatório)*: Ex: "Maria Santos"
   - **Clube** *(opcional)*: Ex: "Clube do Tênis"
   - **Pontuação Inicial**: Ex: "1700" (padrão: 1600)

5. Clique **"Adicionar Jogador"**

✅ **Pronto!** Novo jogador adicionado!

---

## ⚙️ Funcionalidades Especiais

### 🔍 Busca Case-Insensitive
- "joão" = "João" = "JOÃO"
- Todos retornam o mesmo resultado

### 🚫 Sem Duplicatas
- Jogadores já adicionados **não aparecem** na busca
- Previne adicionar a mesma pessoa 2x

### ⚡ Busca Otimizada
- Espera **300 milissegundos** após você parar de digitar
- Reduz requisições ao servidor
- Mais rápido e eficiente

### 📋 Tipos de Usuário
Veja o tipo de cada pessoa:
- 🎯 **Jogador**: Cadastrado como jogador
- 📋 **Organizador**: Pode organizar eventos
- 🔐 **Admin**: Administrador do sistema

### ⬅️ Voltar para Busca
- Após preencher o formulário manual
- Clique **"← Voltar para busca"**
- Tudo é limpo e você pode buscar outro

---

## ❓ Perguntas Comuns

### P: Por que um jogador não aparece na busca?
**R:** Pode ser:
- ✅ Já foi adicionado a este evento
- ✅ Não tem cadastro no sistema
- ✅ Conta foi desativada

**Solução**: Use "Adicionar Novo Jogador" manual

### P: Posso adicionar o mesmo jogador 2 vezes?
**R:** Não! O sistema impede duplicatas.

### P: O que significa "1600" na pontuação?
**R:** É o rating ELO inicial do jogador. Quanto maior, mais forte.
- Iniciante: 1200-1400
- Intermediário: 1500-1700
- Avançado: 1800+

### P: Posso mudar a pontuação depois?
**R:** Sim! A pontuação é atualizada automaticamente conforme joga.

### P: E se digitar errado o nome?
**R:** Sem problemas! Volte e clique "← Voltar para busca" para refazer.

### P: Preciso digitar EXATO o nome?
**R:** Não! Funciona com partes:
- Digite "silva" → encontra "João Silva"
- Digite "mari" → encontra "Maria", "Mariano", etc

---

## 🎨 Interface Visual

### Caixa de Busca
```
┌─────────────────────────────────────────┐
│ 🔍 Buscar jogador por nome...           │
└─────────────────────────────────────────┘
```

### Resultado Found
```
📋 Organizador Teste
organizador@test.com
[Organizador]                    Selecionar →
```

### Resultado Not Found
```
Nenhum jogador encontrado com "xyz"

➕ Adicionar Novo Jogador
```

### Formulário Manual
```
Nome do Jogador *
┌──────────────────────────────────┐
│ Ex: João Silva                   │
└──────────────────────────────────┘

Clube
┌──────────────────────────────────┐
│ Ex: Clube do Tenis               │
└──────────────────────────────────┘

Pontuação Inicial
┌────────┐
│ 1600   │  Padrão: 1600
└────────┘
```

---

## 🚨 Mensagens de Erro

### ⚠️ "Erro ao buscar jogadores"
- Problema temporário de conexão
- Tente novamente

### ⚠️ "Você não tem permissão para adicionar jogadores"
- Você não é o organizador deste evento
- Peça ao organizador para adicionar

### ⚠️ "Nome do jogador é obrigatório"
- Esqueceu de preencher o nome
- Preencha e tente novamente

### ⚠️ "Esse jogador já foi adicionado"
- Este jogador já está no evento
- Busque por outro

---

## 💡 Dicas Práticas

### 1️⃣ Busque Sempre Primeiro
- Economiza tempo
- Evita duplicatas
- Garante dados consistentes

### 2️⃣ Use Partes do Nome
```
Ao invés de:    "João Batista de Oliveira"
Digite:         "joão" ou "batista"
```

### 3️⃣ Verifique o Email
- Certifique-se que é a pessoa certa
- Emails são únicos e identificam bem

### 4️⃣ Ajuste a Pontuação
- Se jogador é iniciante: 1200-1400
- Se é intermediário: 1500-1700
- Se é avançado: 1800+

### 5️⃣ Organize Depois
- Após adicionar jogadores
- Você pode criar grupos
- Organizar as partidas

---

## 🎯 Fluxo Completo

```
Evento "Campeonato de Tênis"
         │
         ├─ Clica "Adicionar Jogador"
         │   │
         │   ├─ [Procura] ──→ Encontra? ──→ [Seleciona] ──→ [Confirma]
         │   │                    │                             │
         │   │                    └─ Não encontra?             │
         │   │                              │                  │
         │   │                              ├─ [Manual] ─────→ [Confirma]
         │   │                              │
         │   │                              └─ [Voltar] ──→ [Busca Novamente]
         │   │
         │   └─ Jogador Adicionado ✅
         │
         └─ Repetir para mais jogadores
                    │
                    └─ Próximo: Criar Grupos/Partidas
```

---

## 📞 Suporte

Tendo problemas? Verifique:
1. ✅ Está logado como organizador?
2. ✅ Tem permissão para editar este evento?
3. ✅ A conexão à internet está ativa?
4. ✅ Navegador atualizado?

Se problema persistir:
- Recarregue a página (F5)
- Limpe cache do navegador
- Tente outro navegador
- Contate o administrador

---

## 📚 Mais Informações

Para detalhes técnicos, veja:
- `DYNAMIC_PLAYER_SEARCH_IMPLEMENTATION.md` - Documentação técnica completa
- `BUSCA_JOGADORES_RESUMO_VISUAL.md` - Resumo visual da arquitetura

---

**Última Atualização**: 2024-11-20
**Versão**: 1.0
