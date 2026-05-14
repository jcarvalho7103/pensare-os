---
name: lead-qualification
description: Qualifica leads usando BANT + fit de ICP, gerando score, tier e próxima ação
argument-hint: "lead: {nome, empresa, cargo, canal_origem, contexto}"
allowed-tools: Read, Write, Bash
tier: skill
version: 0.1.0
usable-by:
  - pensare-sdr
  - pensare-comercial
handoff_in:
  required:
    context: "Dados do lead: nome, empresa, cargo, canal de origem e qualquer contexto disponível (mensagem, formulário, LinkedIn)"
  optional:
    historico: "Interações anteriores com o lead"
    icp_definido: "ICP da campanha ou produto sendo vendido"
handoff_out:
  produces:
    score: "Número de 0 a 100 representando qualificação do lead"
    tier: "Classificação: hot (70-100), warm (40-69), cold (0-39)"
    bant_snapshot: "Resumo dos 4 eixos BANT avaliados"
    proxima_acao: "Ação recomendada com prazo e canal"
quality_gates:
  - "Score calculado com base em evidências explícitas, não suposições"
  - "Tier justificado com pelo menos 2 critérios BANT ou ICP-fit"
  - "Próxima ação é específica: canal + mensagem sugerida + prazo"
  - "Nenhum lead classificado como hot sem Budget ou Authority confirmados"
---

# Lead Qualification

Skill de qualificação de leads para o Pensare OS. Aplica o framework BANT (Budget, Authority, Need, Timeline) combinado com fit de ICP para gerar um score de 0-100, classificar o lead em tier e recomendar a próxima ação comercial.

## Quando Invocar

- Ao receber um novo lead de qualquer canal (formulário, ads, referência, outbound)
- Antes de agendar qualquer reunião de diagnóstico ou demo
- Quando o SDR precisa priorizar uma lista de contatos
- Para revisar leads inativos e decidir se vale reengajamento

---

## Protocolo de Execução

### Passo 1 — Coleta de Dados Disponíveis

Reúna tudo que existe sobre o lead antes de qualquer pergunta:
- Nome, cargo, empresa, setor, tamanho estimado
- Canal de origem (qual ad, qual copy atraiu, qual termo de busca)
- Mensagem inicial ou formulário preenchido
- LinkedIn ou site da empresa (se disponível)

**Regra:** nunca pedir informação que já está disponível no contexto.

---

### Passo 2 — Scoring BANT (25 pts cada eixo)

Avalie cada eixo com base em evidências. Se não há evidência, pontue 0 no eixo — não assuma.

#### Budget (0-25 pts)
| Evidência | Pontos |
|---|---|
| Budget declarado e compatível | 25 |
| Empresa de porte que normalmente tem budget | 15 |
| Mencionou investimento sem valor | 10 |
| Nenhuma evidência de budget | 0 |

#### Authority (0-25 pts)
| Evidência | Pontos |
|---|---|
| CEO, fundador, C-level ou decisor direto | 25 |
| Gerente/coordenador com poder de compra | 15 |
| Influenciador (não decide, mas indica) | 8 |
| Cargo operacional sem poder de compra | 0 |

#### Need (0-25 pts)
| Evidência | Pontos |
|---|---|
| Dor específica declarada e urgente | 25 |
| Interesse claro mas dor genérica | 15 |
| Curiosidade sem necessidade clara | 5 |
| Nenhuma necessidade identificada | 0 |

#### Timeline (0-25 pts)
| Evidência | Pontos |
|---|---|
| Precisa resolver em até 30 dias | 25 |
| Horizonte de 1-3 meses | 15 |
| "Em algum momento" ou sem prazo | 5 |
| Sem urgência ou explorando mercado | 0 |

---

### Passo 3 — ICP Fit Adjustment (+/- 10 pts)

Aplique ajuste com base no fit ao ICP definido:
- **+10 pts:** fit perfeito (setor, tamanho, dor e momento ideais)
- **+5 pts:** fit parcial (2 de 3 critérios do ICP)
- **0 pts:** fit neutro ou desconhecido
- **-10 pts:** fora do ICP (setor errado, tamanho incompatível, sem orçamento típico)

Score final: soma BANT + ajuste ICP, limitado entre 0-100.

---

### Passo 4 — Classificação por Tier

| Score | Tier | Significado |
|---|---|---|
| 70-100 | **hot** | Prioridade máxima. Contato em até 24h. |
| 40-69 | **warm** | Nutrir e qualificar mais. Contato em até 72h. |
| 0-39 | **cold** | Fluxo de nurturing automatizado. Sem esforço manual imediato. |

---

### Passo 5 — Recomendação de Próxima Ação

Com base no tier, recomende uma ação específica:

**Hot:**
- Agendar diagnóstico comercial em 24h
- Canal: WhatsApp (mais rápido) ou ligação
- Mensagem sugerida personalizada com a dor identificada

**Warm:**
- Enviar conteúdo de autoridade relevante à dor identificada
- Fazer 1-2 perguntas de qualificação via WhatsApp ou email
- Tentar avançar BANT nos eixos com menor pontuação

**Cold:**
- Entrar em sequência de email automatizada (5-7 emails)
- Reconsiderar em 30 dias ou quando houver novo sinal de interesse

---

## Template de Output

```
LEAD QUALIFICATION REPORT
=========================
Lead: [Nome] | [Cargo] @ [Empresa]
Canal: [origem]
Data: [data]

BANT SCORE
----------
B - Budget:    [0-25] pts  | [justificativa em 1 linha]
A - Authority: [0-25] pts  | [justificativa em 1 linha]
N - Need:      [0-25] pts  | [justificativa em 1 linha]
T - Timeline:  [0-25] pts  | [justificativa em 1 linha]

ICP Fit:  [+/-X] pts | [justificativa]

SCORE FINAL: [0-100] / 100
TIER: [HOT / WARM / COLD]

PRÓXIMA AÇÃO
------------
Ação: [o que fazer]
Canal: [WhatsApp / Email / Ligação]
Prazo: [quando]
Mensagem sugerida:
"[mensagem pronta para copiar]"

NOTAS
-----
[Observações relevantes sobre o lead que podem ser úteis no diagnóstico]
```

---

## Exemplos de Uso

**Exemplo 1 — Lead hot:**
> Input: João Silva, CEO, empresa de 50 funcionários no varejo, veio pelo ad "Automatize sua operação de vendas", formulário diz "quero implementar IA no meu time comercial ainda esse mês, orçamento disponível de R$3k/mês"
>
> Output: Score 95/100 | Tier: HOT | Próxima ação: WhatsApp em até 4h, agendar diagnóstico

**Exemplo 2 — Lead cold:**
> Input: Ana Lima, assistente administrativa, empresa sem informações, veio de post orgânico de curiosidade sobre IA, nenhuma mensagem adicional
>
> Output: Score 8/100 | Tier: COLD | Próxima ação: sequência de email nurturing

---

## Quality Gates

- Score calculado com base em evidências explícitas, sem suposições
- Tier justificado com pelo menos 2 critérios BANT ou ICP-fit explícitos
- Próxima ação especifica canal, mensagem e prazo
- Nenhum lead classificado como hot sem pelo menos Budget (>10) e Authority (>15) confirmados
- ICP adjustment sempre justificado com critério específico
