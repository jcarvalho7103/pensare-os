# Memory System — Pensare OS

> Sistema de memória persistente file-based, inspirado em Letta/MemGPT, com 4 camadas e organização semântica.

---

## Por que memória importa

Um agente sem memória persistente:
- Começa do zero a cada sessão
- Repete os mesmos erros
- Não acumula contexto sobre clientes, pipeline, mercado
- Não pode evoluir

Um sistema com memória bem estruturada:
- Lembra decisões passadas e seu racional
- Reconhece padrões
- Evita repetir erros
- Personaliza decisões com base no histórico

---

## As 4 Camadas de Memória

```
┌─────────────────────────────────────────────────────────────┐
│  CORE MEMORY                          Sempre carregada      │
│  SOUL.md, IDENTITY.md                 Imutável por sessão   │
├─────────────────────────────────────────────────────────────┤
│  RECALL MEMORY                        Por sessão            │
│  MEMORY.md                            Atualizada continuamente│
├─────────────────────────────────────────────────────────────┤
│  ARCHIVAL MEMORY                      Sob demanda           │
│  memory/shared/ + memory/per-agent/   Buscada quando precisa│
├─────────────────────────────────────────────────────────────┤
│  EVENT LOG                            Append-only           │
│  logs/events.ndjson                   Audit trail completo  │
└─────────────────────────────────────────────────────────────┘
```

### 1. Core Memory (sempre carregada)

**Arquivos**: `SOUL.md`, `IDENTITY.md`

**Propósito**: identidade fundamental que não muda dentro de uma sessão.

**Quando atualizar**: apenas em evolução estratégica deliberada (não a cada sessão).

**Tamanho**: pequeno (200–400 linhas total) — cabe sempre no contexto.

### 2. Recall Memory (estado da sessão)

**Arquivo**: `MEMORY.md`

**Propósito**: estado atual — onde estou, no que estou trabalhando, próximos passos.

**Seções padrão**:
- Last Session (resumo da anterior)
- Current Focus
- Pipeline Snapshot
- Open Questions
- Decisions
- Next Steps
- Monthly Metrics

**Quando atualizar**: ao final de cada sessão substantiva (via `/pensare` no fechamento).

### 3. Archival Memory (histórico estruturado)

**Diretório**: `memory/shared/` (compartilhada) + `memory/per-agent/` (por agente)

**Propósito**: histórico organizado por dimensão semântica.

**Organização** (inspirada no Pensare OS Lovable):

```
memory/shared/
├── context.md                    ← contexto geral de negócio
├── decisions.md                  ← decisões estratégicas registradas
├── clients.md                    ← clientes ativos
│
├── operacional/                  ← O QUE ACONTECEU
│   ├── leads.md
│   ├── conversas.md
│   └── vendas.md
│
├── estrategica/                  ← O QUE FUNCIONA E POR QUÊ
│   ├── icp-real.md               ← quem realmente converte
│   ├── winning-offers.md         ← o que vende
│   └── posicionamento.md
│
├── otimizacao/                   ← COMO MELHORAR
│   ├── best-creatives.md
│   ├── campaign-patterns.md
│   └── funnel-insights.md
│
└── retencao/                     ← O QUE FAZ FICAR
    ├── churn-insights.md
    └── evolucao-clientes.md
```

**Quando atualizar**: quando um padrão se confirma (≥3 ocorrências) ou quando uma decisão importante é tomada.

### 4. Event Log (cronológico imutável)

**Arquivo**: `logs/events.ndjson`

**Formato**: NDJSON (1 linha = 1 evento)

```jsonl
{"ts":"2026-05-13T08:00:00Z","agent":"/pensare","type":"session_start","summary":"Boot sequence completo","payload":{}}
{"ts":"2026-05-13T08:05:00Z","agent":"/pensare-inteligencia","type":"daily_brief","summary":"Brief matinal gerado","payload":{"events_24h":12}}
{"ts":"2026-05-13T14:30:00Z","agent":"/pensare-sdr","type":"lead_captured","summary":"Lead: empresa X","payload":{"score":82}}
```

**Propósito**: audit trail completo, fonte de verdade imutável.

**Quando escrever**: a cada ação relevante (via `pensare-log`).

---

## Reflexão por Agente (Reflexion Pattern)

Baseado em Shinn et al. 2023. Cada agente mantém `memory/per-agent/{nome}/reflections.md`:

```markdown
# Reflexões — /pensare-comercial

## 2026-05-10 — Fechamento bem-sucedido do 1º MVP

**Contexto**: Cliente Y, ticket R$ 25k, ciclo de 18 dias.

**O que funcionou**:
- Diagnóstico completo antes de qualquer proposta
- Apresentação visual de "antes/depois" do AI Systemizer
- Garantia de 30 dias bem destacada

**O que não funcionou**:
- Apressei pricing (cliente perguntou antes de eu mostrar valor)

**Aplicação futura**:
Sempre fazer 3 perguntas SPIN antes de qualquer slide com preço.

**Tags**: #diagnostico #pricing #1o-mvp #closing
```

### Recuperação

```bash
# Top 3 reflexões do CEO
pensare-reflect --agent ceo --top 3

# Reflexões taggeadas com "pricing"
pensare-reflect --agent comercial --tag pricing

# Combinação
pensare-reflect --agent comercial --tag pricing --top 5
```

### Por que reflexão importa

Sem reflexão, o agente erra → corrige no momento → esquece → erra de novo.

Com reflexão, o agente erra → corrige → registra → no próximo erro similar, recupera a lição → corrige antes.

---

## Regras de Atualização

### Quando REGISTRAR

| Situação | Onde registrar |
|----------|---------------|
| Decisão estratégica tomada | `memory/shared/decisions.md` |
| Cliente novo ativo | `memory/shared/clients.md` |
| Padrão confirmado (3+ ocorrências) | `memory/shared/{dimensao}/{tema}.md` |
| Lição de erro/acerto significativo | `memory/per-agent/{nome}/reflections.md` |
| Ação executada por agente | `logs/events.ndjson` (sempre) |
| Estado da sessão mudou | `MEMORY.md` |

### Quando NÃO registrar

- ❌ Ruído (variação dentro do esperado)
- ❌ Evento isolado sem relevância
- ❌ Informação que já está em outro arquivo (DRY)
- ❌ Detalhe efêmero (vai estar obsoleto em 7 dias)

### Pergunta-guia

> "O que o sistema aprendeu com isso?"

Se a resposta for "nada novo, é só registro mecânico", **não atualize a Archival**. Apenas evento em log basta.

---

## Como cada agente usa a memória

### Boot de qualquer agente

```
1. Carrega Core (SOUL.md + IDENTITY.md)
2. Carrega Recall (MEMORY.md)
3. tail -10 do Event Log
4. Carrega Archival relevante para a tarefa (sob demanda)
```

### Durante a operação

```
1. Lê seu próprio reflections.md (top 3 reflexões relevantes)
2. Lê memory/per-agent/{próprio-nome}/ (estado pessoal)
3. Lê memory/shared/{dimensao}/ se a tarefa demanda
```

### Ao terminar a ação

```
1. Escreve evento em logs/events.ndjson (sempre)
2. Atualiza memory/per-agent/{próprio-nome}/{estado}.md (se houve mudança)
3. Atualiza reflections.md (se aprendeu algo significativo)
4. Atualiza memory/shared/ (se padrão confirmou — ≥3 ocorrências)
```

---

## Comandos auxiliares

### `pensare-log`

Registra evento no log NDJSON.

```bash
pensare-log <type> "<summary>" '<payload-json>'

# Exemplos:
pensare-log lead_captured "Novo lead: empresa X" '{"score":82}'
pensare-log decision "Aprovou escala AI Systemizer" '{"impact":"high"}'
pensare-log session_close "Encerrou sessão de planning"
```

### `pensare-reflect`

Recupera reflexões de um agente.

```bash
pensare-reflect --agent <nome> [--top N] [--tag X]

# Exemplos:
pensare-reflect --agent comercial --top 5
pensare-reflect --agent ceo --tag pricing
```

### `pensare-status`

Status agregado do sistema (saúde da memória).

```bash
pensare-status
# Retorna: { "status": "ok|degraded|blocked|error", ... }
```

### `pensare-cost`

Análise de custo por tier.

```bash
pensare-cost                # mostra breakdown
pensare-cost --alert        # dispara se > target × 1.5
```

---

## Padrões anti-correrupção da memória

### 1. Sempre versione com Git
Toda mudança em `memory/shared/` deve ser commitada:
```bash
git add memory/shared/
git commit -m "memory: add winning offer pattern from cliente Y"
```

`memory/per-agent/*/state.md` é **gitignored** (estado efêmero); mas `reflections.md` é versionado.

### 2. Nunca delete — corrija ou arquive
Se uma decisão foi revertida, **adicione** a reversão. Não apague a original.

```markdown
## 2026-05-10 — Decisão: Lançar SaaS R$ 5k

Aprovado pelo Conselho.

### 2026-05-15 — REVISADO

Decisão pausada. Risco de canibalização não foi suficientemente mitigado.
Re-avaliar em 30 dias com dados de pipeline do AI Systemizer.
```

### 3. Frontmatter para metadata
Arquivos longos em `memory/shared/` podem ter frontmatter:

```markdown
---
last_updated: 2026-05-13
confidence: high
data_points: 47
---

# Winning Offers — AI Systemizer
[conteúdo]
```

### 4. Cross-referencing com [[wikilinks]]
Quando uma decisão em `decisions.md` se baseia em padrão em `winning-offers.md`:

```markdown
## Decisão: aumentar preço do AI Systemizer em 20%

Baseado em [[winning-offers]] — 4 últimos clientes pagaram acima do preço atual sem objeção.
```

Facilita navegação manual e busca posterior.

---

## Limites e quando evoluir

### Limites atuais

- **Busca é por path/grep** — não há embedding/semântica
- **Tamanho prático**: ~50MB de memória (~50 mil eventos NDJSON)
- **Sem compressão** — quando ficar grande, exigirá rotação de log

### Quando evoluir

Se você notar:
- Eventos > 100k → considerar particionar `logs/events.ndjson` por mês
- Memória > 100MB → comprimir arquivos antigos ou migrar para banco
- Busca semântica necessária → adicionar `faiss` + embeddings local

Por enquanto, **arquivos são suficientes** e a auditabilidade via Git compensa qualquer ineficiência.

---

## Exemplo concreto — Lead → Cliente

Acompanhe o flow de memória em um caso real:

### T0 — Lead chega
```
pensare-log lead_captured "..." '{"score":82,"id":"L001"}'
```
→ `logs/events.ndjson` recebe linha

### T1 — SDR qualifica
```
/pensare-sdr qualifique L001
```
→ SDR aplica skill `lead-qualification`
→ Escreve em `memory/per-agent/pensare-comercial/pipeline.md`:
```markdown
## Leads ativos
- L001 (empresa X) · SQL 82/100 · próximo: diagnóstico com Closer · 2026-05-13
```
→ Log: `pensare-log sdr_qualified "L001 SQL" '{"score":82}'`

### T2 — Closer fecha
```
/pensare-closer prepare diagnóstico para L001
```
→ Closer lê:
- `memory/per-agent/pensare-comercial/pipeline.md` (L001 está lá)
- `memory/shared/estrategica/winning-offers.md` (o que tem funcionado)
- `memory/per-agent/pensare-closer/reflections.md` (lições passadas)

### T3 — Venda fechada
→ Log: `pensare-log sale_closed "L001 fechado R$ 25k"`
→ Atualiza `memory/shared/clients.md`:
```markdown
## Cliente: empresa X
- Início: 2026-05-15
- Ticket: R$ 25k
- Fase: Onboarding
- Health score: — (ainda não calculado)
```
→ Closer atualiza `memory/per-agent/pensare-closer/reflections.md` (o que funcionou)

### T4 — Pattern emerging
Após 3 vendas no mesmo perfil, `/pensare-inteligencia` atualiza:
```markdown
# memory/shared/estrategica/icp-real.md

## Padrão confirmado (mai/2026)
Agências B2B de 5-10 pessoas com founder operacional fecham em 18-25 dias
com diagnóstico técnico de 60min antes da proposta.
```

Esse padrão agora informa decisões futuras.

---

## Visualização no Dashboard

O módulo **Memory** (`/memory`) do dashboard mostra:
- File tree de toda memória (shared + per-agent + raiz)
- Split editor (visualização + edição)
- Path-traversal prevention (você não pode escrever fora de `memory/`)

Acesse: http://localhost:8360/memory

---

*Lembre-se: memória boa é a que o sistema lê e age. Memória que ninguém recupera é só arquivo morto.*
