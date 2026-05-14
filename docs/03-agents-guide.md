# Agents Guide — Pensare OS

> Guia operacional para os 17 agentes. Para spec canônica, veja [`AGENTS.md`](../AGENTS.md).

---

## Filosofia da Hierarquia

O Pensare OS opera com **4 tiers** que refletem a estrutura de uma empresa de alto desempenho:

```
TIER 0 — COORDINATOR   (entry point — triagem)
   ▼
TIER 1 — C-SUITE       (governança + estratégia)
   ▼
TIER 2 — HEADS         (área específica + análise)
   ▼
TIER 3 — EXECUTION     (mãos na massa)
```

### As 4 Leis da Hierarquia

1. **Operacional não decide estratégia** — T3 só executa
2. **Head não ignora CEO** — T2 opera dentro da estratégia aprovada
3. **CEO não ignora Conselho** — decisões irreversíveis sobem
4. **Sempre decidir no menor nível possível**

---

## Disciplina de Custo (10/20/70)

| Tier | % tokens | Razão |
|------|----------|-------|
| T0 + T1 | 10% | Decisões concisas, alto sinal |
| T2 (Heads) | 20% | Análise com profundidade controlada |
| T3 (Execution) | 70% | Onde o trabalho acontece |

Monitore via:
```bash
pensare-cost --alert
```

Dispara aviso se custo > target × 1.5.

---

## Tier 0 — Coordinator

### `/pensare`

**Quando invocar**: Toda sessão começa aqui. Use quando você não sabe qual agente específico precisa.

**O que ele faz**:
- Interpreta sua intenção
- Identifica qual agente(s) acionar
- Faz triagem e roteamento
- Sintetiza resultados quando múltiplos agentes são usados

**Pergunta central**: "Qual é o próximo melhor agente para agir agora?"

**Nunca faz**: executa tarefas operacionais diretamente, toma decisões estratégicas, ignora hierarquia.

**Exemplos de uso**:
```
/pensare ola, qual o status do sistema?

/pensare estou pensando em aumentar o preço do AI Systemizer.
Por onde começo a análise?

/pensare encerre a sessão e atualize MEMORY.md
```

---

## Tier 1 — C-Suite

### `/pensare-conselho`

**Quando invocar**:
- Decisões irreversíveis ou de alto custo
- Mudanças de posicionamento
- Entrada em novos mercados
- Revisão de pricing
- Análises de expansão ou M&A
- Quando você precisa de "freio" estratégico

**Pergunta central**: "Essa decisão fortalece ou enfraquece o sistema da Pensare?"

**Atua em**: Governança, Estratégia, Gestão, Risco, Sustentabilidade, Coerência sistêmica.

**Aplica as 7 perguntas da Decision Philosophy** (ver `SOUL.md`):
1. Isso fortalece o sistema?
2. Isso aumenta previsibilidade?
3. Isso preserva qualidade?
4. Isso reduz dependência da founder?
5. Isso melhora o Capital Digital?
6. Isso respeita o posicionamento?
7. Isso tem dados suficientes?

**Output**: Veredito (Alinhada | Ajustar | Bloquear) + justificativa + risco + ajuste recomendado.

**Exemplo**:
```
/pensare-conselho avalie a proposta de lançar o SaaS de R$ 5k +
recorrência. Quais riscos sistêmicos eu não estou enxergando?
```

### `/pensare-ceo`

**Quando invocar**:
- Definir prioridades semanais ou mensais
- Conflito entre Heads
- Aprovação de plano antes da execução
- Revisões mensais de performance
- Tradução de visão em ação

**Pergunta central**: "Qual a próxima prioridade que mais alavanca receita previsível?"

**5 Pipelines pré-configurados**:
- `full-growth` — campanha completa de geração de demanda
- `full-sales` — sprint comercial focado em fechamento
- `product-launch` — lançamento de oferta nova
- `crisis-mode` — diagnóstico + ação em queda de métrica
- `weekly-review` — revisão semanal padrão

**Exemplo**:
```
/pensare-ceo me dê as 3 prioridades para esta semana com base em
MEMORY.md e nos eventos dos últimos 7 dias

/pensare-ceo execute o pipeline weekly-review
```

---

## Tier 2 — Heads de Área

### `/pensare-growth` — Head de Growth

**KPIs**: Leads gerados, CPL, CTR, conversão topo de funil, ROAS

**Supervisiona**: Tráfego, Copy, Criativos

**Regra-mãe**: nunca escalar campanha não validada.

**Skills**: `positioning-messaging`, `creative-hook`, `campaign-optimization`

**Exemplo**:
```
/pensare-growth nossa CPL está em R$ 80 — meta é R$ 50. Diagnostique
e me dê plano de 3 ações para 7 dias.
```

### `/pensare-comercial` — Head Comercial

**KPIs**: Pipeline total, taxa MQL→SQL, SQL→venda, ASP, ciclo de vendas

**Supervisiona**: SDR, Closer

**Skills**: `commercial-diagnosis`, `objection-handling`, `offer-creation`, `pricing-strategy`

**Exemplo**:
```
/pensare-comercial me mostre o pipeline atual, identifique o lead
mais quente e proponha a próxima ação
```

### `/pensare-operacoes` — Head de Operações

**KPIs**: Tempo de entrega, NPS de delivery, taxa de retrabalho

**Supervisiona**: Dados

**Skills**: `funnel-diagnosis`

**Exemplo**:
```
/pensare-operacoes o 1º MVP do AI Systemizer está em onboarding.
Audite o processo e identifique riscos de SLA.
```

### `/pensare-financeiro` — Head Financeiro

**KPIs**: MRR/ARR, CAC, LTV, LTV:CAC, churn de receita, runway, margem

**Skills**: `pricing-strategy`

**Exemplo**:
```
/pensare-financeiro projete o caixa para os próximos 90 dias dado
o pipeline atual e os custos de mai/2026
```

### `/pensare-produto` — Head de Produto / Oferta

**KPIs**: NPS produto, time-to-value, conversão da oferta

**Skills**: `positioning-messaging`, `offer-creation`

**Exemplo**:
```
/pensare-produto a oferta do AI Systemizer está convertendo 12%.
Como aumentamos para 25%?
```

### `/pensare-cs` — Head de Customer Success

**KPIs**: NPS, churn rate, expansion revenue, health score, time-to-first-value

**Skills**: `churn-prevention`, `lead-qualification` (para expansão)

**Exemplo**:
```
/pensare-cs revise os clientes ativos e identifique 1 que está em
risco de churn. Proponha touchpoint de reengajamento.
```

### `/pensare-estrategia` — Head de Estratégia / Category Design

**KPIs**: Percepção de categoria, share-of-voice em "Capital Digital"

**Skills**: `commercial-diagnosis`, `positioning-messaging`

**Exemplo**:
```
/pensare-estrategia escreva 3 posts de LinkedIn que defendem a
categoria Capital Digital sem atacar concorrentes
```

### `/pensare-automacao` — Head de Automação / Sistemas

**KPIs**: Uptime de workflows, tempo de resolução de falhas

**Skills**: todas (manutenção e evolução)

**Exemplo**:
```
/pensare-automacao audite os arquivos em .claude/skills/ e
identifique inconsistências entre os frontmatters
```

### `/pensare-inteligencia` — Head de Inteligência de Mercado

**KPIs**: Cobertura de métricas, latência de insight

**Supervisiona**: Dados

**Skills**: `funnel-diagnosis`, `campaign-optimization`

**Exemplo**:
```
/pensare-inteligencia faça scan de mercado dos últimos 7 dias para
movimentações de concorrentes em IA para PMEs no Brasil
```

---

## Tier 3 — Execution

### `/pensare-sdr` — SDR IA (Mariana)

**Responsabilidade**: Inicia conversa, diagnostica, qualifica leads (BANT 0–12).

**Skills**: `lead-qualification`

**Exemplo**:
```
/pensare-sdr qualifique este lead:
"Sou João, dono de uma agência de marketing. Faturamos R$ 80k/mês,
6 funcionários, queremos escalar mas o processo comercial é caos.
Vi seu post no LinkedIn sobre AI Systemizer."
```

### `/pensare-closer` — Closer IA

**Responsabilidade**: Conduz diagnóstico comercial, trata objeções, orienta fechamento.

**Framework**: D.E.A.L. + Feel-Felt-Found para objeções

**Skills**: `objection-handling`, `offer-creation`, `commercial-diagnosis`

**Exemplo**:
```
/pensare-closer um prospect disse: "Achei caro, vou pensar".
Aplique Feel-Felt-Found e proponha próximo passo.
```

### `/pensare-trafego` — Tráfego IA

**Responsabilidade**: Executa campanhas Meta/Google/LinkedIn, otimiza CPL.

**Skills**: `campaign-optimization`

**Exemplo**:
```
/pensare-trafego nossa campanha "AI Systemizer LinkedIn 03" está
com CTR 0.8% e CPL R$ 95. Diagnostique em 3 camadas (creative/LP/oferta).
```

### `/pensare-copy` — Copy IA

**Responsabilidade**: Escreve copies para ads, LPs, emails, sequências, posts.

**Frameworks**: PAS, AIDA, FAB + anti-AI self-check (Brand Voice de `SOUL.md`)

**Skills**: `positioning-messaging`, `creative-hook`

**Exemplo**:
```
/pensare-copy escreva 3 variações de headline para o lead magnet
"Diagnóstico de Capital Digital" — ICP: founders de agências
```

### `/pensare-criativos` — Criativos IA

**Responsabilidade**: Briefings de hooks, roteiros de vídeo, conceitos visuais.

**Skills**: `creative-hook`

**Exemplo**:
```
/pensare-criativos gere 3 conceitos de hook para vídeo de 30s sobre
"sistema antes de volume", target founders B2B
```

### `/pensare-dados` — Dados IA

**Responsabilidade**: Análises, dashboards, anomalia, relatórios.

**Lê**: `logs/events.ndjson`, métricas em `memory/`

**Skills**: `funnel-diagnosis`, `campaign-optimization`

**Exemplo**:
```
/pensare-dados gere relatório de eventos dos últimos 14 dias.
Identifique anomalias e tendências.
```

---

## Como invocar um agente

### Forma 1 — Direta
```
/pensare-ceo defina as prioridades da semana
```

### Forma 2 — Via Coordinator
```
/pensare preciso de uma decisão sobre pricing
```
O Coordinator vai rotear para `/pensare-financeiro` ou `/pensare-conselho` conforme apropriado.

### Forma 3 — Pipeline (CEO)
```
/pensare-ceo execute o pipeline crisis-mode porque receita caiu 20%
```

### Forma 4 — Via Dashboard
1. Abra http://localhost:8360/chat
2. Selecione o agente
3. Digite a mensagem

---

## Padrões de Handoff

Quando um agente delega para outro, sempre via handoff contract YAML:

```yaml
---
handoff_id: 20260513-1430-ceo-comercial
from_agent: /pensare-ceo
to_agent: /pensare-comercial
tier_from: 1
tier_to: 2
priority: high
context_summary: "Aprovação de escala AI Systemizer — próximo: estruturar processo"
deliverable: "Plano de capacitação SDR/Closer + meta de conversão"
decision_required: false
deadline: 2026-05-20
quality_gates:
  - "Métrica de sucesso definida"
  - "Responsável final nomeado"
---
```

### Quando escalar para cima

| De | Para | Quando |
|----|------|--------|
| T3 | T2 | Impacto relevante, decisão tática |
| T2 | T1 (CEO) | Conflito de prioridades, decisão estratégica |
| T1 (CEO) | T1 (Conselho) | Risco financeiro, mudança estrutural |
| T1 (Conselho) | Operadora | Decisão irreversível ou de alto custo |

---

## Sinais de mau uso

Você está **usando errado** quando:

- ❌ Chama `/pensare-ceo` para tarefa operacional (escrever copy, qualificar lead)
- ❌ Chama `/pensare-trafego` para definir estratégia de pricing
- ❌ Pula o Coordinator quando não sabe qual agente precisa
- ❌ Ignora o handoff contract entre agentes (perde rastreabilidade)
- ❌ Não atualiza MEMORY.md ao final de sessão substantiva
- ❌ Usa um agente fora do seu domínio (CEO para análise de criativo, por exemplo)

Você está **usando certo** quando:

- ✓ Cada agente opera no seu tier
- ✓ Decisões irreversíveis passam pelo Conselho
- ✓ Tarefas executáveis caem em T3
- ✓ MEMORY.md reflete o estado real
- ✓ `logs/events.ndjson` cresce a cada sessão

---

## Cheatsheet de invocação rápida

| Preciso de... | Agente |
|---------------|--------|
| Triagem inicial | `/pensare` |
| Avaliar decisão irreversível | `/pensare-conselho` |
| Prioridades da semana | `/pensare-ceo` |
| Diagnóstico de pipeline | `/pensare-comercial` |
| Otimizar CPL | `/pensare-trafego` ou `/pensare-growth` |
| Escrever copy | `/pensare-copy` |
| Hook criativo | `/pensare-criativos` |
| Qualificar lead | `/pensare-sdr` |
| Tratar objeção | `/pensare-closer` |
| Projeção financeira | `/pensare-financeiro` |
| Health check cliente | `/pensare-cs` |
| Reposicionamento | `/pensare-estrategia` |
| Análise de dados | `/pensare-dados` |
| Inteligência competitiva | `/pensare-inteligencia` |
| Audit técnico do OS | `/pensare-automacao` |
| Onboarding cliente | `/pensare-operacoes` |
| Oferta nova | `/pensare-produto` |

---

*Para o spec canônico (KPIs, frontmatter completo), veja [`AGENTS.md`](../AGENTS.md).*
