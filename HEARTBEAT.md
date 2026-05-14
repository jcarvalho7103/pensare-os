# HEARTBEAT.md — Ritmo, Monitoramento e Ajuste Contínuo

> Define o ritmo do Pensare OS: rotinas automáticas, métricas monitoradas, thresholds, alertas e gatilhos de evento.
> O Pensare OS não espera ser chamado — ele **antecipa, monitora e alerta**.
> Runtime: Python daemon (`heartbeat/daemon.py`) + Mac launchd · Atualizado com mapeamento do Lovable.

---

## Filosofia do Heartbeat

> "O sistema que só responde é um assistente. O sistema que antecipa é um OS."

O HEARTBEAT garante que mesmo em dias sem interação explícita da Isis, o Pensare OS:
1. **Monitora** o que importa
2. **Identifica** desvios
3. **Aciona** os agentes corretos
4. **Mantém** o ritmo de execução
5. **Registra** o aprendizado

**Pergunta central do sistema de Heartbeats**:
> "O sistema está melhorando ou piorando?"

**Sem Heartbeats**: caos. **Com Heartbeats**: previsibilidade.

---

## Cadência de Três Camadas

| Ritmo | Foco | Output |
|-------|------|--------|
| **Daily** | Execução — controle operacional do dia | Status do dia + problema principal + ação imediata |
| **Weekly** | Otimização tática — destravar gargalos | Gargalo principal + ajuste da semana + plano de ação |
| **Monthly** | Estratégia — ajuste estrutural | Diagnóstico estratégico + ajustes estruturais |

---

## Métricas Monitoradas

### Aquisição
- **CTR** — taxa de cliques
- **CPL** — custo por lead
- **Leads/dia** — volume bruto
- **Taxa de resposta SDR** — qualidade da abordagem

### Conversão
- **MQL** — leads marketing-qualified
- **SQL** — leads sales-qualified
- **Taxa MQL → SQL**
- **Taxa SQL → venda**
- **Vendas/dia**

### Receita
- **Ticket médio**
- **Receita total**
- **MRR / ARR** (quando SaaS rodando)
- **Pipeline ponderado**

### Retenção
- **Churn rate**
- **LTV** (Lifetime Value)
- **NPS médio**
- **Health score por cliente**

---

## Thresholds (referências saudáveis)

| Métrica | Saudável | Alerta | Crítico |
|---------|----------|--------|---------|
| CTR | ≥1.5% | <1.5% | <1.0% |
| CPL | dentro da meta | +15% vs meta | +30% vs meta |
| Conversão SQL → venda | ≥10% | <10% | <7% |
| Churn mensal | <5% | 5–10% | >10% |
| NPS | >70 | 50–70 | <50 |
| Capacidade utilizada | ≤80% | 80–95% | >95% |
| LTV:CAC | >3x | 2–3x | <2x |
| Margem por projeto | >50% | 35–50% | <35% |

---

## Sistema de Alertas (3 níveis)

### Críticos → escalonar para CEO + Conselho
- CPL subiu >30% vs baseline
- Conversão SQL→venda caiu >20%
- Churn mensal subiu
- Receita caiu >15% vs mês anterior
- Capacidade utilizada >95%
- Runway abaixo de 3 meses

### Moderados → ajuste tático no Head responsável
- CTR baixo (< saudável por 3+ dias)
- Poucos SQL na semana
- NPS médio descendo
- Cliente sem interação há >7 dias
- Lead sem movimentação há >5 dias

### Leves → monitorar (sem ação imediata)
- Oscilação normal dentro do range
- Variação sazonal esperada
- Métrica fora do baseline por <24h

---

## Rotinas Diárias

### [08:00] Daily Heartbeat — Relatório Matinal
```yaml
agente: /pensare-inteligencia
foco: Controle operacional do dia
ler:
  - MEMORY.md
  - logs/events.ndjson (últimos 20 eventos)
  - memory/per-agent/pensare-comercial/pipeline.md
analisar:
  - Volume de entrada (leads gerados)
  - Qualidade de lead (resposta SDR, MQL/SQL)
  - Engajamento (conversas iniciadas)
  - Métricas-chave do dia anterior
acoes_condicionais:
  - se CTR baixo → acionar skill: creative-hook
  - se CPL alto → acionar skill: campaign-optimization
  - se poucos SQL → acionar skill: lead-qualification
  - se sem vendas → acionar skill: commercial-diagnosis
output:
  - memory/shared/daily-brief-{YYYY-MM-DD}.md
  - status_do_dia: [ok|atencao|critico]
  - problema_principal: <texto>
  - acao_imediata: <texto>
condition: executar se há eventos das últimas 24h ou projetos ativos
```

### [09:00] Pipeline Comercial
```yaml
agente: /pensare-comercial
foco: Saúde do pipeline
ler:
  - memory/per-agent/pensare-comercial/pipeline.md
analisar:
  - Quantos leads em cada etapa
  - Leads sem movimentação >5 dias
  - Propostas próximas de vencer
  - Probabilidade de bater meta com pipeline atual
output:
  - memory/per-agent/pensare-comercial/pipeline-review-{YYYY-MM-DD}.md
  - acao_recomendada_para_hoje: <texto>
```

### [16:00] Check de Customer Success
```yaml
agente: /pensare-cs
foco: Saúde dos clientes ativos
ler:
  - memory/shared/clients.md
  - MEMORY.md
identificar:
  - Clientes sem interação >7 dias
  - Health score abaixo da fase esperada
  - Entregas próximas do prazo sem confirmação
acoes:
  - Para casos de risco → acionar skill: churn-prevention
output:
  - Lista priorizada de follow-ups para 24h
```

### [18:00] Fechamento de Sessão
```yaml
agente: /pensare
foco: Encerramento do dia + preparação para amanhã
acoes:
  - Ler MEMORY.md atual
  - Ler últimos 30 eventos de logs/events.ndjson
  - Atualizar MEMORY.md com: o que foi feito, decisões tomadas, status atualizado, próximos passos
  - Registrar evento session_close em logs/events.ndjson
  - Se houver urgência → criar alerta em memory/shared/alerts.md
output:
  - MEMORY.md atualizado
  - logs/events.ndjson (+1 evento)
condition: executar se houver eventos no dia
```

---

## Rotinas Semanais

### [Segunda 08:30] Weekly Planning
```yaml
agente: /pensare-ceo
foco: Otimização tática + plano da semana
ler:
  - MEMORY.md
  - últimos 50 eventos
  - memory/shared/decisions.md
  - memory/shared/week-review-{semana-anterior}.md
produzir:
  - Revisão da semana anterior (entregue vs planejado)
  - 5 prioridades da semana em ordem de impacto
  - Para cada: responsável (agente) + critério de conclusão + risco principal
  - 1 pergunta estratégica para a Isis responder esta semana
output: memory/shared/week-plan-{YYYY-WNN}.md
```

### [Quarta 10:00] Inteligência de Mercado
```yaml
agente: /pensare-inteligencia
foco: Sinais e movimentações de mercado
acoes:
  - WebSearch: notícias IA aplicada a negócios Brasil (7d)
  - WebSearch: movimentações de concorrentes
  - Identificar 1 oportunidade não no radar
  - Identificar 1 ameaça competitiva
para_cada_item:
  - Fonte
  - Relevância para AI Systemizer (Alta/Média/Baixa)
  - Ação sugerida
output: memory/shared/market-intel-{YYYY-MM-DD}.md
```

### [Sexta 17:00] Weekly Review + Lições
```yaml
agente: /pensare-conselho
foco: Análise crítica + aprendizado
ler:
  - memory/shared/week-plan-{semana-atual}.md
  - todos eventos da semana
produzir:
  - % de execução (entregue vs planejado)
  - Principais desvios e por quê
  - 1 decisão que poderia ter sido melhor — aprendizado
  - 1 padrão positivo que deve ser replicado
  - Ajuste de rota para próxima semana
tom: analítico, sem condescendência, focado em aprendizado sistemático
output: memory/shared/week-review-{YYYY-WNN}.md
```

---

## Rotinas Mensais

### [Dia 1 do Mês, 09:00] Monthly Heartbeat — Estratégia
```yaml
agente: /pensare-financeiro
foco: Ajuste estratégico
ler:
  - Todos eventos do mês anterior
  - MEMORY.md
  - memory/per-agent/pensare-comercial/pipeline.md
analisar:
  - Receita do mês (MRR, novos contratos, expansão)
  - Pipeline próximo mês (probabilidade ponderada)
  - Unit economics (CAC, LTV, margem)
  - Crescimento vs mês anterior
  - Evolução do negócio (sistema melhorando ou piorando?)
acoes_condicionais:
  - se churn alto → skill: churn-retention
  - se margem baixa → skill: pricing-strategy
  - se crescimento travado → /pensare-ceo + /pensare-estrategia
output:
  - memory/shared/monthly-close-{YYYY-MM}.md
  - diagnostico_estrategico: <texto>
  - 3_decisoes_para_proximo_mes: [<a>, <b>, <c>]
```

### [Dia 15 do Mês, 09:00] Mid-Month Review — Produto e CS
```yaml
agente: /pensare-produto
foco: Saúde de produto e clientes
ler:
  - memory/shared/clients.md
  - Feedback acumulado do mês
produzir:
  - NPS médio dos clientes ativos (por projeto)
  - Top 3 feedbacks de produto
  - 1 problema recorrente → candidato a feature
  - Semáforo de saúde por cliente
  - 1 recomendação de evolução do AI Systemizer
output: memory/shared/mid-month-review-{YYYY-MM}.md
```

---

## Gatilhos por Evento (event-triggers)

Disparados **imediatamente** quando o evento é detectado.

### lead_captured → /pensare-sdr
```yaml
prompt: |
  Novo lead: {lead_data}
  Aplique skill: lead-qualification (BANT score 0–12)
  Produza:
    - Score 1–10 com justificativa
    - Fit com ICP (segmento, tamanho, estágio, orçamento, urgência)
    - Ação: qualificar-mais | agendar-diagnostico | desqualificar
    - Se qualificado: mensagem de primeiro contato
registrar: memory/per-agent/pensare-comercial/pipeline.md
```

### proposal_sent → /pensare-closer
```yaml
prompt: |
  Proposta enviada para {cliente}
  Configurar follow-up:
    - D+2: check de recebimento e dúvidas
    - D+5: follow-up com material de suporte
    - D+10: reunião de decisão se não houver retorno
  Criar rascunhos de email para cada touchpoint
registrar: memory/per-agent/pensare-comercial/pipeline.md
```

### client_inactive_7d → /pensare-cs
```yaml
prompt: |
  Cliente {cliente} sem registro de interação há 7 dias.
  Acionar skill: churn-prevention
  Avaliar:
    - Fase atual do projeto
    - Entregas pendentes
    - Histórico de engajamento
    - Risco de churn (Alto/Médio/Baixo)
    - Ação: touchpoint proativo | reunião de alinhamento | monitorar
  Se risco Alto: gerar rascunho de mensagem de reengajamento
```

### conversion_dropped → /pensare-comercial
```yaml
condition: conversão SQL→venda caiu >20% vs baseline (7d)
prompt: |
  Conversão caiu. Acionar skill: funnel-diagnosis
  Identificar onde está o vazamento:
    - Lead → MQL?
    - MQL → SQL?
    - SQL → proposta?
    - Proposta → fechamento?
  Gerar diagnóstico + plano de ação imediato
escalonar_se: queda >35% → notificar /pensare-ceo
```

### cpl_increased → /pensare-trafego
```yaml
condition: CPL >+30% vs baseline (3d)
prompt: |
  CPL subiu acima do threshold. Acionar skill: campaign-optimization
  Diagnosticar em 3 camadas:
    - Criativo (CTR, hook, oferta visual)
    - Landing page (taxa de conversão LP)
    - Oferta (clareza, ICP fit)
  Recomendar ajuste prioritário
escalonar_se: CPL +50% → /pensare-growth
```

### offer_not_converting → /pensare-produto
```yaml
condition: conversão de oferta <baseline por 14d
prompt: |
  Oferta atual não está convertendo. Acionar skill: offer-creation
  Revisar:
    - ICP atual ainda é o certo?
    - Promessa está alinhada com dor real?
    - Mecanismo é diferenciado?
    - Garantia é crível?
  Propor ajuste de oferta
```

### strategic_decision_required → /pensare-conselho
```yaml
prompt: |
  Decisão estratégica escalada: {decisao_contexto}
  Como Membro de Conselho, aplicar Decision Philosophy (7 perguntas):
    1. Isso fortalece o sistema?
    2. Isso aumenta previsibilidade?
    3. Isso preserva qualidade?
    4. Isso reduz dependência da founder?
    5. Isso melhora o Capital Digital?
    6. Isso respeita o posicionamento?
    7. Isso tem dados suficientes?
  Veredito: Alinhada | Ajustar | Bloquear
  Justificativa + risco + ajuste recomendado
  Se irreversível ou alto custo: consultar a Isis antes de executar
```

### financial_alert → /pensare-financeiro
```yaml
condition: CAC +30%, churn >10%, receita -15%, ou runway <3 meses
prompt: |
  Alerta financeiro: {alerta_contexto}
  Analisar:
    - Severidade (crítico/alto/médio)
    - Impacto no runway atual
    - Ação nas próximas 24h
    - Notificar Isis? (sim se crítico/alto)
  Enviar PushNotification com resumo de 3 linhas
```

### session_no_closing → /pensare
```yaml
condition: último evento do dia não é do tipo session_close
prompt: |
  Sessão sem fechamento detectada.
  Executar closing retroativo:
    - Ler últimos eventos
    - Atualizar MEMORY.md com o que pode ser inferido
    - Registrar session_close tardio
  Notificar Isis e pedir confirmação do contexto
```

---

## Acionamento por Skill (skill-routing automático)

| Skill | Acionada por | Quando |
|-------|-------------|--------|
| `creative-hook` | /pensare-criativos | CTR baixo, criativo cansado |
| `campaign-optimization` | /pensare-trafego | CPL subiu, ROAS caindo |
| `lead-qualification` | /pensare-sdr | Lead novo, qualificação BANT |
| `commercial-diagnosis` | /pensare-closer | Sem vendas, oferta travada |
| `objection-handling` | /pensare-closer | Lead com objeção registrada |
| `offer-creation` | /pensare-produto | Oferta não converte 14d+ |
| `pricing-strategy` | /pensare-financeiro | Margem baixa, churn por preço |
| `funnel-diagnosis` | /pensare-inteligencia | Conversão geral caindo |
| `churn-prevention` | /pensare-cs | Cliente inativo 7d, health score baixo |
| `positioning-messaging` | /pensare-estrategia | Diluição de categoria |

---

## Runtime do Heartbeat

### Daemon Python
- **Arquivo**: `heartbeat/daemon.py`
- **Frequência base**: verifica a cada 60s
- **Lê**: este arquivo (HEARTBEAT.md) + `heartbeat/state.json`
- **Decide**: `should_run(routine)` baseado em horário + última execução
- **Executa**: `subprocess` chamando `claude --print /agent {prompt}`
- **Registra**: cada execução em `heartbeat/state.json` + evento em `logs/events.ndjson`

### Scheduler (Mac launchd)
- **Arquivo**: `heartbeat/install.sh`
- **Plist**: `com.pensare.heartbeat.plist`
- **StartInterval**: 60 segundos
- **StandardOutPath**: `logs/heartbeat.log`
- **StandardErrorPath**: `logs/heartbeat-error.log`

### Comandos Operacionais
```bash
# Preview do que rodaria agora
python heartbeat/daemon.py --dry-run

# Executa uma vez (debug)
python heartbeat/daemon.py --once

# Daemon contínuo (foreground)
python heartbeat/daemon.py

# Instalar como LaunchAgent (Mac)
bash heartbeat/install.sh
```

---

## Log de Status do Heartbeat

| Rotina | Última execução | Status | Próxima |
|--------|----------------|--------|---------|
| Daily Brief (08:00) | nunca | pendente | depende de install.sh |
| Pipeline (09:00) | nunca | pendente | — |
| CS Check (16:00) | nunca | pendente | — |
| Closing (18:00) | nunca | pendente | — |
| Weekly Plan (seg 08:30) | nunca | pendente | — |
| Market Intel (qua 10:00) | nunca | pendente | — |
| Weekly Review (sex 17:00) | nunca | pendente | — |
| Monthly Close (dia 1) | nunca | pendente | — |
| Mid-Month Review (dia 15) | nunca | pendente | — |

**Para ativar todas as rotinas**: `bash setup.sh` e responder "s" à pergunta do heartbeat.

---

*Atualizar quando novos gatilhos forem identificados, thresholds forem recalibrados ou rotinas forem ajustadas.*
