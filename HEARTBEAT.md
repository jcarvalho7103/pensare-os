# HEARTBEAT.md — Rotinas Proativas do Pensare OS

> Define as rotinas automáticas e gatilhos de evento do sistema.
> O Pensare OS não espera ser chamado — ele antecipa, monitora e alerta.
> Runtime: Claude Code CLI com CronCreate para agendamento.

---

## Filosofia do Heartbeat

O sistema que só responde é um assistente. O sistema que antecipa é um OS.

O HEARTBEAT garante que mesmo em dias sem interação explícita da Isis, o Pensare OS:
1. Monitora o que importa
2. Registra o que muda
3. Alerta o que precisa de atenção
4. Prepara o contexto para a próxima sessão

---

## Rotinas Diárias

### [08:00] Relatório Matinal de Métricas
```
skill: /pensare-inteligencia
prompt: "Gere o relatório matinal do Pensare OS. Leia MEMORY.md e os últimos 20 eventos de logs/events.ndjson. Produza: (1) Resumo executivo em 3 bullets — o que mudou desde ontem; (2) Métricas do pipeline comercial se disponíveis; (3) Alertas — alguma métrica fora do padrão ou projeto sem movimentação há mais de 3 dias; (4) Sugestão de foco para hoje baseada nos projetos ativos. Formato: markdown limpo, máximo 1 página."
condition: "executar apenas se logs/events.ndjson tiver eventos das últimas 24h ou se MEMORY.md tiver projetos ativos"
output: "memory/shared/daily-brief-[YYYY-MM-DD].md"
```

---

### [09:00] Análise de Pipeline Comercial
```
skill: /pensare-comercial
prompt: "Analise o pipeline comercial. Leia memory/per-agent/comercial/pipeline.md. Responda: (1) Quantos leads estão em cada etapa do funil? (2) Algum lead sem movimentação há mais de 5 dias? (3) Há alguma proposta próxima de vencer? (4) Qual é a probabilidade de atingir a meta do mês com o pipeline atual? (5) Uma ação recomendada para hoje. Registre o resultado em memory/per-agent/comercial/pipeline-review-[YYYY-MM-DD].md"
condition: "executar apenas se memory/per-agent/comercial/pipeline.md existir e tiver conteúdo"
```

---

### [16:00] Check de Clientes Sem Atividade
```
skill: /pensare-cs
prompt: "Revise o status de todos os clientes ativos em MEMORY.md e memory/shared/clients.md. Identifique: (1) Clientes sem registro de interação há mais de 7 dias; (2) Clientes com health score abaixo do esperado para a fase do projeto; (3) Clientes com entrega próxima do prazo sem confirmação de progresso. Para cada caso, sugira uma ação de follow-up específica. Use a skill churn-prevention para os casos de risco. Output: lista priorizada de ações de CS para as próximas 24h."
condition: "executar apenas se houver clientes ativos em MEMORY.md"
```

---

### [18:00] Fechamento de Sessão
```
skill: /pensare
prompt: "Execute o fechamento de sessão do Pensare OS. (1) Leia MEMORY.md atual; (2) Leia os últimos 30 eventos de logs/events.ndjson; (3) Atualize MEMORY.md com: o que foi feito hoje, decisões tomadas, status atualizado dos projetos, próximos passos para amanhã; (4) Registre um evento de fechamento em logs/events.ndjson; (5) Se houver algo urgente para a Isis revisar amanhã cedo, crie um alerta em memory/shared/alerts.md. Seja conciso — o fechamento deve ser lido em menos de 2 minutos."
condition: "executar sempre que houver eventos no dia"
output: "atualização de MEMORY.md + evento em logs/events.ndjson"
```

---

## Rotinas Semanais

### [Segunda, 08:30] Planejamento da Semana
```
skill: /pensare-ceo
prompt: "Inicie o planejamento semanal. Leia MEMORY.md, os últimos 50 eventos de logs/events.ndjson, e memory/shared/decisions.md. Produza: (1) Revisão da semana anterior — o que foi entregue, o que ficou pendente; (2) Prioridades desta semana em ordem de impacto — máximo 5 itens; (3) Para cada prioridade: quem é responsável (qual agente), qual o critério de conclusão, qual o risco principal; (4) Uma pergunta estratégica que a Isis deveria responder esta semana. Salve em memory/shared/week-plan-[YYYY-WNN].md"
condition: "toda segunda-feira"
```

---

### [Sexta, 17:00] Revisão Semanal e Lições
```
skill: /pensare-conselho
prompt: "Execute a revisão semanal do Pensare OS. Leia o plano da semana em memory/shared/week-plan-[YYYY-WNN].md e os eventos da semana em logs/events.ndjson. Produza: (1) O que foi entregue vs. o que foi planejado — % de execução; (2) Principais desvios e por quê aconteceram; (3) Uma decisão que poderia ter sido melhor — o que aprendemos; (4) Um padrão positivo que deve ser replicado; (5) Ajuste de rota para a semana seguinte. Tom: analítico, sem condescendência, focado em aprendizado sistemático. Salve em memory/shared/week-review-[YYYY-WNN].md"
condition: "toda sexta-feira"
```

---

### [Quarta, 10:00] Inteligência de Mercado
```
skill: /pensare-inteligencia
prompt: "Execute o scan de inteligência de mercado semanal. Use WebSearch para: (1) Notícias sobre IA aplicada a negócios no Brasil — últimos 7 dias; (2) Movimentações de concorrentes diretos no segmento de consultoria/implementação de IA; (3) Uma oportunidade de mercado identificada que ainda não está no radar da Isis; (4) Uma ameaça competitiva que merece atenção. Para cada item: fonte, relevância para o AI Systemizer (Alta/Média/Baixa), ação sugerida. Salve em memory/shared/market-intel-[YYYY-MM-DD].md"
condition: "toda quarta-feira"
```

---

## Rotinas Mensais

### [Dia 1 do Mês, 09:00] Fechamento Mensal
```
skill: /pensare-financeiro
prompt: "Execute o fechamento mensal do Pensare OS. Leia todos os eventos do mês anterior em logs/events.ndjson, MEMORY.md, e memory/per-agent/comercial/pipeline.md. Produza: (1) Receita do mês — MRR, novos contratos, expansão; (2) Pipeline para o próximo mês — probabilidade ponderada; (3) Unit economics — CAC estimado, LTV médio dos clientes ativos; (4) Comparação com o mês anterior — crescimento %; (5) 3 decisões financeiras para o próximo mês. Salve em memory/shared/monthly-close-[YYYY-MM].md"
condition: "primeiro dia de cada mês"
```

---

### [Dia 15 do Mês, 09:00] Review de Produto e CS
```
skill: /pensare-produto
prompt: "Execute o mid-month review de produto e CS. Leia memory/shared/clients.md e feedback acumulado. Produza: (1) NPS médio dos clientes ativos — detalhamento por projeto; (2) Top 3 feedbacks de produto recebidos este mês; (3) Um problema recorrente que virou candidato a feature; (4) Status de saúde dos projetos em andamento — semáforo por cliente; (5) Uma recomendação de evolução do AI Systemizer baseada no que os clientes estão pedindo. Salve em memory/shared/mid-month-review-[YYYY-MM].md"
condition: "dia 15 de cada mês"
```

---

## Gatilhos por Evento

Os gatilhos abaixo são acionados **imediatamente** quando os eventos são detectados, não em horário fixo.

### Gatilho: Novo Lead Captado
```
event_type: "lead_captured"
skill: /pensare-sdr
prompt: "Um novo lead foi captado: {lead_data}. Aplique a skill lead-qualification com base no ICP definido em _contexto/empresa.md. Produza: (1) Score de qualificação (1-10) com justificativa; (2) Fit com ICP — dimensões: segmento, tamanho, estágio, orçamento estimado, urgência; (3) Ação recomendada — qualificar mais / agendar diagnóstico / desqualificar; (4) Mensagem de primeiro contato personalizada se qualificado. Registre resultado em memory/per-agent/comercial/pipeline.md"
```

---

### Gatilho: Proposta Enviada
```
event_type: "proposal_sent"
skill: /pensare-closer
prompt: "Uma proposta foi enviada para {cliente}. Configure follow-up automático: (1) D+2: check de recebimento e dúvidas; (2) D+5: follow-up com material de suporte; (3) D+10: reunião de decisão se não houve retorno. Crie os rascunhos de email para cada ponto. Registre o follow-up schedule em memory/per-agent/comercial/pipeline.md"
```

---

### Gatilho: Cliente Sem Interação há 7+ Dias
```
event_type: "client_inactive_7d"
skill: /pensare-cs
prompt: "O cliente {cliente} está sem registro de interação há 7 dias. Acione churn-prevention. Avalie: (1) Qual é a fase atual do projeto? (2) Havia entrega prevista que não foi confirmada? (3) Qual é o histórico de engajamento deste cliente? (4) Qual é o risco de churn neste momento (Alto/Médio/Baixo)? (5) Ação recomendada — touchpoint proativo, reunião de alinhamento, ou apenas monitorar. Gere rascunho de mensagem de reengajamento se necessário."
```

---

### Gatilho: Decisão Estratégica Necessária
```
event_type: "strategic_decision_required"
skill: /pensare-conselho
prompt: "Uma decisão estratégica foi escalada: {decisao_contexto}. Como Membro de Conselho, analise: (1) Qual é o impacto de longo prazo de cada opção? (2) Quais são os riscos de segunda ordem que não estão sendo considerados? (3) Esta decisão está alinhada com a missão do Pensare OS? (4) Recomendação clara com racional. Se a decisão for irreversível ou de alto custo, indique explicitamente e recomende consulta com a Isis antes de executar."
```

---

### Gatilho: Alerta Financeiro
```
event_type: "financial_alert"
skill: /pensare-financeiro
prompt: "Alerta financeiro detectado: {alerta_contexto}. Analise imediatamente: (1) Qual é a severidade — crítico/alto/médio? (2) Qual é o impacto no runway atual? (3) Que ação deve ser tomada nas próximas 24h? (4) Notificar a Isis? Envie PushNotification com resumo de 3 linhas se severidade for crítico ou alto."
condition: "sempre que CAC aumentar 30%+, churn superar 10%, ou receita cair 15%+ vs mês anterior"
```

---

### Gatilho: Sessão Sem Fechamento Registrado
```
event_type: "session_no_closing"
skill: /pensare
prompt: "Detectado que a última sessão não teve fechamento registrado. Execute closing retroativo: leia os últimos eventos de logs/events.ndjson, atualize MEMORY.md com o que pode ser inferido, registre evento de closing tardio. Notifique a Isis que o fechamento foi feito automaticamente e peça confirmação se o contexto está correto."
condition: "se o último evento do dia não for do tipo session_close"
```

---

## Configuração de Crons (Claude Code)

Para ativar os crons acima via CronCreate, use o /pensare-automacao com:

```bash
# Exemplo de ativação (executar via /pensare-automacao):
# CronCreate para relatório matinal:
# schedule: "0 8 * * *"
# command: "/pensare-inteligencia"
# args: "[prompt do relatório matinal]"
```

Status atual de ativação dos crons: **pendente configuração inicial pela operadora**.

---

## Log de Último Heartbeat por Rotina

| Rotina | Última execução | Status | Observação |
|--------|----------------|--------|------------|
| Relatório Matinal (08:00) | nunca | pendente | cron não configurado |
| Análise de Pipeline (09:00) | nunca | pendente | cron não configurado |
| Check de CS (16:00) | nunca | pendente | cron não configurado |
| Fechamento (18:00) | nunca | pendente | cron não configurado |
| Planejamento Semanal (seg) | nunca | pendente | cron não configurado |
| Revisão Semanal (sex) | nunca | pendente | cron não configurado |
| Inteligência de Mercado (qua) | nunca | pendente | cron não configurado |

---

*Atualizar quando novos gatilhos forem identificados ou rotinas forem ajustadas.*
*Para ativar crons: instrua /pensare-automacao com os horários desejados.*
