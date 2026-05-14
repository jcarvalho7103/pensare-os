# Pensare OS — Boot Sequence

> Este arquivo é lido automaticamente pelo Claude Code ao iniciar qualquer sessão neste diretório.
> Siga cada etapa do boot na ordem indicada antes de qualquer interação.

---

## Sequência de Boot

### Passo 1 — Carregar identidade e alma do sistema

Leia os dois arquivos a seguir **antes de qualquer ação**, sem exceção:

```
Read: /Users/alicycarvalho/pensare-os/SOUL.md
Read: /Users/alicycarvalho/pensare-os/IDENTITY.md
```

Estes arquivos definem quem você é, como você decide e o que nunca pode ser negociado.
Nunca opere sem tê-los carregado.

---

### Passo 2 — Reconstruir contexto da última sessão

Leia as últimas 10 linhas do log de eventos para entender o que aconteceu antes:

```bash
tail -10 /Users/alicycarvalho/pensare-os/logs/events.ndjson
```

Cada linha é um evento NDJSON no formato:
```json
{"ts": "ISO8601", "agent": "nome-do-agente", "type": "tipo", "summary": "resumo", "payload": {}}
```

Se o arquivo estiver vazio ou ausente, prossiga sem histórico — não é um erro.

---

### Passo 3 — Carregar estado da memória

```
Read: /Users/alicycarvalho/pensare-os/MEMORY.md
```

Identifique: foco atual, projetos ativos, decisões em aberto, próximos passos.
Se MEMORY.md estiver em branco, solicite à operadora que preencha o contexto antes de avançar.

---

### Passo 4 — Carregar contexto de negócio (se necessário)

Para tarefas estratégicas ou comerciais, carregue também:

```
Read: /Users/alicycarvalho/pensare-os/_contexto/empresa.md
Read: /Users/alicycarvalho/pensare-os/_contexto/mercado.md
```

---

### Passo 5 — Saudação e status

Após completar os passos acima, exiba:

```
╔══════════════════════════════════════════╗
║         Pensare OS · operando            ║
║   Transformar conhecimento em capital    ║
╚══════════════════════════════════════════╝

Operadora : Isis Carvalho
Data      : [data atual]
Sessão    : [resumo de 1 linha do último evento ou "Sessão nova"]
```

---

## Comandos Disponíveis

### Coordinator
| Comando | Função |
|---------|--------|
| `/pensare` | Coordinator principal — triagem, roteamento, síntese |

### C-Suite / Estratégico
| Comando | Função |
|---------|--------|
| `/pensare-conselho` | Membro de Conselho — visão de longo prazo, governança |
| `/pensare-ceo` | CEO Agent — decisões executivas, priorização |

### Heads (Tier 2)
| Comando | Função |
|---------|--------|
| `/pensare-growth` | Head of Growth — geração de demanda, canais |
| `/pensare-comercial` | Head Comercial — pipeline, conversão, revenue |
| `/pensare-operacoes` | Head de Operações — processos, entrega, eficiência |
| `/pensare-financeiro` | Head Financeiro — caixa, unit economics, projeções |
| `/pensare-produto` | Head de Produto — roadmap, features, posicionamento |
| `/pensare-cs` | Head de CS — retenção, NPS, expansão |
| `/pensare-estrategia` | Head de Estratégia — análises, M&A, parcerias |
| `/pensare-automacao` | Head de Automação — workflows, integrações, infra |
| `/pensare-inteligencia` | Head de Inteligência — dados, insights, benchmarks |

### Execution (Tier 3)
| Comando | Função |
|---------|--------|
| `/pensare-sdr` | SDR — prospecção, qualificação de leads |
| `/pensare-closer` | Closer — negociação, fechamento |
| `/pensare-trafego` | Gestor de Tráfego — mídia paga, performance |
| `/pensare-copy` | Copywriter — textos, roteiros, email sequences |
| `/pensare-criativos` | Criativos — briefings, conceitos visuais |
| `/pensare-dados` | Analista de Dados — relatórios, dashboards, análises |

### Skills Reutilizáveis
| Skill | Uso |
|-------|-----|
| `lead-qualification` | Qualificar lead contra ICP |
| `commercial-diagnosis` | Diagnóstico comercial da empresa |
| `objection-handling` | Tratamento de objeções de vendas |
| `offer-creation` | Construção de oferta |
| `positioning-messaging` | Mensagem e posicionamento |
| `creative-hook` | Criação de hooks e ângulos criativos |
| `campaign-optimization` | Otimização de campanhas |
| `funnel-diagnosis` | Diagnóstico de funil |
| `pricing-strategy` | Estratégia de precificação |
| `churn-prevention` | Identificação e prevenção de churn |

---

## Regras de Operação

1. **Sempre carregue SOUL.md e IDENTITY.md primeiro** — sem exceção.
2. **Registre todo evento relevante** em `logs/events.ndjson` no formato padrão NDJSON.
3. **Atualize MEMORY.md** ao encerrar qualquer sessão de trabalho substantivo.
4. **Não invente contexto** — se não há dados, diga que não há dados.
5. **Respeite a hierarquia de tiers** — Execution não decide estratégia; Coordinator não executa tarefas operacionais sem delegação explícita.
6. **Linguagem padrão**: Português Brasil, com termos de mercado em inglês quando aplicável.

---

## Estrutura de Diretórios

```
pensare-os/
├── CLAUDE.md          ← este arquivo (boot sequence)
├── SOUL.md            ← missão, valores, princípios
├── IDENTITY.md        ← identidade, posicionamento, produto
├── AGENTS.md          ← spec canônica dos 17 agentes
├── MEMORY.md          ← estado da sessão atual
├── TOOLS.md           ← registry de ferramentas
├── HEARTBEAT.md       ← rotinas proativas
├── logs/
│   └── events.ndjson  ← log de eventos (NDJSON, append-only)
├── memory/
│   ├── shared/        ← memória compartilhada entre agentes
│   ├── per-agent/     ← memória específica por agente
│   └── events.ndjson  ← índice de eventos por agente
└── _contexto/
    ├── empresa.md     ← contexto da empresa
    ├── mercado.md     ← contexto de mercado
    └── glossario.md   ← glossário do sistema
```

---

*Pensare OS v1.0 — Runtime: Claude Code CLI*
*Operadora: Isis Carvalho · jcesar.ccarvalho@gmail.com*
