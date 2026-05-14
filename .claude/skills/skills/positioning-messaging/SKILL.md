---
name: positioning-messaging
description: Define posicionamento e mensagem mestre usando April Dunford + StoryBrand, com variações por canal
argument-hint: "produto: '{descrição}', icp: '{perfil}', contexto_competitivo: '{alternativas}'"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-copy
  - pensare-criativos
  - pensare-estrategia
  - pensare-produto
handoff_in:
  required:
    context: "Produto ou serviço a ser posicionado, ICP definido e principais alternativas que o cliente considera"
  optional:
    oferta: "Output do offer-creation se disponível"
    diagnostico: "Insights de dores do commercial-diagnosis"
    pesquisa_cliente: "Citações reais de clientes sobre o produto"
handoff_out:
  produces:
    mensagem_mestre: "Declaração de posicionamento completa com todos os componentes"
    variacoes_canal: "Adaptações por canal: headline, tagline, elevator pitch, cold email"
    storia_brand_map: "Mapa do cliente como herói no framework StoryBrand"
    diferencial_unico: "Unique Value Proposition em 1 frase"
quality_gates:
  - "Posicionamento é específico para um segmento — não serve para todo mundo"
  - "Diferencial único não é genérico (não pode ser 'qualidade' ou 'atendimento')"
  - "Mensagem mestre passa no teste: um concorrente conseguiria afirmar o mesmo? Se sim, refazer"
  - "Variações por canal adaptam tom sem perder o posicionamento central"
  - "Elevator pitch dura no máximo 30 segundos quando lido em voz alta"
---

# Positioning & Messaging

Skill de posicionamento e mensagem para o Pensare OS. Constrói o framework de mensagem mestre usando April Dunford (Obviously Awesome) para o posicionamento competitivo e Donald Miller (StoryBrand) para a narrativa, gerando variações prontas para cada canal.

## Quando Invocar

- Ao lançar um novo produto ou serviço
- Quando o produto existe mas a mensagem não está convertendo
- Para alinhar comunicação entre times (vendas, marketing, conteúdo)
- Antes de criar qualquer campanha, landing page ou deck de vendas
- Quando há repositionamento estratégico

---

## Framework April Dunford — Obviously Awesome

### Os 5 Componentes do Posicionamento

#### 1. Clientes (Competitive Alternatives)
Quem se beneficia mais do seu produto. Não "todo mundo" — o segmento onde você ganha.

**Perguntas:**
- Quais clientes existentes têm o maior ROI com o produto?
- Qual cargo, setor e momento (trigger) define quem compra?
- Quem você NÃO deveria vender?

#### 2. Atributos Únicos (Unique Attributes)
O que você tem ou faz que nenhum concorrente relevante tem ou faz.

**Regra:** se o concorrente pode afirmar o mesmo, não é único.
- Tecnologia proprietária
- Metodologia exclusiva
- Dados que só você tem
- Integração que só você oferece
- Time ou experiência que não existe em outro lugar

#### 3. Valor (Value Enablers)
O valor que esses atributos únicos entregam. O "então" da frase "temos X, então entregamos Y".

**Traduzir atributos em valor de negócio:**
- Atributo: "IA treinada com dados do setor"
- Valor: "Redução de 70% no tempo de qualificação de leads"

#### 4. Categoria (Market Category)
O contexto mental onde você quer que o cliente te avalie. A categoria define os concorrentes, o benchmark e as expectativas.

**Estratégias de categoria:**
- **Categoria existente:** entrar onde o mercado já existe, mas com diferencial claro
- **Subcategoria:** "IA para [setor específico]" — reduz competição
- **Nova categoria:** criar nova — alta recompensa, alto risco e custo de educação

#### 5. Tendências Relevantes (Relevant Trends)
Ventos favoráveis que tornam o produto urgente agora. O "por que agora" do posicionamento.

---

## Framework StoryBrand — O Cliente é o Herói

### Os 7 Elementos da Narrativa

1. **Herói:** o cliente (não a empresa)
2. **Problema:** o vilão externo, interno e filosófico
3. **Guia:** a empresa como Yoda, não como Luke
4. **Plano:** como o guia resolve o problema (3 passos simples)
5. **Call to Action:** o que fazer agora
6. **Fracasso:** o que acontece se não agir
7. **Sucesso:** a vida do cliente depois da solução

**Princípio central:** a empresa não é o herói. A empresa é o guia que tem a ferramenta que o herói precisa.

---

## Protocolo de Execução

### Passo 1 — Mapeamento Competitivo
Liste as alternativas reais que o ICP considera (não apenas concorrentes diretos — inclui "fazer manualmente", "contratar pessoa" e "não fazer nada").

Para cada alternativa: o que o cliente valoriza nela? O que frustra?

### Passo 2 — Identificar Atributos Únicos
Liste 3-5 coisas que só você tem. Filtre: algum concorrente consegue dizer o mesmo?
Mantenha somente o que passa no filtro.

### Passo 3 — Traduzir em Valor
Para cada atributo único: "então o cliente consegue..."
Priorize o valor que o ICP mais se importa.

### Passo 4 — Escolher Categoria
Onde você ganha na comparação? Qual categoria coloca seus atributos em vantagem?

### Passo 5 — Escrever Declaração de Posicionamento
Use o template:
> "Para [segmento específico] que [situação/trigger], [nome do produto] é [categoria] que [principal diferencial]. Diferente de [principal alternativa], [produto] [diferencial único e verificável]."

### Passo 6 — Construir Mapa StoryBrand
Complete os 7 elementos com linguagem do cliente.

### Passo 7 — Gerar Variações por Canal
Adaptar a mensagem mestre para cada formato.

---

## Variações por Canal

### Headline (Landing page / Ad)
Máximo 10 palavras. Focado no resultado principal.
Formato: [Verbo de resultado] + [o que] + [para quem / em quanto tempo / sem o quê]

### Tagline (Slogan / Marca)
3-6 palavras. Memorável. Captura o posicionamento em essência.

### Elevator Pitch (30 segundos)
Estrutura: "Você sabe quando [problema]? O que a gente faz é [solução simples]. Resultado: [resultado]. Já fizemos isso para [exemplo]. [CTA]."

### Cold Email Opening (2-3 linhas)
Estrutura: [Contexto relevante do destinatário] + [dor específica] + [promessa de 1 linha] + [CTA]

---

## Template de Output

```
POSITIONING & MESSAGING DOCUMENT
=================================
Produto: [nome]
ICP alvo: [perfil]
Data: [data]

DECLARAÇÃO DE POSICIONAMENTO
-----------------------------
"Para [segmento] que [situação/trigger], [produto] é [categoria] que [diferencial principal].
Diferente de [alternativa principal], [produto] [diferencial único verificável]."

ATRIBUTOS ÚNICOS
----------------
1. [Atributo] → Valor: [tradução em resultado de negócio]
2. [Atributo] → Valor: [tradução em resultado de negócio]
3. [Atributo] → Valor: [tradução em resultado de negócio]

DIFERENCIAL ÚNICO (UVP em 1 frase)
------------------------------------
"[A única solução que _____ para _____ sem _____.]"

MAPA STORYBRAND
---------------
Herói: [quem é o cliente — cargo, situação]
Problema externo: [o obstáculo prático]
Problema interno: [como o cliente se sente com o problema]
Problema filosófico: [por que é errado o mundo funcionar assim]
Guia (sua empresa): [como você se posiciona como guia com credibilidade]
Plano em 3 passos: [1. X → 2. Y → 3. Z]
Call to Action: [o que fazer agora]
Cenário de fracasso: [o que acontece se não agir]
Cenário de sucesso: [como fica a vida do cliente depois]

VARIAÇÕES POR CANAL
-------------------

Headline:
"[máximo 10 palavras]"

Tagline:
"[3-6 palavras]"

Elevator Pitch (30s):
"[texto completo de 3-4 frases]"

Cold Email Opening:
"[2-3 linhas prontas para uso]"

Instagram/Meta Ad (hook):
"[1 frase de parada de scroll]"

LinkedIn (contexto profissional):
"[versão adaptada para tom B2B LinkedIn]"
```

---

## Exemplos de Uso

**Exemplo 1 — Plataforma de IA para CS:**
> Posicionamento: "Para gestores de Customer Success em SaaS B2B com carteira acima de 100 contas, nossa plataforma é o único sistema de CS que prevê churn 30 dias antes de acontecer com base em sinais comportamentais — diferente de CRMs genéricos que mostram churn depois que já aconteceu."
> UVP: "A única plataforma que mostra quem vai cancelar antes que eles saibam."

**Exemplo 2 — Agência de automação:**
> Tagline: "Menos operação. Mais decisão."
> Elevator pitch: "Você sabe quando seu time passa metade do dia em tarefas repetitivas que poderiam ser automatizadas? O que a gente faz é mapear essas tarefas e implementar automações em 30 dias. O resultado médio é 15h por semana devolvidas para cada funcionário. Já fizemos isso em 40 empresas. Faz sentido conversar?"

---

## Quality Gates

- Posicionamento é específico para um segmento — não serve para todo mundo
- Diferencial único não é genérico e passa no teste "meu concorrente pode dizer o mesmo?"
- Mensagem mestre foi testada em linguagem do cliente real (não jargão interno)
- Variações por canal adaptam tom sem abandonar o posicionamento central
- Elevator pitch lido em voz alta dura no máximo 30 segundos
- Tagline é memorável e captura o posicionamento em essência
