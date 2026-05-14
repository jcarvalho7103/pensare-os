---
name: campaign-optimization
description: Analisa métricas de campanha em 3 camadas e gera plano de otimização priorizado
argument-hint: "metricas: {impressoes, cliques, conversoes, custo, roas}, canal: 'Meta|Google|LinkedIn'"
allowed-tools: Read, Write
tier: skill
version: 0.1.0
usable-by:
  - pensare-trafego
  - pensare-growth
  - pensare-dados
handoff_in:
  required:
    context: "Métricas atuais da campanha: impressões, cliques, conversões, custo total e ROAS"
  optional:
    historico: "Performance histórica para comparação (semana anterior, mês anterior)"
    canal: "Canal específico (Meta, Google, LinkedIn, YouTube)"
    objetivo: "Objetivo da campanha (leads, vendas, tráfego, awareness)"
    segmentacao: "Dados de segmentação usada (público, dispositivo, posicionamento)"
handoff_out:
  produces:
    diagnostico: "Causa-raiz identificada com camada do problema (criativo/LP/oferta)"
    plano_otimizacao: "Plano priorizado com quick wins e ações de médio prazo"
    hipoteses_teste: "Hipóteses de A/B para validar as melhorias propostas"
    projecao: "Projeção de melhoria esperada por ação implementada"
quality_gates:
  - "Diagnóstico identifica camada específica (não 'está tudo ruim')"
  - "Quick wins são executáveis em até 48h sem novos recursos"
  - "Cada recomendação tem métrica de sucesso definida"
  - "Hipóteses de teste seguem formato: 'Se X então Y porque Z'"
  - "Projeções de melhoria são conservadoras e baseadas em benchmarks de mercado"
---

# Campaign Optimization

Skill de otimização de campanhas de performance para o Pensare OS. Aplica diagnóstico em 3 camadas (criativo, landing page e oferta) com base em thresholds de mercado para identificar causa-raiz e gerar plano de otimização priorizado.

## Quando Invocar

- Quando o ROAS está abaixo do break-even ou de metas definidas
- Na revisão semanal/quinzenal de campanhas ativas
- Quando o CTR ou CVR caem mais de 20% em relação à semana anterior
- Antes de escalar o budget de uma campanha (garantir eficiência antes de aumentar volume)
- Quando resultados de uma campanha nova não estão dentro do esperado após 7 dias

---

## Thresholds de Referência por Métrica

| Métrica | Ruim | Aceitável | Bom | Excelente |
|---|---|---|---|---|
| CTR (Meta Feed) | <0,5% | 0,5-1% | 1-3% | >3% |
| CTR (Google Search) | <2% | 2-5% | 5-10% | >10% |
| CTR (LinkedIn) | <0,3% | 0,3-0,6% | 0,6-1,5% | >1,5% |
| CVR Landing Page | <1% | 1-2% | 2-5% | >5% |
| CVR Formulário Lead | <5% | 5-15% | 15-30% | >30% |
| ROAS E-commerce | <1x | 1-2x | 2-4x | >4x |
| ROAS Lead Gen | <1x | 1-2x | 2-3x | >3x |
| CPC (Meta) | >R$5 | R$2-5 | R$0,5-2 | <R$0,5 |
| CPL (Meta B2B) | >R$150 | R$80-150 | R$30-80 | <R$30 |

**Nota:** thresholds variam por setor, ticket e maturidade da conta. Usar como ponto de partida, calibrar com histórico do cliente.

---

## Diagnóstico em 3 Camadas

### Camada 1 — Criativo
**Sintoma:** CTR baixo. O anúncio não está gerando cliques suficientes.

**Quando suspeitar do criativo:**
- CTR abaixo de 1% em Meta
- CPM alto com CTR baixo (está sendo mostrado, mas não está clicando)
- Queda de CTR após 5-7 dias sem troca de criativo (fadiga)
- Frequência acima de 3x no mesmo público (saturação)

**Diagnóstico de criativo:**
- Hook: os primeiros 3 segundos (imagem/vídeo/headline) estão parando o scroll?
- Relevância: o público reconhece a situação descrita como sua?
- Clareza: em 5 segundos é possível entender o que está sendo oferecido?
- CTA visual: existe chamada clara para ação?

**Ações de otimização — Criativo:**
1. Testar novo hook (pelo menos 3 variações de ângulo diferente)
2. Trocar formato (estático → vídeo ou vice-versa)
3. Mudar ângulo da mensagem (dor → curiosidade ou prova social)
4. Atualizar público para combater fadiga (lookalike novo, segmento diferente)

---

### Camada 2 — Landing Page
**Sintoma:** CTR bom, mas conversão baixa. As pessoas clicam e não convertem.

**Quando suspeitar da LP:**
- CTR bom (>1%) mas CVR <2%
- Alta taxa de rejeição (>70%) ou tempo na página <30s
- Muitos cliques, poucos leads/vendas

**Diagnóstico de landing page:**
- Consistência de mensagem: o que o anúncio prometeu está na LP?
- Velocidade: carrega em menos de 3 segundos no mobile?
- Clareza da oferta: em 5 segundos dá para entender o que é e o que fazer?
- Fricção no formulário: pede informações demais?
- Prova social: tem depoimentos, números, logos?
- CTA: é claro, está acima da dobra e repete ao longo da página?

**Ações de otimização — Landing Page:**
1. Garantir message match (headline da LP = promessa do anúncio)
2. Reduzir campos do formulário para o mínimo (nome + email + WhatsApp = suficiente)
3. Adicionar prova social acima da dobra
4. Teste de velocidade (PageSpeed Insights — meta: >70 mobile)
5. Criar variação de LP com headline diferente para A/B

---

### Camada 3 — Oferta
**Sintoma:** conversão acontece, mas ROAS está baixo ou CAC está alto demais.

**Quando suspeitar da oferta:**
- ROAS <2x em e-commerce ou <1,5x em lead gen
- CAC acima do LTV viável
- Alta taxa de abandono no checkout
- Leads chegam mas não convertem em vendas

**Diagnóstico de oferta:**
- Fit de preço: o preço percebido é proporcional ao valor percebido?
- Clareza do valor: o que o cliente ganha está explícito?
- Risco percebido: há garantia? Prova de resultado?
- Urgência: há razão para agir agora vs. depois?
- Concorrência: como o preço se compara ao que o cliente vê como alternativa?

**Ações de otimização — Oferta:**
1. Revisar stack de valor (usar skill offer-creation)
2. Adicionar ou reforçar garantia
3. Criar urgência legítima (vagas, prazo, bônus temporário)
4. Testar preços diferentes (Van Westendorp ou preço âncora)
5. Aumentar ticket com upsell ao invés de baixar preço

---

## Protocolo de Execução

### Passo 1 — Coleta e Classificação das Métricas
Preencha a tabela de diagnóstico com os dados fornecidos:

| Métrica | Valor Atual | Benchmark | Status |
|---|---|---|---|
| CTR | X% | >1% | Vermelho/Amarelo/Verde |
| CVR | X% | >2% | Vermelho/Amarelo/Verde |
| ROAS | Xx | >2x | Vermelho/Amarelo/Verde |
| CPL/CAC | R$X | Meta definida | Vermelho/Amarelo/Verde |
| Frequência | Xx | <3x | Vermelho/Amarelo/Verde |

### Passo 2 — Identificar a Camada do Problema
Seguir a lógica sequencial:
1. CTR ruim → problema é o criativo (investir aí primeiro)
2. CTR bom + CVR ruim → problema é a landing page
3. CTR bom + CVR bom + ROAS ruim → problema é a oferta ou o funil pós-clique

**Regra:** resolver o criativo antes de mexer na LP. Resolver a LP antes de mexer na oferta.

### Passo 3 — Formular Hipóteses de Teste
Para cada problema identificado, formule hipóteses no padrão:
> "Se [mudança específica] então [métrica] vai melhorar em [X%] porque [razão]."

### Passo 4 — Priorizar Ações

**Quick wins (até 48h, sem novos recursos):**
- Pausar criativos com CTR <0,5% e baixo volume de impressão
- Duplicar conjuntos com melhor performance e aumentar budget
- Adicionar exclusões de público (evitar desperdício)
- Ajustar horário/dia com base nos dados de breakdown

**Ações de médio prazo (3-14 dias):**
- Criar novas variações de criativo com ângulos diferentes
- Otimizar LP (message match, velocidade, formulário)
- Testar nova oferta ou nova estrutura de preço

### Passo 5 — Projeção de Melhoria
Para cada ação proposta, estime:
- Qual métrica melhora
- Quanto (conservador: 10-20%, otimista: 30-50%)
- Em quanto tempo o resultado aparece

---

## Template de Output

```
CAMPAIGN OPTIMIZATION REPORT
==============================
Campanha: [nome]
Canal: [Meta / Google / LinkedIn]
Período analisado: [data início] a [data fim]
Data da análise: [data]

DIAGNÓSTICO DE MÉTRICAS
-----------------------
| Métrica    | Atual  | Benchmark | Status       |
|------------|--------|-----------|--------------|
| CTR        | X%     | >1%       | [R/Y/G]      |
| CVR        | X%     | >2%       | [R/Y/G]      |
| ROAS       | Xx     | >2x       | [R/Y/G]      |
| CPL        | R$X    | R$X meta  | [R/Y/G]      |
| Frequência | Xx     | <3x       | [R/Y/G]      |

CAMADA DO PROBLEMA
------------------
Camada principal: [CRIATIVO / LANDING PAGE / OFERTA]
Causa-raiz identificada: [descrição em 2-3 linhas]

Camada secundária (se houver): [camada]
Causa-raiz secundária: [descrição]

HIPÓTESES DE TESTE
------------------
H1: "Se [mudança] então [métrica] melhora X% porque [razão]"
H2: "Se [mudança] então [métrica] melhora X% porque [razão]"
H3: "Se [mudança] então [métrica] melhora X% porque [razão]"

PLANO DE OTIMIZAÇÃO
-------------------

QUICK WINS (executar em até 48h):
  [ ] 1. [ação] → impacto esperado: [métrica +X%]
  [ ] 2. [ação] → impacto esperado: [métrica +X%]
  [ ] 3. [ação] → impacto esperado: [métrica +X%]

MÉDIO PRAZO (3-14 dias):
  [ ] 4. [ação] → impacto esperado: [métrica +X%] | prazo: [X dias]
  [ ] 5. [ação] → impacto esperado: [métrica +X%] | prazo: [X dias]

PROJEÇÃO
--------
Se quick wins forem implementados:
  CTR esperado: X% → X% (+X%)
  CVR esperado: X% → X% (+X%)
  ROAS esperado: Xx → Xx (+X%)
  Prazo para ver resultado: [X dias]

PRÓXIMA REVISÃO
---------------
Data recomendada: [data]
Métricas a monitorar: [lista]
```

---

## Exemplos de Uso

**Exemplo 1 — Meta Ads com CTR 0,4%:**
> Diagnóstico: Camada 1 (criativo). CTR abaixo do threshold. Frequência 4,2x — saturação.
> Quick wins: pausar 3 conjuntos com CTR <0,3%, criar 2 novos ângulos de hook (curiosidade + dor direta)
> Projeção: CTR de 0,4% para 1,2% em 7 dias com novos criativos

**Exemplo 2 — Google Ads com CTR bom mas CVR 0,8%:**
> Diagnóstico: Camada 2 (LP). CTR 8% (bom), mas CVR 0,8% (crítico). LP carrega em 6s no mobile.
> Quick wins: reduzir campos do formulário, adicionar headline com message match, otimizar velocidade
> Projeção: CVR de 0,8% para 2,5% em 14 dias

---

## Quality Gates

- Diagnóstico identifica camada específica com base em evidências métricas
- Quick wins são executáveis em até 48h sem novos recursos ou aprovações
- Cada recomendação tem métrica de sucesso definida e prazo
- Hipóteses de teste seguem formato: "Se X então Y porque Z"
- Projeções de melhoria são conservadoras e baseadas em benchmarks do setor
- Relatório gerado no máximo 2h após receber os dados
