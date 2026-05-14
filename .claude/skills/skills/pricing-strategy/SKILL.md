---
name: pricing-strategy
description: Define estratégia de precificação para produtos/serviços de IA com 3 cenários e argumentário
argument-hint: "custo: 'R$X', icp: '{perfil}', valor_entregue: '{resultado}', ticket_desejado: 'R$X', concorrentes: '[lista]'"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-financeiro
  - pensare-produto
  - pensare-closer
handoff_in:
  required:
    context: "Custo de entrega do produto/serviço, ICP definido, valor entregue ao cliente e ticket alvo"
  optional:
    concorrentes: "Preços praticados por concorrentes diretos e alternativas"
    pesquisa_cliente: "Feedbacks de clientes sobre preço (aceitou, rejeitou, pediu desconto)"
    oferta: "Output do offer-creation com stack de valor"
    historico_vendas: "Dados históricos de conversão por faixa de preço se disponíveis"
handoff_out:
  produces:
    cenarios_pricing: "3 cenários (conservador/base/agressivo) com justificativa"
    modelo_recomendado: "Modelo de cobrança recomendado com racional"
    argumentario: "Roteiro para defender o preço na conversa de vendas"
    estrutura_desconto: "Política de descontos com limites e condições"
quality_gates:
  - "Todos os cenários cobrem pelo menos 2x o custo de entrega"
  - "Modelo de cobrança é justificado pelo comportamento do ICP, não só por conveniência interna"
  - "Argumentário conecta preço a valor entregue (não apenas defende o número)"
  - "Política de desconto tem limites claros e condições que criam troca de valor"
  - "Cenário base passa no teste: é o que você compraria se fosse o cliente?"
---

# Pricing Strategy

Skill de estratégia de precificação para o Pensare OS. Define o modelo de cobrança ideal, gera 3 cenários de preço (conservador, base e agressivo) com racional e constrói o argumentário de preço para uso em vendas.

## Quando Invocar

- Ao precificar um produto ou serviço novo
- Quando a taxa de conversão cai ao apresentar o preço (problema de precificação ou percepção de valor)
- Para revisar pricing existente com base em feedback de mercado
- Antes de entrar em novo segmento ou mercado com preços diferentes
- Quando o cliente sempre pede desconto (sinal de preço ou valor percebido mal calibrado)

---

## Modelos de Cobrança

### 1. Por Valor (Value-Based Pricing)
Preço baseado no valor entregue ao cliente, não no custo.

**Quando usar:** quando o resultado é claro, mensurável e significativamente maior que o preço.
**Cálculo:** precio = % do valor entregue (10-20% é padrão para serviços de IA)
**Exemplo:** automação que economiza R$20k/mês → pricing entre R$2k-4k/mês

### 2. Por Resultado (Performance-Based)
Cobrança atrelada ao resultado gerado. Parte fixa + variável.

**Quando usar:** quando há confiança alta no resultado e o cliente tem aversão a risco.
**Estrutura:** taxa de setup + % do resultado (ex: % das vendas geradas, % de custo reduzido)
**Risco:** difícil de rastrear e pode criar conflito de atribuição

### 3. Subscription (Recorrência Mensal/Anual)
Acesso à solução por período definido.

**Quando usar:** SaaS, ferramentas, assistentes, automações contínuas.
**Vantagem:** previsibilidade de receita, LTV alto.
**Variações:** mensal (maior churn, menor barreira), anual (menor churn, maior commit)

### 4. One-Time
Pagamento único por entrega específica.

**Quando usar:** projetos, implementações, consultorias pontuais.
**Vantagem:** simples, baixa barreira de entrada.
**Desvantagem:** sem receita recorrente, exige aquisição constante.

### 5. Retainer
Mensalidade fixa por disponibilidade/capacidade, independente do volume.

**Quando usar:** agências, consultores, CS dedicado.
**Vantagem:** previsibilidade para ambos os lados.

### 6. Performance-Based (Puro)
100% baseado em resultado. Sem taxa fixa.

**Quando usar:** somente quando o resultado é 100% rastreável e atribuível.
**Risco alto:** difícil de implementar e defender.

---

## Frameworks de Precificação

### Value-Based Pricing — Cálculo Direto

```
1. Calcule o valor entregue ao cliente em R$/mês
   Valor = (horas economizadas × custo/hora) + (receita gerada) + (custo evitado)

2. Defina a % de captura de valor
   Conservador: 8-12%
   Base: 12-18%
   Agressivo: 18-25%

3. Preço = Valor × % de captura
```

### Van Westendorp (Price Sensitivity)

4 perguntas para descobrir o range psicológico de preço:

1. "Abaixo de qual preço você acharia que essa solução é de baixa qualidade?" → **Muito barato**
2. "Acima de qual preço você acharia que está caro demais para considerar?" → **Muito caro**
3. "Acima de qual preço você acharia caro, mas ainda consideraria comprar?" → **Caro mas aceitável**
4. "Abaixo de qual preço você acharia que é um bom custo-benefício?" → **Barato aceitável**

O **Preço Ótimo** fica no cruzamento de "caro mas aceitável" e "barato aceitável".
O **Range Aceitável** fica entre "muito barato" e "muito caro".

### Preço Âncora (Anchoring)

Apresentar um preço alto primeiro para fazer o preço real parecer razoável.
Sempre apresentar 3 opções: Basic / Standard / Premium.
A maioria escolhe o meio ou é guiada para o plano desejado pelo vendedor.

---

## Protocolo de Execução

### Passo 1 — Calcular Custo Real de Entrega
Liste todos os custos:
- Custo de ferramentas/APIs/infraestrutura
- Horas de setup e onboarding
- Horas de manutenção mensal
- Custo de suporte
- Overhead (impostos, plataforma, comissão)
**Custo total = mínimo absoluto. Preço < custo = suicídio financeiro.**

### Passo 2 — Mapear Valor Entregue ao ICP
Para o ICP definido, calcule:
- Horas economizadas × custo/hora do profissional
- Receita adicional gerada (se mensurável)
- Custo evitado (contratações, retrabalho, erros)
**Valor total = o que o cliente ganha/economiza com a solução**

### Passo 3 — Verificar Referência Competitiva
O que o cliente pagaria pela melhor alternativa?
- Contratar um humano para fazer o mesmo
- Solução concorrente
- Fazer internamente
**Âncora competitiva = o que define percepção de caro ou barato**

### Passo 4 — Gerar os 3 Cenários

**Cenário Conservador:** preço mais próximo do custo + margem mínima (40-60%). Menor risco de rejeição, menor margem.

**Cenário Base:** preço alinhado ao valor entregue com captura moderada (12-18%). Equilíbrio entre margem e conversão.

**Cenário Agressivo:** preço no teto do range aceitável, captura alta de valor (20-25%). Alta margem, menor volume, exige oferta e posicionamento fortes.

### Passo 5 — Escolher e Recomendar
Recomendar o cenário base como ponto de partida. Justificar com:
- Alinhamento ao valor entregue
- Comparação com alternativas
- Margem saudável
- Conversão esperada

### Passo 6 — Construir Argumentário de Preço
Roteiro para a conversa de vendas quando o preço é apresentado.

### Passo 7 — Definir Política de Desconto
Limites e condições para desconto. Nunca desconto sem troca de valor.

---

## Template de Output

```
PRICING STRATEGY DOCUMENT
===========================
Produto/Serviço: [nome]
ICP: [perfil]
Data: [data]

ANÁLISE DE CUSTO E VALOR
-------------------------
Custo de entrega (mensal/por projeto): R$ [X]
  - Ferramentas/infra: R$ [X]
  - Horas de trabalho: R$ [X]
  - Overhead estimado: R$ [X]

Valor entregue ao ICP: R$ [X]/mês
  - [Componente 1]: R$ [X]
  - [Componente 2]: R$ [X]
  - [Componente 3]: R$ [X]

Melhor alternativa do cliente: [o quê] por R$ [X]

MODELOS DE COBRANÇA AVALIADOS
-------------------------------
[X] Subscription mensal  — adequação: [alta/média/baixa]
[ ] One-time             — adequação: [alta/média/baixa]
[ ] Retainer             — adequação: [alta/média/baixa]
[ ] Performance-based    — adequação: [alta/média/baixa]

Modelo recomendado: [modelo]
Justificativa: [2-3 linhas]

3 CENÁRIOS DE PRICING
---------------------
CONSERVADOR
  Preço: R$ [X]/[mês|projeto]
  Margem sobre custo: [X]%
  Captura de valor: [X]%
  Conversão esperada: [alta/média]
  Quando usar: [contexto]

BASE (RECOMENDADO)
  Preço: R$ [X]/[mês|projeto]
  Margem sobre custo: [X]%
  Captura de valor: [X]%
  Conversão esperada: [média]
  Quando usar: [contexto]

AGRESSIVO
  Preço: R$ [X]/[mês|projeto]
  Margem sobre custo: [X]%
  Captura de valor: [X]%
  Conversão esperada: [baixa/seletiva]
  Quando usar: [contexto]

ESTRUTURA DE PLANOS (se aplicável)
-----------------------------------
| Plano    | Preço    | O que inclui         | Para quem    |
|----------|----------|----------------------|--------------|
| Basic    | R$ X/mês | [entregáveis básicos] | [perfil]     |
| Standard | R$ X/mês | [entregáveis std]     | [perfil]     |
| Premium  | R$ X/mês | [entregáveis premium] | [perfil]     |

ARGUMENTÁRIO DE PREÇO
---------------------
Quando o cliente perguntar o preço:
1. Apresentar primeiro o valor (não o preço): "[o que entregamos]"
2. Ancorar no custo da alternativa: "Isso equivale a [comparação]"
3. Apresentar o preço como investimento: "O investimento é R$ X/mês"
4. Conectar ao ROI: "Considerando que isso gera/economiza R$ X, o payback é [prazo]"
5. Facilitar a decisão: "[próximo passo concreto]"

Resposta para "está caro":
"[roteiro específico para este produto/ICP]"

POLÍTICA DE DESCONTO
--------------------
Desconto máximo sem aprovação: [X]%
Desconto máximo com aprovação: [X]%
Condições para desconto:
  - Pagamento anual antecipado → até [X]% de desconto
  - Indicação de cliente → [benefício]
  - Expansão de escopo → negociação de pacote
  - Piloto para prova de valor → [condições]

Nunca dar desconto sem: [o que pedir em troca]
```

---

## Exemplos de Uso

**Exemplo 1 — Agência de IA para automação de CS:**
> Custo: R$3.500/mês (infra + horas). Valor entregue: R$25k (3 atendentes × R$8k). Alternativa: contratar 3 atendentes.
> Cenário base: R$5.500/mês (22% de captura de valor, margem 57%). Modelo: subscription.
> Argumentário: "3 atendentes custam R$24k. Nossa solução cobre a mesma demanda por R$5.500."

**Exemplo 2 — SaaS de qualificação de leads:**
> Custo: R$800/mês (infra). Valor entregue: ~R$15k (SDR economizado). Alternativa: contratar SDR.
> Cenário conservador: R$1.200 | Base: R$2.500 | Agressivo: R$4.000/mês.
> Modelo: subscription anual com desconto de 2 meses.

---

## Quality Gates

- Todos os cenários cobrem pelo menos 2x o custo de entrega
- Modelo de cobrança justificado pelo comportamento do ICP, não por conveniência interna
- Argumentário conecta preço a valor entregue (não apenas defende o número)
- Política de desconto tem limites claros e condições que criam troca de valor
- Cenário base passa no teste: é o que você venderia para o seu melhor cliente?
- Nenhum preço definido sem custo de entrega calculado primeiro
