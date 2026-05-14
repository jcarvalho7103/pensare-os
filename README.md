# Pensare OS

> Sistema operacional de IA da **Pensare Digital** — 17 agentes especializados, memória persistente, heartbeat autônomo e dashboard próprio rodando sobre Claude Code CLI.

```
╔══════════════════════════════════════════════════╗
║              Pensare OS · v1.0                   ║
║   Transformar conhecimento em Capital Digital    ║
╚══════════════════════════════════════════════════╝
```

[![Production](https://img.shields.io/badge/production-pensare--os.vercel.app-success)](https://pensare-os.vercel.app)
[![GitHub](https://img.shields.io/badge/github-jcarvalho7103%2Fpensare--os-blue)](https://github.com/jcarvalho7103/pensare-os)

---

## O que é o Pensare OS

O Pensare OS é um sistema operacional de inteligência artificial construído para empresas de serviço que querem crescer com método. Não é chatbot, não é assistente genérico, não é ferramenta de produtividade pessoal.

É uma **arquitetura de agentes especializados** que replica a estrutura funcional de uma empresa de alto desempenho — com Conselho, CEO, Heads de área e times de execução — rodando sobre **Claude Code CLI** como runtime.

O Pensare OS pensa, decide, delega, executa e registra. Cada interação é rastreada. Cada decisão tem dono. Cada resultado é conectado a uma estratégia.

---

## Quickstart

```bash
# 1. Clone o repositório
git clone https://github.com/jcarvalho7103/pensare-os.git
cd pensare-os

# 2. Execute o setup
bash setup.sh

# 3. Suba o dashboard local
cd dashboard && python server.py
# → http://localhost:8360

# 4. Em outro terminal, inicie o Claude Code aqui
cd /path/to/pensare-os && claude
> /pensare ola, qual o status do sistema?
```

Veja [`docs/02-getting-started.md`](docs/02-getting-started.md) para o setup completo.

---

## Arquitetura em 1 minuto

```
┌───────────────────────────────────────────────────────────┐
│  CAMADA 1 — IDENTIDADE (Core Memory)                      │
│  SOUL.md · IDENTITY.md · CLAUDE.md                        │
└─────────────────────────────┬─────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────┐
│  CAMADA 2 — AGENTES (17 SKILL.md em .claude/skills/)      │
│  Coordinator → C-Suite → Heads → Execution                │
└─────────────────────────────┬─────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────┐
│  CAMADA 3 — MEMÓRIA (file-based, Letta-inspired)          │
│  Core · Recall · Archival · Event Log (NDJSON)            │
└─────────────────────────────┬─────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────┐
│  CAMADA 4 — HEARTBEAT (Python daemon + launchd)           │
│  Daily/Weekly/Monthly + 9 gatilhos por evento             │
└─────────────────────────────┬─────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────────┐
│  CAMADA 5 — DASHBOARD (FastAPI + SPA)                     │
│  11 módulos visuais para operar o sistema                 │
└───────────────────────────────────────────────────────────┘
```

Detalhes completos em [`docs/01-architecture.md`](docs/01-architecture.md).

---

## Os 17 Agentes

### Tier 0 — Coordinator
| Comando | Função |
|---------|--------|
| `/pensare` | Triagem, roteamento, síntese |

### Tier 1 — C-Suite
| Comando | Função |
|---------|--------|
| `/pensare-conselho` | Governança · valida decisões críticas |
| `/pensare-ceo` | Decisões executivas · prioriza Heads |

### Tier 2 — Heads
| Comando | Função |
|---------|--------|
| `/pensare-growth` | Geração de demanda · canais · CPL/ROAS |
| `/pensare-comercial` | Pipeline · conversão · revenue |
| `/pensare-operacoes` | Processos · entrega · SLAs |
| `/pensare-financeiro` | Caixa · unit economics · projeções |
| `/pensare-produto` | Roadmap · features · oferta |
| `/pensare-cs` | Retenção · NPS · expansão |
| `/pensare-estrategia` | Category Design · narrativa · M&A |
| `/pensare-automacao` | Workflows · integrações · infra |
| `/pensare-inteligencia` | Dados · insights · benchmarks |

### Tier 3 — Execution
| Comando | Função |
|---------|--------|
| `/pensare-sdr` | Prospecção · qualificação BANT |
| `/pensare-closer` | Negociação · fechamento |
| `/pensare-trafego` | Mídia paga · performance |
| `/pensare-copy` | Textos · roteiros · email sequences |
| `/pensare-criativos` | Briefings · conceitos visuais |
| `/pensare-dados` | Relatórios · dashboards · análises |

Detalhes em [`docs/03-agents-guide.md`](docs/03-agents-guide.md) e [`AGENTS.md`](AGENTS.md).

---

## Skills Reutilizáveis

10 skills (frameworks consolidados aplicáveis por múltiplos agentes):

| Skill | Framework | Quem usa |
|-------|-----------|----------|
| `lead-qualification` | BANT 0–100 | SDR, CS |
| `commercial-diagnosis` | D.E.A.L. + SPIN | Closer, Estratégia |
| `objection-handling` | Feel-Felt-Found | Closer |
| `offer-creation` | $100M Offers (Hormozi) | Produto, Closer |
| `positioning-messaging` | April Dunford + StoryBrand | Estratégia, Copy |
| `creative-hook` | 6 hook types | Criativos, Copy |
| `campaign-optimization` | 3-layer diagnosis | Tráfego, Growth |
| `funnel-diagnosis` | 5 stages + benchmarks | Inteligência |
| `pricing-strategy` | Value-Based + Van Westendorp | Financeiro, Produto |
| `churn-prevention` | Health score 5D + 4 playbooks | CS |

Detalhes em [`docs/04-skills-guide.md`](docs/04-skills-guide.md).

---

## Estrutura de Diretórios

```
pensare-os/
├── README.md                ← este arquivo
├── CLAUDE.md                ← boot sequence (auto-loaded pelo Claude Code)
├── SOUL.md                  ← missão, princípios, brand voice
├── IDENTITY.md              ← identidade, produtos, posicionamento
├── AGENTS.md                ← spec canônica dos 17 agentes
├── MEMORY.md                ← estado da sessão atual
├── TOOLS.md                 ← registry de ferramentas
├── HEARTBEAT.md             ← rotinas e gatilhos
├── setup.sh                 ← script de setup completo
├── requirements.txt         ← deps Python (FastAPI, etc.)
├── vercel.json              ← config de deploy Vercel
│
├── .claude/skills/          ← 17 agentes + 10 skills
│   ├── pensare/SKILL.md
│   ├── pensare-ceo/SKILL.md
│   ├── ...
│   ├── skills/
│   │   ├── lead-qualification/SKILL.md
│   │   └── ...
│   └── _shared/bin/         ← CLIs: pensare-log, pensare-status, etc.
│
├── dashboard/               ← FastAPI + SPA
│   ├── server.py            ← 12 endpoints REST
│   ├── index.html           ← SPA com 11 módulos
│   └── requirements.txt
│
├── api/index.py             ← entry point Vercel
│
├── heartbeat/               ← rotinas autônomas
│   ├── daemon.py            ← loop Python
│   └── install.sh           ← LaunchAgent Mac
│
├── memory/                  ← memória persistente
│   ├── shared/              ← compartilhada entre agentes
│   ├── per-agent/           ← por agente
│   └── events.ndjson        ← log NDJSON (ignorado pelo git)
│
├── logs/                    ← logs runtime (ignorado pelo git)
│   └── events.ndjson
│
├── _contexto/               ← contexto de negócio
│   ├── empresa.md
│   ├── mercado.md
│   ├── glossario.md
│   └── lovable-map/         ← mapeamento do Pensare OS Lovable
│
└── docs/                    ← documentação detalhada (este diretório)
    ├── 01-architecture.md
    ├── 02-getting-started.md
    ├── 03-agents-guide.md
    ├── 04-skills-guide.md
    ├── 05-memory-system.md
    ├── 06-heartbeat-runbook.md
    ├── 07-dashboard.md
    ├── 08-deployment.md
    └── 09-troubleshooting.md
```

---

## Índice da Documentação

### Para começar
- **[Getting Started](docs/02-getting-started.md)** — Setup, primeira execução, validações

### Para entender
- **[Arquitetura](docs/01-architecture.md)** — As 5 camadas do sistema em detalhes
- **[Agentes](docs/03-agents-guide.md)** — Como invocar e operar os 17 agentes
- **[Skills](docs/04-skills-guide.md)** — Como usar e criar novas skills
- **[Memória](docs/05-memory-system.md)** — Sistema de memória persistente

### Para operar
- **[Heartbeat](docs/06-heartbeat-runbook.md)** — Daemon, rotinas, gatilhos
- **[Dashboard](docs/07-dashboard.md)** — Interface web do sistema

### Para deployar
- **[Deployment](docs/08-deployment.md)** — GitHub, Vercel, LaunchAgent

### Para resolver
- **[Troubleshooting](docs/09-troubleshooting.md)** — Problemas comuns

### Referência canônica
- **[SOUL.md](SOUL.md)** — Alma do sistema (missão, princípios, brand voice)
- **[IDENTITY.md](IDENTITY.md)** — Identidade da Pensare Digital
- **[AGENTS.md](AGENTS.md)** — Spec canônica dos 17 agentes
- **[HEARTBEAT.md](HEARTBEAT.md)** — Rotinas e gatilhos canônicos
- **[TOOLS.md](TOOLS.md)** — Registry de ferramentas
- **[MEMORY.md](MEMORY.md)** — Estado da sessão atual

---

## Stack Técnica

| Camada | Tecnologia |
|--------|-----------|
| Runtime de agentes | Claude Code CLI (Anthropic) |
| Memória | Arquivos markdown + NDJSON append-only |
| Heartbeat | Python 3 (stdlib) + Mac launchd |
| Dashboard backend | FastAPI + uvicorn + pyyaml |
| Dashboard frontend | HTML + Tailwind CDN + Alpine.js CDN |
| Versionamento | Git + GitHub |
| Deploy | Vercel (serverless Python) |

**Sem build step**. Sem banco de dados. Sem framework de frontend. Tudo arquivo.

---

## Filosofia

> **"Transformar conhecimento, serviço e expertise em Capital Digital."**

O Pensare OS opera segundo 8 princípios não-negociáveis:

1. **Sistema antes de volume**
2. **Fit antes de venda**
3. **Valor antes de preço**
4. **Clareza antes de complexidade**
5. **Dados antes de opinião**
6. **Qualidade antes de escala**
7. **Capital Digital antes de marketing isolado**
8. **Evolução contínua**

E faz 7 perguntas para toda decisão estratégica:
1. Isso fortalece o sistema?
2. Isso aumenta previsibilidade?
3. Isso preserva qualidade?
4. Isso reduz dependência da founder?
5. Isso melhora o Capital Digital?
6. Isso respeita o posicionamento?
7. Isso tem dados suficientes?

**Regra final**: se a decisão gera crescimento mas enfraquece o sistema, ela deve ser ajustada ou bloqueada.

Veja [`SOUL.md`](SOUL.md) para a alma completa do sistema.

---

## Operadora

**Isis Carvalho** — fundadora da Pensare Digital e operadora do Pensare OS.
`jcesar.ccarvalho@gmail.com`

---

## Licença

Uso interno da Pensare Digital. Não distribuir sem autorização.

---

*Pensare OS v1.0 · Runtime: Claude Code CLI · 2026*
