# Arquitetura do Pensare OS

> Documento de arquitetura detalhada do Pensare OS. Versão 1.0 — Maio 2026.

---

## Sumário

1. [Visão Geral](#visão-geral)
2. [As 5 Camadas](#as-5-camadas)
3. [Camada 1 — Identidade (Core Memory)](#camada-1--identidade-core-memory)
4. [Camada 2 — Agentes](#camada-2--agentes)
5. [Camada 3 — Memória](#camada-3--memória)
6. [Camada 4 — Heartbeat](#camada-4--heartbeat)
7. [Camada 5 — Dashboard](#camada-5--dashboard)
8. [Fluxo de Dados End-to-End](#fluxo-de-dados-end-to-end)
9. [Padrões Arquiteturais Aplicados](#padrões-arquiteturais-aplicados)
10. [Decisões de Design](#decisões-de-design)
11. [Limites e Trade-offs](#limites-e-trade-offs)

---

## Visão Geral

O Pensare OS é um sistema de **multi-agentes hierárquicos** que rodam sobre **Claude Code CLI** como runtime de execução, com **memória persistente em arquivos** versionados no Git e **rotinas autônomas** orquestradas por um daemon Python + Mac launchd.

### Princípios arquiteturais

| Princípio | Implementação |
|-----------|---------------|
| **Files-first** | Toda configuração e memória vive em arquivos `.md`, `.yaml`, `.json` — versionáveis no Git |
| **Hierarquia explícita** | 4 tiers (Coordinator, C-Suite, Heads, Execution) com regras de escalação |
| **Memória persistente** | Estado sobrevive entre sessões via Recall + Archival + Event Log |
| **Autonomia controlada** | Heartbeat antecipa; mas decisões críticas escalam para o humano |
| **Custo monitorado** | Disciplina 10/20/70 com alertas automáticos |
| **Reflexão explícita** | Cada agente registra aprendizado em `reflections.md` |
| **Sem build step** | Frontend usa CDN; backend é Python stdlib + FastAPI |

---

## As 5 Camadas

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CAMADA 1 — IDENTIDADE (Core Memory)                                │
│  ─────────────────────────────────────                              │
│  • SOUL.md       missão · 8 princípios · 13 non-negotiables         │
│  • IDENTITY.md   Pensare Digital · AI Systemizer · SaaS · ICP       │
│  • CLAUDE.md     boot sequence (auto-loaded pelo Claude Code)       │
│                                                                     │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │  carregada antes de qualquer ação
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CAMADA 2 — AGENTES (17 SKILL.md em .claude/skills/)                │
│  ─────────────────────────────────────────────────                  │
│  Tier 0   /pensare                       (Coordinator)              │
│  Tier 1   /pensare-conselho · /pensare-ceo   (C-Suite)              │
│  Tier 2   9 Heads (growth, comercial, ...)                          │
│  Tier 3   6 Executores (sdr, closer, ...)                           │
│                                                                     │
│  + 10 Skills reutilizáveis (lead-qualification, offer-creation, ...)│
│  + Disciplina de custo 10/20/70                                     │
│                                                                     │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │  invocam, delegam, escalam
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CAMADA 3 — MEMÓRIA (Letta-inspired, file-based)                    │
│  ──────────────────────────────────────────────                     │
│  • Core      SOUL.md + IDENTITY.md         (sempre carregado)       │
│  • Recall    MEMORY.md                     (por sessão)             │
│  • Archival  memory/shared/, memory/per-agent/   (sob demanda)      │
│  • Event Log logs/events.ndjson            (append-only)            │
│                                                                     │
│  4 camadas semânticas: Operacional · Estratégica · Otimização       │
│                       · Retenção                                    │
│                                                                     │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │  alimentado por ações dos agentes
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CAMADA 4 — HEARTBEAT (Python daemon + launchd)                     │
│  ─────────────────────────────────────────────                      │
│  • daemon.py     loop verifica HEARTBEAT.md a cada 60s              │
│  • install.sh    LaunchAgent Mac (com.pensare.heartbeat.plist)      │
│  • state.json    última execução por rotina                         │
│                                                                     │
│  Rotinas:                                                           │
│    Daily   08h/09h/16h/18h                                          │
│    Weekly  seg 08:30 · qua 10:00 · sex 17:00                        │
│    Monthly dia 1 · dia 15                                           │
│                                                                     │
│  + 9 gatilhos por evento (lead_captured, cpl_increased, ...)        │
│  + 3 níveis de alerta (crítico/moderado/leve)                       │
│                                                                     │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │  expõe estado via API
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  CAMADA 5 — DASHBOARD (FastAPI + SPA HTML/Tailwind/Alpine)          │
│  ─────────────────────────────────────────────────────              │
│  Backend:   dashboard/server.py    12 endpoints REST                │
│  Frontend:  dashboard/index.html   11 módulos SPA                   │
│                                                                     │
│  Módulos: Dashboard · Core · Orchestrator · Agents · Skills         │
│           · Memory · Heartbeats · Tools · Soul · Tasks · Chat       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Camada 1 — Identidade (Core Memory)

### Propósito

Definir **quem é** o sistema, **como decide**, **o que nunca faz** e **como fala**. Esta camada é carregada antes de qualquer ação e nunca é negociada por conveniência operacional.

### Arquivos

#### `SOUL.md` — A alma do sistema

Contém:
- **Missão**: Transformar conhecimento, serviço e expertise em Capital Digital
- **Visão**: Sistema operacional de referência para empresas de serviço com IA
- **8 Princípios**:
  1. Sistema antes de volume
  2. Fit antes de venda
  3. Valor antes de preço
  4. Clareza antes de complexidade
  5. Dados antes de opinião
  6. Qualidade antes de escala
  7. Capital Digital antes de marketing isolado
  8. Evolução contínua
- **13 Não-Negociáveis** (o que a Pensare NUNCA faz)
- **7 Perguntas da Decision Philosophy** (aplicadas pelo Conselho)
- **Brand Voice** (estratégica, direta, segura, clara, consultiva)
- **Tom**: "A Pensare não grita. A Pensare diagnostica."

#### `IDENTITY.md` — Identidade da empresa

Contém:
- Nomenclatura: Pensare Digital (empresa) · Pensare OS (sistema) · AI Systemizer (produto consultivo)
- Categoria criada: **Capital Digital**
- ICP detalhado (2 produtos: consultoria + SaaS em validação)
- Posicionamento competitivo
- Estado atual da operação (mai/2026)

#### `CLAUDE.md` — Boot sequence

Lido **automaticamente** pelo Claude Code ao iniciar qualquer sessão no diretório. Define 5 passos obrigatórios:

1. Carregar SOUL.md + IDENTITY.md
2. Reconstruir contexto da última sessão (`tail -10` em `logs/events.ndjson`)
3. Carregar estado da memória (`MEMORY.md`)
4. Carregar contexto de negócio se necessário (`_contexto/empresa.md`, `mercado.md`)
5. Saudação e status

### Por que esta camada existe

Sem identidade explícita, o sistema **deriva**. Cada sessão começaria do zero, cada agente teria viés do prompt do momento, decisões seriam inconsistentes. Com Core Memory persistente, o sistema mantém coerência ao longo do tempo — equivalente a ter "memória de longo prazo da identidade" como um humano tem.

---

## Camada 2 — Agentes

### Hierarquia

```
                    /pensare                        (Tier 0 — Coordinator)
                       │
              ┌────────┴────────┐
              │                 │
        /pensare-conselho  /pensare-ceo            (Tier 1 — C-Suite)
                                 │
        ┌────────────────┬───────┴────────┬────────────────┐
        │                │                │                │
   /pensare-growth  /pensare-comercial  /pensare-operacoes ...   (Tier 2 — Heads)
        │                │
   ┌────┴────┐      ┌────┴────┐
   │  copy   │      │   sdr   │
   │ trafego │      │ closer  │                              (Tier 3 — Execution)
   │criativos│      │         │
   └─────────┘      └─────────┘
```

### Disciplina de custo (10/20/70)

| Tier | % do orçamento de tokens | Justificativa |
|------|--------------------------|---------------|
| 0–1  | 10% | Coordinator + C-Suite decidem em poucas palavras |
| 2    | 20% | Heads analisam com profundidade controlada |
| 3    | 70% | Execution é onde o trabalho real acontece |

**Por que importa**: sem disciplina, o C-Suite "puxa para si" tarefas que deveriam ser delegadas, inflando custo sem agregar valor. O monitoramento é via `pensare-cost --alert`.

### Estrutura interna de cada agente

Cada agente vive em `.claude/skills/pensare-{role}/SKILL.md` com YAML frontmatter:

```yaml
---
name: pensare-ceo
description: CEO Agent — decisões executivas, priorização entre áreas
tier: director
reports_to: /pensare-conselho
supervises: [/pensare-growth, /pensare-comercial, /pensare-operacoes, ...]
token_budget_pct: 20
handoff_in:
  - frontmatter: handoff_contract v1
handoff_out:
  - frontmatter: handoff_contract v1
quality_gates:
  - "Decisão tem 3 alternativas avaliadas"
  - "Cada alternativa tem impacto + custo + risco"
skills_used:
  - positioning-messaging
pipelines:
  - full-growth
  - full-sales
  - product-launch
  - crisis-mode
  - weekly-review
---

# Pensare CEO — Director Strategy

[corpo do agente com prompt-template, exemplos, regras]
```

### Os 17 Agentes (resumo)

Veja [`AGENTS.md`](../AGENTS.md) para spec completa. Resumo:

| # | Agente | Tier | Responsabilidade core |
|---|--------|------|----------------------|
| 0 | `/pensare` | 0 | Triagem, roteamento, síntese |
| 1 | `/pensare-conselho` | 1 | Governança, validação de decisões críticas |
| 2 | `/pensare-ceo` | 1 | Decisões executivas, prioriza Heads |
| 3 | `/pensare-growth` | 2 | Geração de demanda |
| 4 | `/pensare-comercial` | 2 | Pipeline, conversão |
| 5 | `/pensare-operacoes` | 2 | Entrega, SLAs |
| 6 | `/pensare-financeiro` | 2 | Caixa, unit economics |
| 7 | `/pensare-produto` | 2 | Roadmap, oferta |
| 8 | `/pensare-cs` | 2 | Retenção, expansão |
| 9 | `/pensare-estrategia` | 2 | Category Design |
| 10 | `/pensare-automacao` | 2 | Workflows, infra |
| 11 | `/pensare-inteligencia` | 2 | Dados, insights |
| 12 | `/pensare-sdr` | 3 | Qualificação BANT |
| 13 | `/pensare-closer` | 3 | Diagnóstico, fechamento |
| 14 | `/pensare-trafego` | 3 | Mídia paga |
| 15 | `/pensare-copy` | 3 | Textos persuasivos |
| 16 | `/pensare-criativos` | 3 | Conceitos visuais |
| 17 | `/pensare-dados` | 3 | Relatórios, anomalias |

### Handoff Contract

Todo handoff entre agentes carrega frontmatter YAML padronizado:

```yaml
---
handoff_id: 20260513-1430-ceo-comercial
from_agent: /pensare-ceo
to_agent: /pensare-comercial
tier_from: 1
tier_to: 2
priority: high
context_summary: "Decisão de escala AI Systemizer aprovada. Próximo: estruturar processo para fechar +2 MVPs"
deliverable: "Plano de capacitação SDR/Closer + meta de conversão"
decision_required: false
deadline: 2026-05-20
related_memory:
  - "memory/shared/decisions.md"
  - "memory/per-agent/pensare-comercial/pipeline.md"
quality_gates:
  - "Métrica de sucesso definida"
  - "Responsável final nomeado"
---
```

### Regras de Roteamento e Escalação

| Origem | Para onde vai |
|--------|---------------|
| Conversa com lead | `/pensare-sdr` |
| Diagnóstico comercial | `/pensare-closer` |
| Campanha | `/pensare-trafego` |
| Conversão caindo | `/pensare-inteligencia` (skill: funnel-diagnosis) |
| Risco financeiro | `/pensare-financeiro` → escalar para `/pensare-ceo` |
| Mudança estrutural | `/pensare-conselho` |

---

## Camada 3 — Memória

### Os 4 Tipos (inspirados no Letta/MemGPT)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   CORE MEMORY                                                    │
│   ───────────                                                    │
│   • SOUL.md, IDENTITY.md                                         │
│   • Sempre carregado em toda sessão                              │
│   • Imutável dentro de uma sessão                                │
│   • Mudanças = decisão estratégica deliberada                    │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   RECALL MEMORY (estado da sessão)                               │
│   ──────────────                                                 │
│   • MEMORY.md                                                    │
│   • Carregado a cada sessão                                      │
│   • Atualizado ao longo da sessão                                │
│   • Inclui: foco atual, decisões em aberto, próximos passos      │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ARCHIVAL MEMORY (histórico estruturado)                        │
│   ────────────────                                               │
│   • memory/shared/ (compartilhada)                               │
│   • memory/per-agent/ (por agente)                               │
│   • Carregada sob demanda                                        │
│   • Organizada em 4 dimensões semânticas                         │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   EVENT LOG (cronológico append-only)                            │
│   ──────────                                                     │
│   • logs/events.ndjson                                           │
│   • Formato NDJSON (1 linha = 1 evento)                          │
│   • Consultado via tail -10 no boot                              │
│   • Imutável após escrita (audit trail)                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Estrutura física

```
memory/
├── shared/                              ← acessível a todos os agentes
│   ├── context.md                       ← contexto de negócio
│   ├── decisions.md                     ← decisões estratégicas registradas
│   ├── clients.md                       ← clientes ativos
│   │
│   ├── operacional/                     ← memória OPERACIONAL
│   │   ├── leads.md
│   │   ├── conversas.md
│   │   └── vendas.md
│   │
│   ├── estrategica/                     ← memória ESTRATÉGICA
│   │   ├── icp-real.md
│   │   ├── winning-offers.md
│   │   └── posicionamento.md
│   │
│   ├── otimizacao/                      ← memória de OTIMIZAÇÃO
│   │   ├── best-creatives.md
│   │   ├── campaign-patterns.md
│   │   └── funnel-insights.md
│   │
│   └── retencao/                        ← memória de RETENÇÃO
│       ├── churn-insights.md
│       └── evolucao-clientes.md
│
├── per-agent/                           ← por agente
│   ├── pensare-ceo/
│   │   └── reflections.md               ← Reflexion pattern
│   ├── pensare-comercial/
│   │   └── pipeline.md
│   ├── pensare-growth/
│   │   └── campaigns.md
│   └── [outros]/
│
└── events.ndjson                        ← log NDJSON local
```

### Formato do Event Log

`logs/events.ndjson` (uma linha por evento):

```jsonl
{"ts":"2026-05-13T14:30:00Z","agent":"/pensare-ceo","type":"decision","summary":"Aprovou escala controlada AI Systemizer","payload":{"impact":"high"}}
{"ts":"2026-05-13T14:35:00Z","agent":"/pensare-sdr","type":"lead_captured","summary":"Novo lead: empresa X","payload":{"score":8}}
{"ts":"2026-05-13T14:40:00Z","agent":"/pensare-closer","type":"handoff_in","summary":"Recebeu lead qualificado de SDR","payload":{"lead_id":"..."}}
```

### Reflexão por Agente (Reflexion pattern)

Baseado em Shinn et al. 2023. Cada agente mantém `memory/per-agent/{nome}/reflections.md`:

```markdown
# Reflexões — /pensare-comercial

## 2026-05-10 — Fechamento bem-sucedido do 1º MVP

**O que funcionou**: Foco em diagnóstico antes de proposta. O cliente listou as
3 dores antes de eu mencionar valor.

**O que não funcionou**: Eu apressei a apresentação de preço. Próxima vez,
esperar o cliente perguntar.

**Aplicação futura**: Sempre fazer 3 perguntas de diagnóstico antes de qualquer
slide de proposta.

**Tags**: #diagnostico #pricing #1o-mvp
```

Recuperação via `pensare-reflect --agent comercial --top 3 --tag diagnostico`.

### Regras de Atualização da Memória

**Registrar quando**:
- Algo deu muito certo (caso de sucesso replicável)
- Algo deu muito errado (caso para não repetir)
- Padrão se repetiu (3ª ocorrência vira padrão)
- Métrica saiu do normal (>20% de desvio)

**NÃO registrar**:
- Ruído
- Evento isolado sem relevância
- Variação dentro do esperado

**Pergunta-guia**: "O que o sistema aprendeu com isso?"

---

## Camada 4 — Heartbeat

### Componentes

```
heartbeat/
├── daemon.py              ← loop Python (verifica a cada 60s)
├── install.sh             ← instala como LaunchAgent (Mac launchd)
├── requirements.txt       ← stdlib apenas
└── state.json             ← última execução de cada rotina (gitignored)
```

### Funcionamento

```
┌───────────────────────────────────────────────────┐
│  Mac launchd (StartInterval: 60s)                 │
└────────────────────┬──────────────────────────────┘
                     │ executa
                     ▼
┌───────────────────────────────────────────────────┐
│  heartbeat/daemon.py                              │
│                                                   │
│  1. Lê HEARTBEAT.md (parser de rotinas)           │
│  2. Lê heartbeat/state.json (últimas execuções)   │
│  3. Para cada rotina: should_run() ?              │
│  4. Se sim: execute_routine()                     │
│       → subprocess: claude --print /agente {prompt}│
│  5. Atualiza state.json                           │
│  6. Registra evento em logs/events.ndjson         │
└───────────────────────────────────────────────────┘
```

### Modos de execução

```bash
# Preview do que rodaria agora
python heartbeat/daemon.py --dry-run

# Executa uma vez (debug)
python heartbeat/daemon.py --once

# Daemon contínuo em foreground
python heartbeat/daemon.py

# Instala como LaunchAgent (Mac)
bash heartbeat/install.sh
```

### Cadência

Veja [`HEARTBEAT.md`](../HEARTBEAT.md) para detalhes completos.

| Camada | Quando | O que faz |
|--------|--------|-----------|
| **Daily** | 08h, 09h, 16h, 18h | Brief matinal, pipeline, CS check, fechamento |
| **Weekly** | seg 08:30, qua 10h, sex 17h | Planning, market intel, review |
| **Monthly** | dia 1, dia 15 | Fechamento financeiro, mid-month review |

### Gatilhos por evento

9 gatilhos automáticos disparados ao detectar evento:

- `lead_captured` → SDR
- `proposal_sent` → Closer (setup follow-up)
- `client_inactive_7d` → CS (churn-prevention)
- `conversion_dropped` → Comercial (funnel-diagnosis)
- `cpl_increased` → Tráfego (campaign-optimization)
- `offer_not_converting` → Produto (offer-creation)
- `strategic_decision_required` → Conselho
- `financial_alert` → Financeiro
- `session_no_closing` → Coordinator (closing retroativo)

### Thresholds (3 níveis de alerta)

| Métrica | Saudável | Alerta | Crítico |
|---------|----------|--------|---------|
| CTR | ≥1.5% | <1.5% | <1.0% |
| CPL | dentro da meta | +15% | +30% |
| Conversão SQL→venda | ≥10% | <10% | <7% |
| Churn mensal | <5% | 5–10% | >10% |
| NPS | >70 | 50–70 | <50 |
| Runway | >6 meses | 3–6 | <3 |

---

## Camada 5 — Dashboard

### Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI + uvicorn + pyyaml |
| Frontend | HTML5 + Tailwind CSS (CDN) + Alpine.js (CDN) |
| Charts | Vanilla SVG |
| Fonte | Inter (Google Fonts) |
| Build | **nenhum** — tudo CDN |

### Backend (`dashboard/server.py` — 12 endpoints)

```
GET  /api/metrics              ← agrega events.ndjson + empresa.md
GET  /api/events               ← últimos 50 eventos do log
GET  /api/agents               ← scaneia .claude/skills/pensare-*
GET  /api/memory/tree          ← file tree de memory/ + raiz
GET  /api/memory/file          ← lê arquivo com path traversal prevention
PUT  /api/memory/file          ← escreve arquivo
GET  /api/tasks                ← parseia MEMORY.md "Next Steps"
POST /api/tasks                ← adiciona task em MEMORY.md
GET  /api/heartbeats           ← parseia HEARTBEAT.md + state.json
GET  /api/soul                 ← lê SOUL.md + IDENTITY.md + AGENTS.md
POST /api/chat                 ← invoca claude --print /agente
GET  /api/heartbeat/status     ← checa launchctl
```

### Frontend (11 módulos SPA)

| Módulo | URL | Descrição |
|--------|-----|-----------|
| Dashboard | `/` | Métricas cards + bar chart + events table |
| Core | `/core` | Visão dos 4 componentes core |
| Orchestrator | `/orchestrator` | File explorer + editor de configs |
| Agents | `/agents` | Cards dos 17 agentes agrupados por tier |
| Skills | `/skills` | Grid das 10 skills |
| Memory | `/memory` | File tree + split editor |
| Heartbeats | `/heartbeats` | Rotinas + status do daemon |
| Tools | `/tools` | Registry de ferramentas |
| Soul | `/soul` | Seções colapsáveis (princípios, etc.) |
| Tasks | `/tasks` | Kanban drag-and-drop |
| Chat | `/chat` | Conversa com agentes |

### Configuração via env var

`WORKSPACE_ROOT` é configurável:

```python
WORKSPACE_ROOT = Path(os.environ.get("PENSARE_WORKSPACE", "/Users/alicycarvalho/pensare-os"))
```

Em produção (Vercel), funciona apenas como visualização — sem `claude CLI` disponível no serverless.

---

## Fluxo de Dados End-to-End

Exemplo: **novo lead entra via WhatsApp**

```
1. Trigger externo (manual ou integração futura)
   ↓
2. pensare-log "lead_captured" {...}
   → append em logs/events.ndjson
   ↓
3. heartbeat/daemon.py detecta no próximo ciclo (≤60s)
   → checa event-triggers em HEARTBEAT.md
   → match: lead_captured → /pensare-sdr
   ↓
4. subprocess: claude --print /pensare-sdr "qualifique: {lead_data}"
   ↓
5. /pensare-sdr boota:
   → lê SOUL.md, IDENTITY.md (Camada 1)
   → lê MEMORY.md (Camada 3 - Recall)
   → tail -10 logs/events.ndjson
   → carrega skill lead-qualification
   ↓
6. SDR analisa (BANT 0–12), decide:
   - Score >8 → SQL → handoff /pensare-closer
   - Score 5–7 → MQL → nutrição
   - Score <5 → desqualificado
   ↓
7. SDR escreve:
   → memory/per-agent/pensare-comercial/pipeline.md (estado)
   → logs/events.ndjson (evento sdr_qualified)
   → memory/per-agent/pensare-sdr/reflections.md (se relevante)
   ↓
8. Dashboard (Camada 5):
   → polling em /api/events e /api/metrics
   → kanban /tasks reflete novo lead
   → chart /metrics atualiza
   ↓
9. Operadora (Isis) vê no dashboard ou recebe alerta se crítico
```

---

## Padrões Arquiteturais Aplicados

### 1. Orchestrator-Worker Pattern (Anthropic)
Coordinator delega para workers especializados. Inspirado no padrão da Anthropic para multi-agent systems.

### 2. Letta-inspired Memory (file-based MemGPT)
4 camadas de memória (Core/Recall/Archival/Event Log) baseadas em MemGPT, mas em arquivos versionáveis ao invés de banco vetorial.

### 3. Reflexion (Shinn et al. 2023)
Cada agente registra reflexão pós-ação em `reflections.md`. Recuperável por tag e ranking.

### 4. Hierarchy as Cost Discipline
A hierarquia 4-tier não é só organizacional — é **mecanismo de controle de custo** via 10/20/70.

### 5. Event Sourcing (parcial)
`logs/events.ndjson` é append-only, imutável, audit trail completo. Estado derivado pode ser reconstruído.

### 6. Handoff Contracts
Frontmatter YAML em todo handoff força explicitação de contexto, decisão necessária, e quality gates — reduz idas e vindas.

### 7. Heartbeat Pattern
Daemon proativo + cron substitui "esperar comando humano". Sistema antecipa.

---

## Decisões de Design

### Por que arquivos ao invés de banco?

**Trade-off**: queries complexas vs. simplicidade + versionamento + auditabilidade.

**Escolha**: arquivos. Razões:
- Git é o melhor sistema de versionamento existente
- Permite edição manual quando necessário
- Sem dependência de infra (Postgres, Redis, Pinecone)
- O volume de dados é pequeno (KBs, não GBs)
- Backup é `git clone`

### Por que Tailwind/Alpine via CDN?

**Trade-off**: bundle otimizado vs. zero-build.

**Escolha**: CDN. Razões:
- Sem build step = sem manutenção de pipeline
- Mudança de UI = editar 1 arquivo HTML
- Latência aceitável para uso interno
- Tailwind via CDN é production-ready

### Por que Mac launchd e não cron?

**Trade-off**: portabilidade vs. integração nativa.

**Escolha**: launchd. Razões:
- O sistema é da Isis, que opera em Mac
- launchd lida com sleep/wake melhor que cron
- StartInterval é mais simples que crontab
- Logs nativos via `launchctl`

### Por que Claude Code CLI como runtime?

**Trade-off**: API direta vs. CLI tooling.

**Escolha**: Claude Code CLI. Razões:
- Já tem skills, hooks, MCP, sub-agentes nativos
- Não precisamos construir sandbox, tool-use, etc.
- Permission system pronto
- Skills carregam automaticamente do `.claude/skills/`

### Por que NDJSON e não JSON array?

**Trade-off**: parsing vs. append performance.

**Escolha**: NDJSON. Razões:
- Append é O(1) — não precisa reler/reescrever
- Cada linha é parseável independentemente
- `tail -10` funciona out-of-the-box
- Compatível com ferramentas de log (jq, ripgrep)

---

## Limites e Trade-offs

### Limites atuais

1. **Tools não estão conectadas via API nativa** — GHL, WhatsApp, Meta Ads estão documentadas mas executadas via Bash/WebFetch, não SDKs oficiais
2. **Dashboard Vercel é read-only** — backend serverless não consegue rodar `claude CLI` nem rodar daemon
3. **Sem testes automatizados** — sistema é validado manualmente
4. **Single-tenant** — pensado para a operação da Isis; multi-tenancy exigiria refactor
5. **Sem RAG/embeddings** — busca em memória é por path/grep, não semântica
6. **Sem rate limiting nativo** — depende do throttling do Claude Code

### Trade-offs aceitos

| Aceitamos | Em troca de |
|-----------|-------------|
| Sem multi-tenant | Simplicidade radical |
| Sem testes automáticos (por enquanto) | Velocidade de iteração |
| Memória sem embeddings | Auditabilidade total via Git |
| Bash para integrações | Não precisar manter SDKs |
| Mac-only (launchd) | Integração nativa com OS da operadora |

### Próximos passos para escalar

Se o sistema for entregue a clientes via AI Systemizer (modelo serviço), os pontos a evoluir:
- Multi-tenant via sub-diretórios `clients/{nome}/pensare-os/`
- Memory search semântico (embeddings + faiss local)
- Tools conectadas via MCP servers oficiais
- Testes E2E dos fluxos críticos
- Observability (Grafana ou similar)

---

## Referências

- **Letta/MemGPT**: https://github.com/letta-ai/letta (arquitetura de memória)
- **Reflexion** (Shinn et al. 2023): https://arxiv.org/abs/2303.11366
- **Anthropic Orchestrator-Worker**: https://www.anthropic.com/research (multi-agent patterns)
- **Claude Code Skills**: https://docs.claude.com/en/docs/claude-code/skills
- **Event Sourcing**: https://martinfowler.com/eaaDev/EventSourcing.html

---

*Última atualização: 2026-05-13*
