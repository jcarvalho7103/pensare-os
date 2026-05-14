---
name: offer-creation
description: Cria oferta irresistível baseada no framework $100M Offers de Alex Hormozi
argument-hint: "icp: '{perfil}', dores: '[lista]', mecanismo: '{diferencial}', ticket_alvo: 'R$X'"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-produto
  - pensare-comercial
  - pensare-closer
handoff_in:
  required:
    context: "ICP definido, dores primárias mapeadas, mecanismo proprietário ou diferencial da solução e ticket alvo"
  optional:
    diagnostico: "Output do commercial-diagnosis se disponível"
    posicionamento: "Output do positioning-messaging se disponível"
    concorrentes: "Principais alternativas que o ICP considera"
handoff_out:
  produces:
    oferta_estruturada: "Documento completo com todos os componentes da oferta"
    pitch_3_linhas: "Versão compacta da oferta para uso em cold outreach ou apresentações"
    stack_de_valor: "Lista de todos os entregáveis com valor percebido estimado"
    garantia: "Garantia estruturada que reduz risco percebido"
quality_gates:
  - "Promessa conecta resultado específico + tempo + remoção da dor principal"
  - "Mecanismo é proprietário ou diferenciado — não genérico"
  - "Stack de valor totaliza pelo menos 3x o preço cobrado em valor percebido"
  - "Garantia é real e mensurável, não vaga"
  - "Urgência ou escassez é verdadeira, nunca fabricada"
---

# Offer Creation

Skill de criação de ofertas para o Pensare OS. Aplica o framework de Alex Hormozi ($100M Offers) para construir uma oferta irresistível com promessa forte, mecanismo claro, stack de valor, garantia e elementos de urgência — eliminando a comparação por preço.

## Quando Invocar

- Ao criar ou reformular uma oferta de produto ou serviço
- Quando a oferta atual não está convertendo (diagnóstico de oferta fraca)
- Para criar variações de oferta por segmento de ICP
- Antes de lançar uma nova campanha ou entrar em novo mercado

---

## Framework $100M Offers — Componentes Obrigatórios

### 1. Promessa (Dream Outcome)
**Formato:** [resultado desejado] + [em quanto tempo] + [sem a dor/objeção principal]

A promessa deve ser:
- Específica e verificável (não "crescer vendas", mas "fechar 20% mais negócios")
- Conectada ao resultado final que o cliente quer (não ao processo)
- Realista e alcançável com o mecanismo proposto

**Template:**
> "Ajudamos [ICP] a [resultado específico] em [prazo] sem [dor ou trade-off que eles temem]."

---

### 2. Mecanismo (Proprietary Vehicle)
O "como" da entrega. Deve soar diferente de qualquer coisa que o concorrente faz.

**Requisitos do mecanismo:**
- Tem nome próprio (ex: "Sistema de Atendimento Neural", "Método de Expansão Reversa")
- Explica o processo em 3-5 passos simples
- O cliente consegue repetir a explicação para outra pessoa
- Claramente diferente de "fazemos consultoria" ou "implementamos IA"

**Template de mecanismo em 3 passos:**
1. [Passo de diagnóstico/configuração]
2. [Passo de implementação/ação]
3. [Passo de resultado/otimização]

---

### 3. Stack de Valor (Value Stack)
Lista todos os entregáveis com valor percebido estimado. Objetivo: o total deve ser pelo menos 3x o preço.

**Como construir o stack:**
- Liste cada entregável separadamente (não agrupe)
- Atribua valor percebido de mercado a cada item (não custo de produção)
- Inclua bônus que resolvem objeções específicas
- Separe entregáveis core dos bônus

**Template:**
| Entregável | Valor de Mercado |
|---|---|
| [Core 1] | R$ X |
| [Core 2] | R$ X |
| [Core 3] | R$ X |
| Bônus 1: [resolve objeção] | R$ X |
| Bônus 2: [resolve objeção] | R$ X |
| **Total de Valor** | **R$ X** |
| **Seu Investimento** | **R$ X (Y% de desconto)** |

---

### 4. Garantia (Risk Reversal)
Transfere o risco do comprador para o vendedor. Remove a última barreira de decisão.

**Tipos de garantia (do mais ao menos agressivo):**
1. **Garantia de resultado:** "Se não atingir X em Y dias, devolvemos o dinheiro"
2. **Garantia de satisfação:** "Se não estiver satisfeito em 30 dias, sem perguntas"
3. **Garantia de trabalho:** "Continuamos trabalhando até atingir o resultado sem custo extra"
4. **Garantia de cláusula de performance:** "Só cobraremos a segunda parcela se atingir [métrica]"

**Regra:** a garantia deve ser assustadora para quem vende — se não assustar, não está boa.

---

### 5. Urgência e Escassez (Somente se for verdadeira)
Nunca fabricar urgência. Usar somente se houver razão real.

**Exemplos de urgência/escassez legítimas:**
- Vagas limitadas de onboarding (se o onboarding requer atenção dedicada)
- Preço de lançamento com prazo real
- Bônus que expiram (webinar gravado tem data, consultoria ao vivo tem agenda)
- Disponibilidade de calendário real

---

## Protocolo de Execução

### Passo 1 — Clareza de ICP e Dores
Confirme:
- Quem exatamente é o comprador (cargo, empresa, momento)
- Qual é a dor primária (resultado que eles perdem sem a solução)
- Qual é o maior medo/objeção na hora de comprar
- Qual resultado eles mais desejam

### Passo 2 — Construir a Promessa
Combine: resultado desejado + prazo específico + remoção do maior medo.
Teste: "Se um cliente lesse isso, ele saberia exatamente o que vai ganhar, quando e sem o quê?"

### Passo 3 — Nomear o Mecanismo
Crie um nome que soe proprietário. Liste os 3-5 passos. Garanta que é diferente do que o mercado diz.

### Passo 4 — Montar o Stack de Valor
Liste cada entregável. Atribua valor. Inclua bônus que resolvem as 2-3 maiores objeções.
Verifique: total de valor >= 3x o preço?

### Passo 5 — Formular a Garantia
Escolha o tipo de garantia. Deixe-a específica e mensurável.
Teste: "Essa garantia me assusta como vendedor? Se não, não está boa."

### Passo 6 — Escrever o Pitch de 3 Linhas
Linha 1: Para quem + resultado + prazo
Linha 2: Mecanismo + diferencial
Linha 3: Garantia + próximo passo

---

## Template de Output

```
OFFER CREATION DOCUMENT
========================
Produto/Serviço: [nome]
ICP: [perfil do comprador]
Data: [data]

PROMESSA
--------
"[Resultado específico] em [prazo] sem [dor/trade-off principal]."

MECANISMO: [Nome Proprietário]
-------------------------------
Como funciona:
1. [Fase 1 — diagnóstico/configuração]
2. [Fase 2 — implementação]
3. [Fase 3 — resultado/otimização]

STACK DE VALOR
--------------
Entregáveis core:
  ✓ [Entregável 1] ................................. R$ X
  ✓ [Entregável 2] ................................. R$ X
  ✓ [Entregável 3] ................................. R$ X

Bônus (resolve objeção: [qual objeção]):
  ✓ [Bônus 1] ...................................... R$ X
  ✓ [Bônus 2] ...................................... R$ X

Valor Total: R$ [X]
Seu Investimento: R$ [Y] ([Z]% do valor total)

GARANTIA
--------
"[Descrição da garantia — específica e mensurável]"
Tipo: [resultado / satisfação / trabalho / performance]

URGÊNCIA/ESCASSEZ (se aplicável)
---------------------------------
[Descrição ou "N/A — não aplicável neste momento"]

PITCH EM 3 LINHAS
-----------------
[Linha 1: Para quem + resultado + prazo]
[Linha 2: Mecanismo + diferencial]
[Linha 3: Garantia + próximo passo]

PREÇO
-----
Ticket: R$ [valor]
Forma de pagamento: [opções]
Justificativa de preço: [1-2 linhas conectando ao ROI]
```

---

## Exemplos de Uso

**Exemplo 1 — Agência de IA para vendas:**
> Promessa: "Ajudamos gestores comerciais a aumentar a taxa de conversão do funil em 25% nos primeiros 60 dias sem contratar mais SDRs."
> Mecanismo: Sistema de Qualificação Neural (diagnóstico automatizado + cadência personalizada + dashboard em tempo real)
> Garantia: Se não atingir 20% de melhoria em 60 dias, trabalhamos mais 30 dias sem custo adicional.

**Exemplo 2 — Produto SaaS:**
> Promessa: "Reduza 80% do tempo gasto em relatórios manuais em 2 semanas sem mudar sua stack atual."
> Mecanismo: Integração Zero-Fricção (conecta em 1 dia + automação configurada em 1 semana + treinamento em 2 horas)
> Garantia: Integração funcional em até 72h ou devolvemos a mensalidade do primeiro mês.

---

## Quality Gates

- Promessa conecta resultado específico + tempo + remoção da dor principal
- Mecanismo tem nome proprietário e é diferenciado do que concorrentes oferecem
- Stack de valor totaliza pelo menos 3x o preço cobrado em valor percebido
- Garantia é real e mensurável, com critério claro de acionamento
- Urgência ou escassez usada somente quando verdadeira
- Pitch em 3 linhas pode ser lido em menos de 15 segundos e faz sentido completo
