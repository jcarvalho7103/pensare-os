---
name: funnel-diagnosis
description: Diagnóstico completo do funil mapeia cada etapa, identifica gargalos e gera plano de 30 dias
argument-hint: "metricas_funil: {visitantes, leads, qualificados, propostas, fechamentos, retencao}, setor: 'B2B|B2C'"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-dados
  - pensare-growth
  - pensare-trafego
  - pensare-comercial
handoff_in:
  required:
    context: "Métricas por etapa do funil — mínimo: volume de entrada, volume de saída por etapa e receita gerada"
  optional:
    historico: "Dados históricos para comparação de tendência"
    setor: "Setor da empresa para calibrar benchmarks corretamente"
    modelo_negocio: "B2B SaaS, e-commerce, agência, serviço, etc."
    objetivo: "Meta de receita ou crescimento definida"
handoff_out:
  produces:
    mapa_funil: "Visualização ASCII do funil com taxas reais e benchmarks"
    gargalos: "Top 3 gargalos com impacto quantificado em receita perdida"
    plano_30_dias: "Plano de ação por etapa com owner e métricas de sucesso"
    projecao: "Projeção de receita incremental se gargalos forem corrigidos"
quality_gates:
  - "Cada etapa tem taxa de conversão calculada (não estimada)"
  - "Gargalos rankeados por impacto de receita, não por facilidade de resolver"
  - "Plano de 30 dias tem ações específicas, não genéricas"
  - "Projeção de receita tem premissas explícitas"
  - "Mapa ASCII é legível e mostra volume + taxa em cada etapa"
---

# Funnel Diagnosis

Skill de diagnóstico de funil para o Pensare OS. Mapeia todas as etapas do funil (awareness a retenção), calcula taxas de conversão, compara com benchmarks de setor, identifica os top 3 gargalos com impacto em receita e gera plano de ação de 30 dias.

## Quando Invocar

- Quando a receita está abaixo da meta e não está claro por quê
- No onboarding de novo cliente para entender a situação atual
- Na revisão mensal/trimestral de performance
- Quando há queda de performance sem causa óbvia
- Antes de aumentar budget de aquisição (não faz sentido trazer mais tráfego para funil com vazamento)

---

## Modelo de Funil Universal

O diagnóstico cobre 5 macro-etapas, cada uma com sub-etapas:

```
AWARENESS → CONSIDERAÇÃO → DECISÃO → COMPRA → RETENÇÃO
```

### Etapa 1 — Awareness (Topo de Funil)
**Métricas-chave:** impressões, alcance, visitantes únicos, seguidores/inscritos
**Pergunta:** as pessoas certas sabem que você existe?
**Benchmark:** depende do canal; foco em crescimento MoM (meta: >10%/mês no início)

### Etapa 2 — Consideração (Meio de Funil)
**Métricas-chave:** engajamento, tempo na página, visualizações de produto, leads gerados, CPL
**Pergunta:** quem conhece está interessado o suficiente para se aprofundar?
**Benchmark:** CVR visitante→lead = 1-3% (geral) | 2-5% (LP otimizada)

### Etapa 3 — Decisão (Qualificação e Proposta)
**Métricas-chave:** leads qualificados (MQL→SQL), reuniões agendadas, propostas enviadas
**Pergunta:** os leads que chegam têm perfil e são trabalhados corretamente?
**Benchmark:** lead→MQL = 20-40% | MQL→SQL = 30-50% | SQL→proposta = 60-80%

### Etapa 4 — Compra (Fechamento)
**Métricas-chave:** taxa de fechamento, ticket médio, ciclo de vendas (dias)
**Pergunta:** os leads qualificados estão fechando em prazo e valor adequados?
**Benchmark:** proposta→fechamento = 20-30% (B2B complexo) | 30-60% (B2B simples/B2C)

### Etapa 5 — Retenção (Pós-venda)
**Métricas-chave:** churn mensal, NPS, LTV, upsell/cross-sell, indicações
**Pergunta:** quem comprou está ficando, expandindo e indicando?
**Benchmark:** churn mensal saudável = <2% (SaaS) | <5% (serviços) | NPS >40

---

## Benchmarks por Modelo de Negócio

### B2B SaaS
| Etapa | Taxa Ruim | Taxa Ok | Taxa Boa |
|---|---|---|---|
| Visitante → Lead | <0,5% | 1-3% | >3% |
| Lead → MQL | <15% | 20-35% | >35% |
| MQL → SQL | <20% | 30-45% | >45% |
| SQL → Proposta | <50% | 60-75% | >75% |
| Proposta → Fechamento | <15% | 20-30% | >30% |
| Churn mensal | >5% | 2-5% | <2% |

### Agência / Serviços
| Etapa | Taxa Ruim | Taxa Ok | Taxa Boa |
|---|---|---|---|
| Visitante → Lead | <0,3% | 0,5-2% | >2% |
| Lead → Reunião | <10% | 15-30% | >30% |
| Reunião → Proposta | <40% | 50-70% | >70% |
| Proposta → Fechamento | <20% | 25-40% | >40% |
| Renovação/Retenção | <60% | 70-85% | >85% |

### E-commerce
| Etapa | Taxa Ruim | Taxa Ok | Taxa Boa |
|---|---|---|---|
| Visitante → Página produto | <20% | 30-50% | >50% |
| Página produto → Carrinho | <2% | 3-8% | >8% |
| Carrinho → Checkout | <40% | 50-65% | >65% |
| Checkout → Compra | <50% | 60-75% | >75% |
| Recompra (90 dias) | <10% | 20-35% | >35% |

---

## Protocolo de Execução

### Passo 1 — Mapear Volumes por Etapa
Para cada etapa: volume de entrada e volume de saída.
Se não tiver dado, marcar como "desconhecido" — nunca estimar sem avisar.

### Passo 2 — Calcular Taxas de Conversão
Taxa = (saída / entrada) × 100 para cada etapa.

### Passo 3 — Comparar com Benchmarks
Classificar cada etapa: Vermelho (ruim) / Amarelo (aceitável) / Verde (bom).

### Passo 4 — Calcular Impacto de Receita por Gargalo
Para cada etapa vermelha:
> Receita perdida = (volume atual × diferença de taxa até benchmark) × ticket médio

Exemplo: 1.000 leads com 10% de taxa de qualificação (benchmark: 25%) → 150 oportunidades perdidas. Se ticket = R$5k, receita perdida = R$750k/mês.

### Passo 5 — Rankear os Top 3 Gargalos
Por impacto de receita, não por facilidade de resolver.

### Passo 6 — Gerar Plano de 30 Dias
Para cada gargalo: ação específica + owner + prazo + métrica de sucesso.

### Passo 7 — Projetar Resultado
Se os 3 gargalos forem corrigidos para o benchmark "ok": qual é a receita incremental projetada?

---

## Template de Output

```
FUNNEL DIAGNOSIS REPORT
========================
Empresa: [nome]
Modelo de negócio: [tipo]
Período analisado: [período]
Data: [data]

MAPA DO FUNIL
-------------

[AWARENESS]
  Visitantes/mês: X.XXX
  ↓ Taxa: X,X%
[LEADS]
  Leads/mês: XXX
  ↓ Taxa: XX%
[QUALIFICADOS]
  Qualificados/mês: XX
  ↓ Taxa: XX%
[PROPOSTAS]
  Propostas/mês: XX
  ↓ Taxa: XX%
[FECHAMENTOS]
  Novos clientes/mês: X
  Ticket médio: R$ X.XXX
  Receita nova/mês: R$ XX.XXX
  ↓ Taxa de retenção: XX%
[RETENÇÃO]
  Churn mensal: X%
  NPS: XX
  LTV estimado: R$ X.XXX

TAXAS vs. BENCHMARKS
---------------------
| Etapa                    | Taxa Atual | Benchmark | Status |
|--------------------------|------------|-----------|--------|
| Visitante → Lead         | X%         | X%        | [R/Y/G]|
| Lead → Qualificado       | X%         | X%        | [R/Y/G]|
| Qualificado → Proposta   | X%         | X%        | [R/Y/G]|
| Proposta → Fechamento    | X%         | X%        | [R/Y/G]|
| Retenção mensal          | X%         | X%        | [R/Y/G]|

TOP 3 GARGALOS
--------------
#1 GARGALO: [etapa]
   Taxa atual: X% | Benchmark: X% | Gap: X pp
   Receita perdida estimada: R$ X.XXX/mês
   Causa provável: [diagnóstico em 2 linhas]

#2 GARGALO: [etapa]
   Taxa atual: X% | Benchmark: X% | Gap: X pp
   Receita perdida estimada: R$ X.XXX/mês
   Causa provável: [diagnóstico]

#3 GARGALO: [etapa]
   Taxa atual: X% | Benchmark: X% | Gap: X pp
   Receita perdida estimada: R$ X.XXX/mês
   Causa provável: [diagnóstico]

PLANO DE 30 DIAS
----------------

SEMANA 1-2 (Gargalo #1: [nome]):
  [ ] Ação 1: [específica] | Owner: [quem] | Prazo: [data]
      Métrica de sucesso: [taxa X% → Y%]
  [ ] Ação 2: [específica] | Owner: [quem] | Prazo: [data]

SEMANA 2-3 (Gargalo #2: [nome]):
  [ ] Ação 1: [específica] | Owner: [quem] | Prazo: [data]
  [ ] Ação 2: [específica] | Owner: [quem] | Prazo: [data]

SEMANA 3-4 (Gargalo #3: [nome]):
  [ ] Ação 1: [específica] | Owner: [quem] | Prazo: [data]
  [ ] Ação 2: [específica] | Owner: [quem] | Prazo: [data]

PROJEÇÃO DE IMPACTO
-------------------
Premissas: [lista das premissas usadas]

Se gargalos forem corrigidos para benchmark "ok":
  Receita incremental estimada: R$ X.XXX/mês
  Novo MRR projetado: R$ X.XXX (vs. atual R$ X.XXX)
  Prazo para ver resultado: [X dias]

Cenário conservador (50% da melhoria): R$ X.XXX/mês incremental
Cenário base (100% da melhoria): R$ X.XXX/mês incremental
```

---

## Exemplos de Uso

**Exemplo 1 — Agência B2B com problema de fechamento:**
> Métricas: 500 visitantes → 15 leads → 6 reuniões → 5 propostas → 0,5 fechamentos/mês
> Diagnóstico: gargalo #1 = proposta→fechamento (10% vs. benchmark 25%). Gargalo #2 = lead→reunião (40% ok). Gargalo #3 = visitante→lead (3% ok)
> Plano: revisar metodologia de proposta, adicionar diagnóstico estruturado, follow-up em 48h

**Exemplo 2 — SaaS com churn alto:**
> Churn mensal 8% (benchmark <2%) → gargalo #1 = retenção
> Receita perdida: 8% do MRR todo mês = perda de R$40k/mês em base de R$500k
> Plano: implementar health score, criar CSM para top 20% da base, programa de onboarding estruturado

---

## Quality Gates

- Cada etapa tem taxa de conversão calculada com dados reais (não estimados sem aviso)
- Gargalos rankeados por impacto de receita (não por facilidade de resolver)
- Plano de 30 dias tem ações específicas, owner e métrica de sucesso para cada item
- Projeção de receita tem premissas explícitas listadas
- Mapa ASCII mostra volume e taxa em cada etapa de forma legível
- Benchmarks usados são declarados com fonte ou calibrados ao setor informado
