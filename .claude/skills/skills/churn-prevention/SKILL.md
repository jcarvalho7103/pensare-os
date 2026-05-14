---
name: churn-prevention
description: Calcula health score, identifica clientes em risco e gera playbook personalizado de retenção
argument-hint: "cliente: {tempo_de_casa, uso_semanal, nps, ultimas_interacoes, expansao_historica}"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-cs
  - pensare-comercial
handoff_in:
  required:
    context: "Dados do cliente: tempo de casa (meses), frequência de uso, NPS ou CSAT mais recente, histórico de interações com suporte e CS"
  optional:
    expansao: "Histórico de expansão (upsell/cross-sell) ou redução de escopo"
    onboarding: "Como foi o onboarding — estruturado, autoguiado, com dificuldades"
    objetivo_original: "O que o cliente queria resolver quando contratou"
    concorrentes: "Sinais de que está avaliando alternativas"
handoff_out:
  produces:
    health_score: "Score 0-100 com breakdown por dimensão"
    perfil_risco: "Classificação: em risco / estável / saudável / expansível"
    playbook: "Sequência de ações para o perfil identificado"
    proximas_3_acoes: "As 3 próximas ações específicas com prazo e responsável"
    template_mensagem: "Mensagem pronta para o canal de contato do cliente"
quality_gates:
  - "Health score calculado com ao menos 3 das 5 dimensões com dados reais"
  - "Perfil de risco justificado com evidências específicas, não suposições"
  - "Playbook é diferente por perfil — não serve a mesma abordagem para todos"
  - "Template de mensagem usa contexto real do cliente, não é genérico"
  - "Próximas 3 ações têm prazo, owner e métrica de resultado"
---

# Churn Prevention & Retention

Skill de prevenção de churn e expansão de contas para o Pensare OS. Calcula o health score do cliente com base em 5 dimensões, classifica o perfil de risco e gera playbook personalizado com as próximas ações e template de mensagem pronto para uso.

## Quando Invocar

- Na revisão mensal do portfólio de clientes (triagem de risco)
- Quando um cliente para de usar o produto ou desaparece
- Antes de renovações ou revisões contratuais
- Quando um cliente abre chamado de reclamação ou NPS negativo
- Para identificar clientes prontos para expansão (upsell/cross-sell)
- Em onboardings com dificuldade para sinalizar risco precoce

---

## Health Score — 5 Dimensões (20 pts cada)

### Dimensão 1 — Uso do Produto (0-20 pts)

| Uso | Pontos |
|---|---|
| Usa ativamente toda semana, volume crescente | 20 |
| Usa toda semana, volume estável | 15 |
| Usa pelo menos 2x por semana | 10 |
| Usa esporadicamente (menos de 1x/semana) | 5 |
| Não usa há mais de 2 semanas | 0 |

**Sinal de alarme:** queda de >50% no uso em 2 semanas consecutivas.

---

### Dimensão 2 — Engajamento com CS/Suporte (0-20 pts)

| Engajamento | Pontos |
|---|---|
| Responde rápido, participa de QBRs, proativo | 20 |
| Responde quando acionado, participação regular | 15 |
| Responde com atraso, participação irregular | 8 |
| Raramente responde, cancela reuniões | 3 |
| Sumiu — sem resposta há mais de 3 semanas | 0 |

**Sinal de alarme:** cliente que deixa de responder sem explicação.

---

### Dimensão 3 — Histórico de Suporte (0-20 pts)

| Suporte | Pontos |
|---|---|
| Sem tickets ou tickets resolvidos com satisfação | 20 |
| 1-2 tickets no mês, resolvidos | 15 |
| Tickets recorrentes mas resolvidos | 8 |
| Tickets recorrentes sem resolução satisfatória | 3 |
| Escalada, reclamação formal ou ameaça de cancelar | 0 |

**Sinal de alarme:** mesmo problema reportado mais de 1x sem solução definitiva.

---

### Dimensão 4 — NPS / Satisfação (0-20 pts)

| NPS | CSAT | Pontos |
|---|---|---|
| Promotor (9-10) | Muito satisfeito | 20 |
| Neutro (7-8) | Satisfeito | 12 |
| Detrator (0-6) | Insatisfeito | 2 |
| Não respondeu | N/A | 8 |
| Cancelou pesquisa / recusou responder | N/A | 4 |

**Sinal de alarme:** detrator ou queda de 2+ pontos em relação à última pesquisa.

---

### Dimensão 5 — Histórico de Expansão (0-20 pts)

| Expansão | Pontos |
|---|---|
| Expandiu escopo ou plano nos últimos 6 meses | 20 |
| Usando 100% da capacidade contratada | 15 |
| Estável, sem expansão, sem redução | 10 |
| Pediu redução de escopo ou downgrade | 3 |
| Cancelou módulo ou reduziu investimento | 0 |

**Sinal de alarme:** pedido de downgrade ou cancelamento parcial.

---

## Classificação por Health Score

| Score | Perfil | Significado |
|---|---|---|
| 80-100 | **Expansível** | Cliente saudável, pronto para expandir. Prioridade: upsell/cross-sell. |
| 60-79 | **Saudável** | Tudo bem, manter o ritmo. Prioridade: aprofundar relacionamento. |
| 40-59 | **Atenção** | Sinais mistos. Prioridade: identificar o que não está funcionando antes que piore. |
| 20-39 | **Em Risco** | Risco alto de churn. Prioridade: intervenção imediata. |
| 0-19 | **Crítico** | Quase certeza de churn se nada for feito. Prioridade: salvar ou managed exit. |

---

## Playbooks por Perfil

### Playbook — Em Risco (score 20-39)

**Objetivo:** identificar causa-raiz do risco e criar plano de recuperação.

1. **Contato imediato (24-48h):** ligação ou reunião, não mensagem de texto
2. **Agenda da reunião:**
   - Abrir sem agenda oculta: "Quero entender como está sendo sua experiência"
   - Perguntar o que não está funcionando (não defender o produto)
   - Ouvir mais do que falar
3. **Identificar a causa-raiz:** é de produto (não entrega resultado), de CS (abandono), de contexto (mudança interna no cliente), ou de expectativa (prometeram mais do que entregaram)?
4. **Propor ação específica:** não prometer em geral — comprometer-se com 1 coisa concreta e fazer
5. **Follow-up em 7 dias:** verificar se a ação foi executada
6. **Se não houver recuperação em 30 dias:** managed exit (perder bem, manter relacionamento)

**Evitar:** defender o produto antes de ouvir, prometer desconto como solução, sumir após a reunião.

---

### Playbook — Em Atenção (score 40-59)

**Objetivo:** diagnosticar o que está incompleto antes que vire risco.

1. **Check-in proativo em até 7 dias:** mensagem ou email perguntando como está
2. **Business Review simplificado:** revisar resultados obtidos vs. esperados
3. **Identificar o gap:** o que ainda não aconteceu que o cliente esperava?
4. **Reforçar valor entregue:** mostrar dados de uso e resultados (muitas vezes o cliente não sabe o que já ganhou)
5. **Criar novo plano de 30 dias:** metas específicas com o cliente
6. **Verificar contexto:** mudou algo no cliente (budget, time, prioridade estratégica)?

---

### Playbook — Saudável (score 60-79)

**Objetivo:** manter e aprofundar o relacionamento.

1. **Reunião de QBR (Quarterly Business Review):** revisão trimestral de resultados
2. **Compartilhar novidades do produto** que são relevantes para esse cliente
3. **Pedir indicações:** clientes satisfeitos raramente indicam se não forem pedidos diretamente
4. **Mapear outras áreas:** há outras áreas da empresa que poderiam se beneficiar?
5. **Coletar case study / depoimento**

---

### Playbook — Expansível (score 80-100)

**Objetivo:** identificar e capturar oportunidade de expansão.

1. **Revisão de uso:** onde está usando bem? O que ainda não está usando?
2. **Mapear necessidades adjacentes:** o que mais o cliente quer resolver além do que já resolve com você?
3. **Apresentar upsell/cross-sell** como evolução natural, não como venda
4. **Proposta de expansão:** com ROI calculado, baseado nos resultados já obtidos
5. **Solicitar indicação formal** com incentivo se aplicável

---

## Protocolo de Execução

### Passo 1 — Coletar Dados do Cliente
Reunir informações nas 5 dimensões. Se alguma dimensão não tiver dado, marcar como "desconhecido" e pontuar com o mínimo conservador (5 pts).

### Passo 2 — Calcular Health Score
Somar pontos por dimensão. Anotar qual dimensão está mais baixa.

### Passo 3 — Classificar Perfil
Aplicar a tabela de classificação. Identificar o sinal de alarme mais relevante.

### Passo 4 — Selecionar e Personalizar Playbook
Usar o playbook do perfil, mas personalizar com o contexto específico do cliente.

### Passo 5 — Definir as 3 Próximas Ações
Concreta, com prazo e owner definidos.

### Passo 6 — Escrever Template de Mensagem
Adaptar ao canal (WhatsApp, email, LinkedIn) e ao contexto real do cliente.

---

## Template de Output

```
CHURN PREVENTION REPORT
========================
Cliente: [Nome] | [Cargo] @ [Empresa]
Tempo de casa: [X meses]
CS Responsável: [nome]
Data: [data]

HEALTH SCORE
------------
| Dimensão               | Pontos | Evidência                        |
|------------------------|--------|----------------------------------|
| Uso do produto         | X/20   | [evidência específica]           |
| Engajamento com CS     | X/20   | [evidência específica]           |
| Histórico de suporte   | X/20   | [evidência específica]           |
| NPS / Satisfação       | X/20   | [evidência ou "não coletado"]    |
| Histórico de expansão  | X/20   | [evidência específica]           |
|------------------------|--------|----------------------------------|
| TOTAL                  | X/100  |                                  |

PERFIL: [CRÍTICO / EM RISCO / ATENÇÃO / SAUDÁVEL / EXPANSÍVEL]

Sinais de alarme identificados:
  - [sinal 1]
  - [sinal 2]

Dimensão mais crítica: [dimensão com menor pontuação]
Causa provável: [diagnóstico em 2 linhas]

PLAYBOOK SELECIONADO: [nome do playbook]

PRÓXIMAS 3 AÇÕES
----------------
1. [Ação específica]
   Owner: [quem]
   Prazo: [data]
   Resultado esperado: [o que muda]

2. [Ação específica]
   Owner: [quem]
   Prazo: [data]
   Resultado esperado: [o que muda]

3. [Ação específica]
   Owner: [quem]
   Prazo: [data]
   Resultado esperado: [o que muda]

TEMPLATE DE MENSAGEM
--------------------
Canal: [WhatsApp / Email / LinkedIn]
Tom: [urgente / amigável / consultivo / expansão]

---
[texto da mensagem pronto para enviar, sem campos genéricos como {nome}]
---

META DE RESULTADO
-----------------
Se playbook executado com sucesso:
  Health score esperado em 30 dias: [X/100]
  Risco de churn: [redução de X% para Y%]
  Oportunidade identificada (se expansível): [descrição e valor estimado]
```

---

## Exemplos de Uso

**Exemplo 1 — Cliente em risco:**
> Dados: 8 meses de casa, uso caiu 60% no último mês, NPS 5 (detrator), 3 tickets sem resolução
> Health score: 18/100 (Crítico)
> Playbook: contato em 24h, reunião para ouvir sem agenda defensiva, comprometer-se com 1 solução concreta
> Template: "Olá [nome], sou a [CS]. Percebi que você não está usando [produto] com a frequência de antes e quero entender como posso ajudar. Você teria 20 minutos essa semana?"

**Exemplo 2 — Cliente expansível:**
> Dados: 14 meses de casa, usa 100% da capacidade, NPS 9, 0 tickets no trimestre, indicou 1 cliente
> Health score: 95/100 (Expansível)
> Playbook: mapear áreas adjacentes, apresentar upsell baseado em resultados, pedir indicação formal
> Template: "Incrível ver o que vocês estão construindo com [produto]. Queria fazer uma revisão de como maximizar ainda mais os resultados. Quando você teria 30 min para uma conversa estratégica?"

---

## Quality Gates

- Health score calculado com ao menos 3 das 5 dimensões com dados reais
- Perfil de risco justificado com evidências específicas, não suposições genéricas
- Playbook personalizado ao contexto do cliente — não cópia genérica do template
- Template de mensagem usa dados reais do cliente (tempo de casa, uso, contexto)
- Próximas 3 ações têm prazo, owner e métrica de resultado específica
- Clientes críticos têm resposta em 24-48h, nunca em mais de 72h
