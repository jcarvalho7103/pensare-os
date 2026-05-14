---
name: commercial-diagnosis
description: Diagnóstico comercial de 30min usando D.E.A.L. lite + SPIN para mapear dores e personalizar proposta
argument-hint: "cliente: {contexto, setor, cargo_decisor, produto_sendo_vendido}"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-sdr
  - pensare-closer
  - pensare-cs
handoff_in:
  required:
    context: "Contexto do cliente: empresa, setor, cargo do decisor e produto/solução sendo apresentado"
  optional:
    qualificacao: "Output do lead-qualification se já executado"
    historico: "Histórico de interações anteriores com o cliente"
    proposta_anterior: "Proposta ou conversa prévia se houver reengajamento"
handoff_out:
  produces:
    mapa_dores: "Lista priorizada de dores identificadas (primária + secundárias)"
    budget_estimado: "Range de budget com confiança (alta/média/baixa)"
    proximo_passo: "Próximo passo acordado com data e responsável"
    proposta_de_valor: "Proposta de valor personalizada ao contexto do cliente"
    roteiro_executado: "Perguntas feitas e respostas coletadas durante o diagnóstico"
quality_gates:
  - "Ao menos 1 dor primária identificada com impacto quantificado (R$, tempo, %)."
  - "Budget explorado — mesmo que estimado, não pode ficar em branco"
  - "Próximo passo tem data e responsável definidos"
  - "Proposta de valor usa linguagem do próprio cliente, não jargão da empresa"
---

# Commercial Diagnosis

Skill de diagnóstico comercial para o Pensare OS. Conduz uma conversa estruturada de 30 minutos usando o framework D.E.A.L. lite combinado com perguntas SPIN para mapear dores, estimar budget e construir uma proposta de valor personalizada antes do fechamento.

## Quando Invocar

- Após a qualificação do lead (tier hot ou warm elevado)
- Na primeira reunião de discovery com um prospect
- Em reuniões de reengajamento de oportunidades paradas
- Quando o CS precisa entender fundo do cliente para expansão ou renovação

---

## Framework D.E.A.L. Lite

O diagnóstico está estruturado em 4 fases conversacionais:

| Fase | Objetivo | Duração |
|---|---|---|
| **D** — Descoberta | Entender o contexto atual | 8 min |
| **E** — Exploração | Identificar dores e problemas | 10 min |
| **A** — Aprofundamento | Quantificar impacto e urgência | 8 min |
| **L** — Link | Conectar dor à solução | 4 min |

---

## Protocolo de Execução

### Fase D — Descoberta (Perguntas de Situação SPIN)

Objetivo: mapear o estado atual sem julgamentos. Ouvir mais, falar menos.

**Perguntas-guia:**
1. "Me conta um pouco sobre como funciona hoje o seu processo de [área relevante — vendas, marketing, operações]?"
2. "Qual é o tamanho do seu time que cuida disso hoje?"
3. "Quais ferramentas vocês usam atualmente para essa parte?"
4. "Como você mensura o sucesso nessa área hoje?"
5. "Quem mais está envolvido nessa decisão além de você?"

**O que capturar:**
- Estrutura atual do processo
- Ferramentas em uso (concorrentes potenciais)
- Tamanho da operação (volume, time, escala)
- Stakeholders envolvidos

---

### Fase E — Exploração (Perguntas de Problema SPIN)

Objetivo: trazer à superfície as dores que o cliente já sente mas talvez não tenha articulado.

**Perguntas-guia:**
1. "Quais são as maiores dificuldades que você enfrenta com o processo atual?"
2. "O que trava mais o seu crescimento hoje nessa área?"
3. "Se você pudesse mudar uma coisa no jeito que funciona hoje, o que seria?"
4. "Tem alguma coisa que você faz hoje no manual que claramente poderia ser automatizado?"
5. "O que o seu time reclama mais nessa operação?"

**O que capturar:**
- Dores declaradas (em palavras do próprio cliente)
- Problemas percebidos vs. reais
- Nível de consciência do problema (cliente já sabe que tem um problema?)

---

### Fase A — Aprofundamento (Perguntas de Implicação e Necessidade SPIN)

Objetivo: quantificar o impacto das dores e criar urgência genuína.

**Perguntas de Implicação:**
1. "O que acontece se esse problema não for resolvido nos próximos 6 meses?"
2. "Qual é o custo aproximado desse problema pra você hoje — em tempo, dinheiro ou oportunidade perdida?"
3. "Como isso afeta outras áreas da empresa além de [área mencionada]?"
4. "Vocês já tentaram resolver isso antes? O que funcionou ou não funcionou?"

**Perguntas de Necessidade:**
1. "Se você conseguisse [resultado desejado], o que isso mudaria no seu dia a dia?"
2. "Qual resultado seria considerado um sucesso pra você em 90 dias?"
3. "Isso é algo que você precisa resolver agora ou é mais algo que está no radar pra futuro?"

**O que capturar:**
- Impacto em R$ ou % (mesmo estimado)
- Urgência real (não urgência educada)
- Critérios de sucesso do cliente
- Tentativas anteriores de resolução

---

### Fase L — Link (Conectar dor à solução)

Objetivo: apresentar a proposta de valor de forma cirúrgica, usando as palavras do cliente.

**Estrutura do Link:**
1. Resumir as dores identificadas em voz alta: "Então se eu entendi bem, o seu maior desafio é [dor primária em palavras do cliente]..."
2. Confirmar: "Está correto? Tem mais alguma coisa que eu deixei de mencionar?"
3. Conectar: "Exatamente esse problema é o que nós resolvemos para [exemplo de cliente similar]. O que a gente faz é [mecanismo] e o resultado típico é [resultado com número se possível]."
4. Propor próximo passo: "Faz sentido a gente avançar para [proposta/demo/contrato]? Quando você estaria disponível para [próximo passo]?"

---

## Budget Exploration (Paralelo à Fase A)

Explore budget sem constrangimento. Use uma dessas abordagens conforme o perfil do cliente:

**Direta (para decisores diretos):**
> "Para a gente não perder o seu tempo nem o meu, qual é a faixa de investimento que vocês têm disponível para resolver esse problema?"

**Âncora (para clientes mais conservadores):**
> "Projetos como esse costumam variar de R$X a R$Y dependendo do escopo. Você consegue me dar uma ideia de onde estaria o orçamento de vocês nessa faixa?"

**Custo da inação (para clientes sem budget definido):**
> "Se esse problema custa [valor estimado da dor] por mês pra você, quanto faria sentido investir para resolver de uma vez?"

---

## Template de Output

```
COMMERCIAL DIAGNOSIS REPORT
============================
Cliente: [Nome] | [Cargo] @ [Empresa] | [Setor]
Data: [data] | Duração: [X min]
Conduzido por: [agente/pessoa]

CONTEXTO ATUAL (Descoberta)
---------------------------
Processo atual: [resumo em 2-3 linhas]
Ferramentas em uso: [lista]
Tamanho da operação: [time, volume, escala]
Outros stakeholders: [quem mais decide]

MAPA DE DORES (Exploração + Aprofundamento)
-------------------------------------------
Dor Primária: [dor em palavras do cliente]
  Impacto estimado: [R$ / horas / % mencionado pelo cliente]
  Urgência: [imediata / 1-3 meses / sem urgência]

Dores Secundárias:
  1. [dor secundária]
  2. [dor secundária]
  3. [dor secundária]

BUDGET
------
Budget declarado: [valor ou "não declarado"]
Budget estimado: [range]
Confiança: [alta / média / baixa]
Justificativa: [como chegou nessa estimativa]

CRITÉRIOS DE SUCESSO
--------------------
"[citação direta do cliente sobre o que seria sucesso]"

PROPOSTA DE VALOR PERSONALIZADA
--------------------------------
"Para [empresa], que enfrenta [dor primária em palavras deles], nossa solução entrega [resultado] em [tempo], sem [objeção principal]. Já fizemos isso para [referência de setor similar]."

PRÓXIMO PASSO
-------------
Ação: [o que acontece agora]
Responsável: [quem faz]
Data/Prazo: [quando]
Acordado em reunião: [sim / não confirmado]

NOTAS ADICIONAIS
----------------
[Observações sobre comportamento, objeções levantadas, concorrentes mencionados]
```

---

## Exemplos de Uso

**Exemplo 1 — SaaS B2B:**
> Input: CEO de empresa de 80 funcionários no setor de logística, produto sendo vendido é automação de atendimento via IA
> Output: Dor primária = "time de CS sobrecarregado, 300 tickets/mês no manual" | Budget ~R$5k/mês | Próximo passo = proposta em 48h

**Exemplo 2 — Reengajamento:**
> Input: CMO que conversou há 3 meses e não fechou, novo contexto = empresa cresceu e o problema ficou maior
> Output: Nova dor identificada (escala) + budget revisado + urgência alta | Próximo passo = demo acelerada da solução

---

## Quality Gates

- Ao menos 1 dor primária identificada com impacto quantificado (R$, tempo ou %)
- Budget explorado — mesmo que estimado, não pode ficar em branco no relatório
- Próximo passo tem data e responsável definidos
- Proposta de valor usa linguagem do próprio cliente, não jargão da empresa
- Relatório gerado imediatamente após a reunião (máximo 15 min depois)
