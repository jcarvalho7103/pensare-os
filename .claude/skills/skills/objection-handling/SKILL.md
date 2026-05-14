---
name: objection-handling
description: Gestão das 10 objeções mais comuns em vendas de IA/tecnologia usando Feel-Felt-Found
argument-hint: "objecao: '[texto da objeção do lead]', contexto: '{dados do lead e momento da venda}'"
allowed-tools: Read
tier: skill
version: 0.1.0
usable-by:
  - pensare-closer
  - pensare-comercial
handoff_in:
  required:
    objecao: "Texto exato ou parafraseado da objeção levantada pelo lead"
    contexto: "Momento da venda (primeiro contato, pós-proposta, pré-fechamento) e dados do lead"
  optional:
    historico_objecoes: "Objeções anteriores já levantadas pelo mesmo lead"
    produto: "Produto ou solução específica sendo vendida"
handoff_out:
  produces:
    objecao_identificada: "Nome da objeção mapeada dentre as 10 catalogadas"
    resposta_fff: "Resposta completa no padrão Feel-Felt-Found"
    pergunta_avanco: "Pergunta para avançar a conversa após a resposta"
    nivel_risco: "Avaliação: objeção real vs. smoke screen"
quality_gates:
  - "Objeção identificada corretamente antes de responder"
  - "Resposta usa Feel-Felt-Found na sequência correta"
  - "Pergunta de avanço é aberta e convida o lead a se comprometer"
  - "Resposta não é defensiva nem empurra o produto"
---

# Objection Handling

Skill de gestão de objeções para o Pensare OS. Cobre as 10 objeções mais frequentes em vendas de IA e tecnologia, com resposta estruturada no padrão Feel-Felt-Found e pergunta de avanço calibrada para cada situação.

## Quando Invocar

- Quando o lead levanta uma objeção durante ou após o diagnóstico
- Antes de responder a um "não" ou hesitação do cliente
- Para preparar o closer antes de uma reunião com objeções conhecidas
- Quando o SDR precisa de apoio para superar resistências por escrito (WhatsApp/email)

---

## Framework Feel-Felt-Found

**Feel:** "Eu entendo como você se sente..."
Valida a emoção ou preocupação do cliente. Nunca minimize ou rebata diretamente.

**Felt:** "Outros clientes nossos também sentiram isso..."
Normaliza a objeção. Mostra que não é um problema único, remove a pressão.

**Found:** "O que eles encontraram foi..."
Apresenta a virada. Use prova, resultado ou reframe com base em evidência.

**Pergunta de Avanço:** Pergunta aberta que coloca o lead no próximo passo sem pressão.

---

## As 10 Objeções e Respostas

---

### 1. "Muito caro"

**Identificar se é real:** Perguntar "Caro em comparação com o quê?" revela se é percepção de valor ou realmente fora de budget.

**Resposta FFF:**
- **Feel:** "Faz todo sentido querer ter certeza que o investimento vale a pena antes de comprometer."
- **Felt:** "Vários dos nossos clientes chegaram com a mesma percepção — o número parecia alto antes de entender o retorno."
- **Found:** "O que eles descobriram foi que, considerando [custo da inação — horas, oportunidades perdidas, custo do problema], o ROI costuma aparecer nos primeiros [prazo típico]. No seu caso, você mesmo estimou que esse problema custa [X] por mês — o investimento se paga em [cálculo rápido]."

**Pergunta de Avanço:** "Se a gente conseguisse mostrar um cenário de ROI com os números da sua empresa, isso mudaria sua perspectiva sobre o investimento?"

---

### 2. "Não é o momento"

**Identificar se é real:** Smoke screen frequente. Explorar o que mudaria o momento.

**Resposta FFF:**
- **Feel:** "Entendo, timing é tudo — não faz sentido iniciar algo sem o momento certo."
- **Felt:** "Muitos clientes nossos também disseram isso quando falamos pela primeira vez. Alguns esperaram e voltaram meses depois."
- **Found:** "O que eles perceberam é que o 'momento ideal' raramente aparece sozinho. O que costuma criar o momento é a decisão de priorizar. Me diz: o que precisaria acontecer para esse problema subir na lista de prioridades de vocês?"

**Pergunta de Avanço:** "O que está competindo com isso pelo orçamento e atenção agora? Pode ser que a gente consiga encaixar de um jeito que não conflite."

---

### 3. "Vou pensar"

**Identificar se é real:** Quase sempre é uma forma educada de dizer não sem conflito. Explorar o que falta para decidir.

**Resposta FFF:**
- **Feel:** "Claro, uma decisão dessas merece reflexão — eu não esperaria menos de você."
- **Felt:** "Outros decisores com quem trabalhamos também pediram tempo para pensar. Na maioria dos casos, o que ajudou foi clareza sobre o que ainda faltava."
- **Found:** "Pra eu poder te ajudar nessa reflexão: o que especificamente você ainda precisa ver, entender ou confirmar antes de tomar uma decisão? Às vezes tem uma dúvida pontual que a gente resolve aqui agora."

**Pergunta de Avanço:** "Qual é o fator número 1 que você ainda precisa resolver mentalmente para seguir em frente — ou não seguir?"

---

### 4. "Já temos uma solução"

**Identificar se é real:** Entender qual solução, como está funcionando e o nível de satisfação atual.

**Resposta FFF:**
- **Feel:** "Ótimo — significa que vocês já entenderam a importância de resolver isso."
- **Felt:** "Boa parte dos nossos clientes também tinham uma solução em uso quando nos procuraram. Não necessariamente porque a solução era ruim."
- **Found:** "O que eles encontraram é que havia uma lacuna específica que a solução atual não cobria — geralmente em [área comum de gap: integração, escala, custo por usuário, suporte]. Me conta: como está sendo a experiência com o que vocês usam hoje? Tem alguma coisa que você gostaria que funcionasse diferente?"

**Pergunta de Avanço:** "Se você pudesse mudar uma coisa no que vocês usam hoje, o que seria?"

---

### 5. "Preciso aprovar com o time / com a diretoria"

**Identificar se é real:** Confirmar quem são as pessoas, o processo de aprovação e se o interlocutor apoia a solução.

**Resposta FFF:**
- **Feel:** "Faz todo sentido envolver o time — decisões assim impactam mais de uma área."
- **Felt:** "Frequentemente passamos por esse processo com nossos clientes e entendemos bem como funciona."
- **Found:** "O que costuma ajudar muito é preparar o material certo para cada stakeholder — especialmente com argumentos financeiros para diretoria e argumentos de usabilidade para o time operacional. Posso te ajudar a montar isso. Me diz: quem são as pessoas que precisam dar o aval e qual é a principal preocupação de cada uma?"

**Pergunta de Avanço:** "Você pessoalmente acredita que isso faz sentido para a empresa? Se sim, posso te ajudar a montar o case interno."

---

### 6. "Não confio em IA"

**Identificar se é real:** Objeção frequente e genuína. Não minimizar — aprofundar para entender a origem da desconfiança.

**Resposta FFF:**
- **Feel:** "Essa desconfiança é completamente válida — e honestamente é saudável. IA tem muito hype e muita promessa sem entrega."
- **Felt:** "Vários dos nossos melhores clientes entraram com ceticismo alto. Um deles disse literalmente que só veio porque um amigo insistiu."
- **Found:** "O que eles encontraram foi que a diferença está em como a IA é implementada e com que nível de controle humano. No nosso caso, [descrever salvaguardas, revisão humana, transparência]. A dúvida de vocês não é sobre IA em geral — é sobre se essa IA específica vai fazer o que promete. E isso é exatamente o que a gente testa antes de assinar qualquer contrato."

**Pergunta de Avanço:** "O que seria necessário para você ter confiança suficiente para fazer um teste controlado — sem compromisso de longo prazo?"

---

### 7. "Sem tempo para implementar"

**Identificar se é real:** Objeção operacional válida. Entender quem seria responsável pela implementação e qual é o esforço real esperado.

**Resposta FFF:**
- **Feel:** "Implementação dá trabalho — e um projeto que toma tempo do time sem entregar rápido é um problema real."
- **Felt:** "Outros clientes tinham o mesmo receio. Um deles adiou 2 meses por esse motivo."
- **Found:** "O que encontramos é que o onboarding leva [X dias/semanas] e requer [Y horas] do lado de vocês, concentradas nos primeiros [Z dias]. Depois disso é totalmente autônomo. Posso te mostrar o cronograma padrão de implementação e você me diz se encaixaria na agenda de vocês?"

**Pergunta de Avanço:** "Qual seria o pior momento do calendário de vocês para iniciar? Assim a gente planeja fora desse período."

---

### 8. "Quero testar grátis primeiro"

**Identificar se é real:** Avaliar se é objeção de confiança (legítima) ou hábito de não pagar (problema de valor percebido).

**Resposta FFF:**
- **Feel:** "Faz sentido querer ver resultado antes de comprometer — especialmente com algo novo."
- **Felt:** "Muita gente pede isso. E quando a gente tem um trial, ele costuma virar cliente."
- **Found:** "O desafio com testes sem compromisso é que eles raramente recebem a atenção necessária para mostrar resultado real. O que funciona melhor é [opção: um piloto pago reduzido / garantia de resultado / onboarding intensivo no primeiro mês]. Isso te dá a segurança do teste com a seriedade de um projeto real. Qual das duas opções faria mais sentido para o seu caso?"

**Pergunta de Avanço:** "O que você precisaria ver no teste para tomar a decisão de seguir em frente?"

---

### 9. "Meu concorrente não usa isso"

**Identificar se é real:** Reframing de liderança vs. seguidor de mercado.

**Resposta FFF:**
- **Feel:** "É sempre bom calibrar com o mercado antes de mover."
- **Felt:** "Curiosamente, essa é uma das objeções mais comuns — e também uma das mais paradoxais que ouvimos."
- **Found:** "O que nossos clientes perceberam é que quando o concorrente já está usando, a vantagem de adotar agora já diminuiu. Os que cresceram mais rápido foram exatamente os que chegaram primeiro. [Se concorrente já usa]: na verdade, [concorrente ou empresa do setor] já está usando — o que significa que cada mês de espera é vantagem competitiva cedida."

**Pergunta de Avanço:** "Qual seria a vantagem para vocês se conseguissem resolver [dor principal] antes dos seus concorrentes?"

---

### 10. "Resultados não são garantidos"

**Identificar se é real:** Objeção de risco. Explorar qual garantia seria suficiente.

**Resposta FFF:**
- **Feel:** "Você está 100% certo — nenhum resultado em negócios é absolutamente garantido. E qualquer um que prometa isso está mentindo."
- **Felt:** "Os clientes que mais nos pressionam nesse ponto são exatamente os que se tornaram nossos melhores cases — porque eles monitoram de perto."
- **Found:** "O que a gente oferece não é uma garantia mágica, mas sim [garantia real: garantia de resultado em X dias / política de reembolso / cláusula de performance / acompanhamento mensal com metas]. Isso coloca a pele no jogo do nosso lado também. Me conta: qual seria o resultado mínimo aceitável para você considerar o projeto um sucesso?"

**Pergunta de Avanço:** "Se a gente conseguisse colocar esse critério de sucesso em contrato, isso te daria segurança suficiente para avançar?"

---

## Template de Output

```
OBJECTION HANDLING REPORT
==========================
Lead: [Nome] | [Momento da venda]
Objeção recebida: "[texto exato ou parafraseado]"

DIAGNÓSTICO
-----------
Objeção identificada: [nome das 10]
Tipo: [real / smoke screen / mista]
Causa provável: [percepção de valor / risco / timing / processo interno]

RESPOSTA RECOMENDADA
--------------------
Feel: "[texto]"
Felt: "[texto]"
Found: "[texto — adaptar com dados do lead se disponível]"

Pergunta de Avanço: "[pergunta]"

NÍVEL DE RISCO
--------------
[baixo / médio / alto] — [justificativa em 1 linha]

PRÓXIMO PASSO SE CONTORNAR
--------------------------
[o que fazer depois de superar essa objeção]
```

---

## Quality Gates

- Objeção identificada corretamente antes de responder (nunca responder no piloto automático)
- Resposta usa Feel-Felt-Found na sequência correta, sem pular etapas
- Pergunta de avanço é aberta e convida o lead a se comprometer com uma resposta
- Resposta não é defensiva, não minimiza a preocupação e não empurra o produto
- Se objeção for smoke screen, aprofundar antes de responder com o roteiro padrão
