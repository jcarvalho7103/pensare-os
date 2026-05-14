# Skills Guide — Pensare OS

> Skills são **unidades de inteligência reutilizáveis** — frameworks consolidados que múltiplos agentes podem instanciar com contexto próprio. Vivem em `.claude/skills/skills/{nome}/SKILL.md`.

---

## Por que skills existem

Sem skills, cada agente teria que carregar a metodologia BANT no próprio prompt — duplicação e inconsistência. Com skills:

- **Reutilização**: 1 skill, N agentes
- **Manutenção centralizada**: melhorar a skill melhora todos os agentes
- **Composabilidade**: agente pode usar 2-3 skills em sequência
- **Auditabilidade**: o framework usado fica explícito

---

## As 10 Skills

| Skill | Framework | Usada por |
|-------|-----------|-----------|
| `lead-qualification` | BANT score 0–100 + ICP fit | SDR, CS |
| `commercial-diagnosis` | D.E.A.L. lite + SPIN | Closer, Estratégia |
| `objection-handling` | Feel-Felt-Found · 10 objeções comuns | Closer |
| `offer-creation` | $100M Offers (Hormozi) | Produto, Closer |
| `positioning-messaging` | April Dunford + StoryBrand | Estratégia, Copy |
| `creative-hook` | 6 hook types · 3 concepts + 2 scripts | Criativos, Copy |
| `campaign-optimization` | 3-layer diagnosis (creative/LP/oferta) | Tráfego, Growth |
| `funnel-diagnosis` | 5 stages + benchmarks setoriais | Inteligência |
| `pricing-strategy` | Value-Based + Van Westendorp + 3 cenários | Financeiro, Produto |
| `churn-prevention` | Health score 5D + 4 playbooks | CS |

---

## Anatomia de uma Skill

Cada skill é um diretório:

```
.claude/skills/skills/lead-qualification/
└── SKILL.md
```

O `SKILL.md` tem frontmatter padrão:

```yaml
---
name: lead-qualification
description: "Qualificar lead contra ICP usando BANT score 0–100"
framework: "BANT + ICP fit dimensions"
inputs:
  - lead_data: "informações disponíveis sobre o lead"
  - icp_definition: "ICP definido em _contexto/empresa.md"
outputs:
  - bant_score: "0–100 com breakdown"
  - icp_fit: "alto/médio/baixo com justificativa por dimensão"
  - recommendation: "agendar-diagnostico | nutrir | desqualificar"
  - first_contact_message: "se qualificado"
used_by:
  - /pensare-sdr
  - /pensare-cs
  - /pensare-comercial
---

# Lead Qualification

[corpo com instruções, exemplos, dos & don'ts]
```

---

## Detalhamento das Skills

### 1. `lead-qualification` — BANT 0–100

**Quando usar**: novo lead chegou, precisamos saber se é SQL/MQL/desqualificado.

**Dimensões**:
- **Budget** (0–25): capacidade de investir
- **Authority** (0–25): tem autonomia de decisão?
- **Need** (0–25): dor real e mensurável?
- **Timeline** (0–25): urgência declarada ou inferida

**Classificação**:
- 75–100 → **SQL** → encaminhar para Closer
- 50–74 → **MQL** → nutrição
- 0–49 → **Desqualificado** → encerrar com elegância

**Plus**: avaliação de ICP fit (segmento, tamanho, estágio).

**Output esperado**:
```
Score: 82/100
- Budget: 22/25 (R$ 80k/mês faturamento)
- Authority: 25/25 (founder)
- Need: 20/25 (caos comercial declarado)
- Timeline: 15/25 (sem urgência explícita)

ICP fit: ALTO (agência B2B, 6 pessoas, validada)

Recomendação: agendar diagnóstico com Closer
Próxima ação: mensagem personalizada (rascunho abaixo)
```

### 2. `commercial-diagnosis` — D.E.A.L. lite + SPIN

**Quando usar**: prospect qualificado, hora de descobrir a dor real antes de propor.

**Estrutura**:
- **D**escoberta — fatos da operação atual
- **E**xploração — onde dói e por quê
- **A**mplificação — custo de não resolver
- **L**ançamento — só agora apresentar oferta

**Combinado com SPIN**:
- **S**ituation: como está hoje?
- **P**roblem: o que não funciona?
- **I**mplication: o que isso causa?
- **N**eed-Payoff: o que mudaria com solução?

**Regra**: nunca propor antes de completar o D + E + A.

### 3. `objection-handling` — Feel-Felt-Found

**Quando usar**: prospect levantou objeção ou hesita no fechamento.

**Estrutura Feel-Felt-Found**:
- **Feel** (entendo como se sente)
- **Felt** (outros clientes se sentiram igual)
- **Found** (o que eles descobriram)

**10 objeções pré-mapeadas**:
1. "Achei caro"
2. "Preciso pensar"
3. "Preciso falar com sócio"
4. "Já temos algo parecido"
5. "Não é o momento"
6. "Não tenho equipe pra absorver"
7. "Como sei que funciona?"
8. "Já tentei IA, não funcionou"
9. "Posso fazer internamente"
10. "Quanto tempo até resultado?"

Cada uma com respostas Feel-Felt-Found prontas para o ICP do AI Systemizer.

### 4. `offer-creation` — $100M Offers (Hormozi)

**Quando usar**: criar nova oferta ou ajustar a existente.

**Value Equation** (Hormozi):
```
Valor = (Dream Outcome × Perceived Likelihood)
        ────────────────────────────────────
        (Time Delay × Effort & Sacrifice)
```

**Para maximizar valor**:
- **Aumente** Dream Outcome (transformação clara)
- **Aumente** Perceived Likelihood (prova, garantia)
- **Reduza** Time Delay (resultado mais rápido)
- **Reduza** Effort & Sacrifice (mais easy)

**Componentes da Grand Slam Offer**:
1. Mecanismo único (o "como" diferenciado)
2. Bônus que removem objeções
3. Garantia que reduz risco
4. Escassez/urgência (quando legítima)
5. Stack visual de valor

### 5. `positioning-messaging` — April Dunford + StoryBrand

**Quando usar**: definir/refinar posicionamento, criar mensagem central, atualizar landing page.

**Framework April Dunford (5 elementos)**:
1. Alternativas competitivas (o que cliente faria se nós não existíssemos?)
2. Atributos únicos (o que só nós temos)
3. Valor (o que esses atributos permitem)
4. Características do cliente que valoriza esse valor
5. Categoria de mercado

**Plus StoryBrand**:
- Cliente é o herói (não a empresa)
- Empresa é o guia
- Plano de 3 passos
- Convite à ação clara

### 6. `creative-hook` — 6 hook types

**Quando usar**: criar abertura de vídeo, post, anúncio que prende atenção em 3s.

**6 tipos de hook**:
1. **Contrarian** — "Pare de fazer X. Aqui está o porquê."
2. **Curiosity Gap** — "A maioria dos founders comete este erro..."
3. **Stat Shocker** — "73% dos negócios B2B falham por..."
4. **Story Open** — "Em 2024, eu perdi um cliente porque..."
5. **Question Hook** — "Por que sua agência fatura R$ 100k mas você não para?"
6. **Promise Hook** — "Vou te mostrar como sair da operação em 90 dias."

**Output da skill**:
- 3 conceitos diferentes para o mesmo brief
- 2 roteiros de vídeo (30s e 60s)
- Variantes para LinkedIn vs Instagram

### 7. `campaign-optimization` — 3-layer diagnosis

**Quando usar**: CPL subiu, ROAS caiu, campanha ficou "cansada".

**As 3 camadas**:

1. **Creative** (CTR, hook, fadiga)
   - CTR está saudável? (≥1.5%)
   - Quantos dias o criativo está rodando?
   - Frequência de impressão?

2. **Landing Page** (LP conversion, fricção)
   - Taxa de conversão da LP?
   - Tempo médio na página?
   - Mobile vs desktop performance?

3. **Oferta** (clareza, fit com ICP)
   - O lead chegou à LP esperando o quê?
   - A oferta cumpre essa expectativa?
   - O ICP-alvo da campanha está certo?

**Regra**: nunca otimizar 2 camadas ao mesmo tempo — perde causalidade.

### 8. `funnel-diagnosis` — 5 stages + benchmarks

**Quando usar**: conversão geral caiu, não está claro onde está o vazamento.

**5 etapas do funil**:
1. Lead → MQL
2. MQL → SQL
3. SQL → Proposta
4. Proposta → Fechamento
5. Fechamento → Cliente ativo

**Benchmarks consultoria B2B alto-ticket**:

| Etapa | Saudável | Atenção | Crítico |
|-------|----------|---------|---------|
| Lead → MQL | >60% | 40–60% | <40% |
| MQL → SQL | >30% | 15–30% | <15% |
| SQL → Proposta | >70% | 50–70% | <50% |
| Proposta → Cliente | >40% | 20–40% | <20% |

A skill aplica os benchmarks e identifica **onde** está o vazamento.

### 9. `pricing-strategy` — Value-Based + Van Westendorp

**Quando usar**: definir preço de oferta nova, revisar preço atual, lidar com objeção de preço.

**Value-Based Pricing**:
- Preço deve ser 10–20% do valor entregue
- Se AI Systemizer libera 20h/semana do founder = R$ 30k/mês de valor → preço R$ 3–6k é "barato"

**Van Westendorp** (4 perguntas ao mercado):
1. Em qual preço você acharia muito caro?
2. Em qual preço você começaria a achar caro mas pensaria?
3. Em qual preço seria uma barganha?
4. Em qual preço seria barato demais (suspeito)?

**Output**: 3 cenários de preço (conservador / target / agressivo) com racional.

### 10. `churn-prevention` — Health score 5D + playbooks

**Quando usar**: avaliar saúde de cliente ativo, prevenir churn.

**Health Score (5 dimensões, 0–20 cada)**:
1. **Engajamento** — frequência de interação
2. **Adoção** — uso das features/processos entregues
3. **Resultado** — está atingindo o ROI prometido?
4. **Relacionamento** — sentimento nas conversas
5. **Pagamento** — em dia? expansão? downgrade?

**Classificação**:
- 80–100: Saudável
- 60–79: Atenção
- 40–59: Risco
- <40: Crítico

**4 Playbooks**:
1. **Reignite** — para "atenção": touchpoint de reengajamento
2. **Realign** — para "risco": reunião de realinhamento + plano
3. **Rescue** — para "crítico": intervenção da liderança + concessões
4. **Expand** — para "saudável": oportunidade de expansion revenue

---

## Como Skills são invocadas

### Forma direta — agente pede skill
```
/pensare-sdr qualifique este lead aplicando a skill lead-qualification:
[dados do lead]
```

### Forma automática — agente decide
Cada agente tem `skills_used` no frontmatter. Quando recebe uma tarefa, ele escolhe a skill apropriada e a aplica.

### Forma composta — múltiplas skills em sequência
```
/pensare-closer este prospect levantou objeção de preço.
1. Aplique objection-handling (feel-felt-found)
2. Reforce com pricing-strategy (value-based framing)
3. Proponha próximo passo
```

---

## Anti-patterns

❌ **Skill como agente** — skill não é agente. Skill não tem opinião, só método.

❌ **Skill sem framework** — toda skill deve referenciar um framework consolidado (BANT, SPIN, $100M Offers, etc.)

❌ **Skill genérica** — "improve-conversion" é vago demais. Skills devem ser específicas (e.g. `campaign-optimization` para CPL/ROAS, `funnel-diagnosis` para taxas de conversão).

❌ **Duplicação entre skills** — se 2 skills fazem quase a mesma coisa, consolide ou faça uma chamar a outra.

❌ **Skill que exige contexto que não tem** — toda skill declara seus `inputs` necessários.

---

## Como criar uma skill nova

### Quando criar
- Você notou que está repetindo o mesmo framework em 2+ agentes
- Você quer codificar uma metodologia consolidada do mercado
- Você quer extrair lógica do prompt do agente para reuso

### Como criar

```bash
mkdir -p .claude/skills/skills/{nome-da-skill}
```

Crie `SKILL.md`:

```markdown
---
name: nome-da-skill
description: "1 frase do que faz"
framework: "Nome do framework consolidado"
inputs:
  - <input_1>: "descrição"
  - <input_2>: "descrição"
outputs:
  - <output_1>: "formato esperado"
used_by:
  - /pensare-<agente>
---

# Nome da Skill

## Quando usar
[1 parágrafo]

## Framework
[detalhe o framework com estrutura/passos]

## Output esperado
[exemplo concreto]

## Anti-patterns
- ❌ ...
- ❌ ...
```

### Após criar

1. Adicione referência em `AGENTS.md` (`skills_used` do agente)
2. Adicione no CLAUDE.md (tabela de skills)
3. Adicione em README.md (tabela de skills)
4. Teste invocando via agente e revisando output

---

## Cheatsheet: qual skill usar?

| Situação | Skill |
|----------|-------|
| Lead novo chegou | `lead-qualification` |
| Hora de propor venda | `commercial-diagnosis` (antes!) |
| Prospect com objeção | `objection-handling` |
| Criar/refazer oferta | `offer-creation` |
| Definir posicionamento | `positioning-messaging` |
| Criativo cansado | `creative-hook` |
| CPL/ROAS travado | `campaign-optimization` |
| Conversão caiu, não sei onde | `funnel-diagnosis` |
| Definir/revisar preço | `pricing-strategy` |
| Cliente está OK? | `churn-prevention` |

---

*Skills são imutáveis durante uma sessão — mudar uma skill é decisão de arquitetura, não de execução.*
