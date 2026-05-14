---
name: creative-hook
description: Cria hooks e conceitos criativos para ads e conteúdo por canal e objetivo
argument-hint: "produto: '{descrição}', publico: '{ICP}', canal: 'Meta|YouTube|LinkedIn|Instagram', objetivo: 'awareness|conversao'"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-criativos
  - pensare-copy
  - pensare-trafego
handoff_in:
  required:
    context: "Produto ou serviço, público-alvo, canal de distribuição e objetivo da campanha (awareness ou conversão)"
  optional:
    posicionamento: "Output do positioning-messaging para manter alinhamento de mensagem"
    oferta: "Output do offer-creation com a promessa e diferenciais"
    top_performers: "Exemplos de criativos que já funcionaram para este produto ou nicho"
handoff_out:
  produces:
    hooks: "10 hooks variados por tipo"
    conceitos_criativos: "3 conceitos completos com hook + body + CTA"
    roteiros_video: "2 roteiros de vídeo curto (até 60s)"
    analise_hooks: "Justificativa de por que cada hook funciona para o público"
quality_gates:
  - "10 hooks cobrem ao menos 4 tipos diferentes (não todos do mesmo tipo)"
  - "Cada hook passa no teste: faria o scroll parar nos primeiros 3 segundos?"
  - "Conceitos criativos têm hook + body + CTA — nenhuma parte pode faltar"
  - "Roteiros de vídeo têm marcação de tempo e indicação de visual/locução"
  - "Nenhum hook usa linguagem de IA óbvia ou clichê de marketing"
---

# Creative Hook Creation

Skill de criação de hooks e criativos para o Pensare OS. Produz 10 hooks por tipo, 3 conceitos criativos completos e 2 roteiros de vídeo curto adaptados ao canal, público e objetivo de campanha.

## Quando Invocar

- Ao iniciar uma nova campanha de ads
- Quando os criativos atuais estão com CTR abaixo de 1% ou fadigados
- Para criar variações de teste A/B de criativos existentes
- Na produção de conteúdo orgânico com objetivo de crescimento de audiência
- Quando o time criativo precisa de conceitos para briefar produção

---

## Os 6 Tipos de Hook

### Tipo 1 — Curiosidade
Abre um loop cognitivo que o cérebro precisa fechar.
**Padrão:** "[Afirmação estranha ou contraintuitiva que contradiz o que o público acredita]"
**Exemplo:** "O erro que 90% dos gestores de vendas cometem justamente quando o time está crescendo."

### Tipo 2 — Prova Social
Usa resultado real de terceiro para gerar credibilidade e inveja saudável.
**Padrão:** "Como [pessoa/empresa similar ao ICP] conseguiu [resultado específico] em [prazo]"
**Exemplo:** "Como uma clínica de SP substituiu 3 atendentes por um assistente de IA e reduziu custo em 40%."

### Tipo 3 — Dor Direta
Nomeia exatamente o problema que o público vive e odeia.
**Padrão:** "[Situação de dor específica e reconhecível em 1ª ou 2ª pessoa]"
**Exemplo:** "Cansado de perder leads qualificados porque ninguém respondeu a tempo?"

### Tipo 4 — Polêmica
Afirmação forte que vai contra o senso comum do setor.
**Padrão:** "[Coisa que todos fazem] está errado. [Posição contrária]."
**Exemplo:** "Parar de postar todo dia foi o que fez meu alcance triplicar."

### Tipo 5 — Número Específico
Número concreto que ancora credibilidade e especificidade.
**Padrão:** "[Número específico] + [resultado] + [contexto que gera comparação]"
**Exemplo:** "R$ 127.000 em vendas em 11 dias — sem tráfego pago."

### Tipo 6 — Identidade
Invoca a identidade do público-alvo. Quem você é define o que você clica.
**Padrão:** "Se você é [identidade específica], [promessa ou aviso relevante]."
**Exemplo:** "Se você é fundador de uma startup e ainda faz atendimento manual, leia isso."

---

## Adaptação por Canal

### Meta Ads (Feed + Stories + Reels)
- Primeiros 3 segundos são o hook — texto na tela ou fala
- Feed: imagem estática ou vídeo até 15s — hook deve funcionar sem som
- Reels: vertical, ritmo rápido, hook visual + verbal simultâneos
- Tom: direto, próximo, sem formalidade excessiva

### YouTube (Pre-roll + Shorts)
- Pre-roll: primeiros 5 segundos antes do skip — hook tem que ser a coisa mais intrigante
- Shorts: vertical, hooks de identidade ou polêmica funcionam melhor
- Tom: mais elaborado, pode ter contexto antes do CTA

### LinkedIn
- Primeira linha visível antes do "ver mais" é o hook — máximo 160 caracteres
- Tom: profissional mas não corporativo, primeira pessoa
- Hooks de número específico e polêmica performam melhor
- Evitar: linguagem de vendor, termos como "solução robusta" ou "ecossistema"

### Instagram (Feed + Stories + Reels)
- Feed: estético + informativo — hook pode ser mais inspiracional
- Stories: interativo, direto, CTAs claros (swipe up, link)
- Reels: entretenimento primeiro, valor segundo — hook de polêmica ou curiosidade

---

## Protocolo de Execução

### Passo 1 — Definir Contexto
Confirme: produto, ICP, canal, objetivo (awareness = topo de funil / conversão = fundo de funil).
Se tiver posicionamento definido, use a linguagem do cliente identificada ali.

### Passo 2 — Gerar os 10 Hooks
Distribua pelos tipos:
- Mínimo 4 tipos diferentes representados
- Ao menos 2 hooks de curiosidade (alta performance geral)
- Ao menos 1 hook de dor direta e 1 de prova social
- Adaptar linguagem ao canal escolhido

### Passo 3 — Selecionar os 3 Melhores para Conceitos Completos
Critérios de seleção:
1. Mais provável de parar o scroll para o público específico
2. Mais alinhado ao objetivo (awareness vs. conversão)
3. Mais diferente entre si (cobrir variação de abordagem)

### Passo 4 — Desenvolver os 3 Conceitos Completos
Cada conceito: Hook + Body + CTA

**Body** deve:
- Entregar o que o hook prometeu (não prometer e não cumprir)
- Ter um único ângulo — sem dispersar
- Usar prova, dados ou narrativa para sustentar
- Falar diretamente ao ICP (não ao mundo)

**CTA** deve:
- Ser específico sobre o próximo passo
- Reduzir fricção ("responde aqui", "clica no link", "comenta X")
- Criar micro-comprometimento antes do grande compromisso

### Passo 5 — Criar 2 Roteiros de Vídeo
Um roteiro mais curto (15-30s) e um mais longo (45-60s).
Marcar: tempo de cada cena / fala + indicação de visual + texto na tela se necessário.

---

## Template de Output

```
CREATIVE HOOK REPORT
=====================
Produto: [nome]
ICP: [perfil]
Canal: [canal]
Objetivo: [awareness / conversão]
Data: [data]

10 HOOKS
--------
[1] CURIOSIDADE: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[2] CURIOSIDADE: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[3] PROVA SOCIAL: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[4] DOR DIRETA: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[5] DOR DIRETA: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[6] POLÊMICA: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[7] POLÊMICA: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[8] NÚMERO ESPECÍFICO: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[9] NÚMERO ESPECÍFICO: "[texto do hook]"
    Por que funciona: [justificativa em 1 linha]

[10] IDENTIDADE: "[texto do hook]"
     Por que funciona: [justificativa em 1 linha]

---

CONCEITO CRIATIVO 1 — [Nome do Conceito]
-----------------------------------------
Hook: "[texto]"

Body:
"[texto completo do body — 3-5 parágrafos ou bullets]"

CTA: "[texto do call to action]"

Formato sugerido: [imagem estática / carrossel / vídeo / stories]
Nota de produção: [orientações para o time de criação]

---

CONCEITO CRIATIVO 2 — [Nome do Conceito]
-----------------------------------------
Hook: "[texto]"
Body: "[texto]"
CTA: "[texto]"
Formato sugerido: [formato]
Nota de produção: [orientações]

---

CONCEITO CRIATIVO 3 — [Nome do Conceito]
-----------------------------------------
Hook: "[texto]"
Body: "[texto]"
CTA: "[texto]"
Formato sugerido: [formato]
Nota de produção: [orientações]

---

ROTEIRO DE VÍDEO 1 — [título] (15-30s)
----------------------------------------
[00:00-00:03] HOOK VISUAL: [o que aparece na tela]
              FALA/LEGENDA: "[texto]"

[00:03-00:12] DESENVOLVIMENTO: [visual]
              FALA/LEGENDA: "[texto]"

[00:12-00:20] PROVA / RESULTADO: [visual]
              FALA/LEGENDA: "[texto]"

[00:20-00:25] CTA: [visual]
              FALA/LEGENDA: "[texto]"

Texto na tela key moments: [lista dos textos]
Música sugerida: [tipo/mood]

---

ROTEIRO DE VÍDEO 2 — [título] (45-60s)
----------------------------------------
[estrutura similar com mais desenvolvimento]
```

---

## Exemplos de Uso

**Exemplo 1 — Meta Ads, conversão, automação de vendas:**
> Hook 1 (dor): "Seu time de vendas está ocupado demais para vender?"
> Hook 2 (número): "22 horas por semana economizadas por SDR. Aqui está como."
> Conceito 1: Dor direta → problema do tempo perdido → solução específica → agendamento como CTA

**Exemplo 2 — LinkedIn, awareness, IA para RH:**
> Hook (polêmica): "Recrutamento por currículo seleciona os melhores candidatos para mentir, não para trabalhar."
> Body: argumento, dados, nova perspectiva → CTA: "Comente 'novo jeito' e eu te mando o estudo."

---

## Quality Gates

- 10 hooks cobrem ao menos 4 tipos diferentes
- Cada hook passa no teste: faria o scroll parar nos primeiros 3 segundos?
- Conceitos criativos têm hook + body + CTA — nenhuma parte pode faltar
- Roteiros têm marcação de tempo e indicação de visual/locução
- Nenhum hook usa linguagem de IA óbvia ("como IA", "inovação", "soluções disruptivas") ou clichê de marketing ("a melhor", "número 1")
- Body entrega o que o hook prometeu — sem bait-and-switch
