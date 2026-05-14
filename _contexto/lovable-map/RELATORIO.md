# Mapeamento Completo — Pensare OS Lovable

> Fonte: https://pensare-os.lovable.app/
> Data: 2026-05-13
> Objetivo: documentar tudo que existe no Pensare OS Lovable para informar a evolução do sistema local em `/Users/alicycarvalho/pensare-os/`

---

## Visão Geral

O Pensare OS hospedado no Lovable está organizado em **11 guias** principais. Cada guia (exceto Dashboard, Tasks e Chat) usa o mesmo padrão: lista de arquivos `.md` à esquerda + painel de conteúdo à direita.

| Guia | Descrição | Quantidade de docs |
|------|-----------|--------------------|
| Dashboard | Estado do sistema em tempo real (métricas operacionais) | — |
| Core | Componentes centrais que orquestram o sistema | 4 nós |
| Orchestrator | Fluxo, decisão, execução, aprendizado entre agents | 16 arquivos |
| Agents | Organograma vivo (17 agentes) | 17 agents |
| Skills | Manual operacional vivo (unidades de inteligência reutilizáveis) | 10 skills |
| Memory | Aprendizado, registro, evolução contínua | 17 arquivos |
| Heartbeats | Ritmo, monitoramento, ajuste contínuo | 13 arquivos |
| Tools | Sistema de integração e execução | 15 arquivos |
| Soul | Essência, filosofia, princípios de decisão | 7 arquivos |
| Tasks | Kanban (Pendente/Em Execução/Concluído) | 33+ tasks reais |
| Chat | Conversa 1:1 ou grupo com agentes | 3 conversas existentes |

---

## 1. Dashboard

**Métricas operacionais monitoradas:**
- Leads hoje
- SQL (Sales Qualified Leads)
- Vendas
- Receita
- CPL (Custo Por Lead)
- Conversão

**Painéis visíveis:**
- Gráfico "Leads & Receita — últimos 14 dias"
- Lista "Em execução" (tasks ativas)
- "Heartbeats recentes"

**Estado atual**: vazio (sem dados em `metrics_daily`).

---

## 2. Core

4 nós centrais:

### 2.1 Orchestrator
**Função**: Cérebro operacional. Garante que cada evento gere a ação correta, no agente correto, no momento certo.

**Responsabilidades**:
- Interpretar eventos
- Direcionar ações
- Manter ordem lógica
- Garantir execução contínua
- Alimentar aprendizado (memory)

**Limites**:
- Não cria estratégia
- Não executa tarefas
- Não decide sozinho fora da hierarquia

### 2.2 System Flow
Macro fluxo operacional do negócio.

### 2.3 Decision Engine
Classifica decisões em 4 níveis: Operacional, Tático, Estratégico, Crítico. Regra: sempre decidir no menor nível possível.

### 2.4 State Machine
Controla estados do sistema e de cada fluxo (lead, deal, cliente, projeto).

**Estados típicos**: idle, routing, executing, waiting, done, failed.

---

## 3. Orchestrator (16 arquivos)

`system-flow.md, execution-flow.md, agent-hierarchy.md, event-triggers.md, decision-engine.md, task-engine.md, state-machine.md, skills-routing.md, routing-rules.md, priority-rules.md, escalation-rules.md, validation-rules.md, orchestrate.md, decision-routing.md, README.md, CLAUDE.md`

### Highlights estratégicos

**system-flow.md** (fluxo macro):
1. Lead entra → 2. SDR qualifica → 3. Closer diagnostica → 4. Venda → 5. Operações entrega → 6. CS acompanha → 7. Dados analisa → 8. Growth otimiza → 9. CEO ajusta → 10. Board valida

**Feedback Loop**: Dados IA → Memory → ajusta Oferta + Criativo + Comercial → sistema evolui continuamente.

**execution-flow.md**:
- Lead entrou → SDR (Skill: lead-qualification)
- SQL → Closer; MQL → Nutrição; Desqualificado → Encerrar
- Closer (Skills: commercial-diagnosis, objection-handling)
- Operações → Onboarding → Entrega inicial
- CS (Skill: churn-retention)
- Dados → Registra conversão, gargalos, padrões
- Growth (Skills: creative-hook, campaign-optimization)

**event-triggers.md** (eventos → reações):
- Lead entrou → SDR
- Lead qualificado → Closer
- Venda → Operações
- Conversão caiu → Funnel Diagnosis
- CPL subiu → Campaign Optimization
- Cliente parou → Churn Prevention
- Oferta não converte → Offer Creation
- Risco detectado → CEO / Board

**escalation-rules.md**:
- Operacional → Growth
- Tático → Head
- Estratégico → CEO
- Crítico → Board

**priority-rules.md**: Receita > Conversão > Qualidade > Volume. **Nunca escalar volume sem conversão**.

**validation-rules.md**: Toda ação precisa de Métrica + Objetivo + Responsável. Sem isso, não executa.

---

## 4. Agents (17 agentes — organograma)

### Conselho / C-Suite
| # | Agente | Tier | Função |
|---|--------|------|--------|
| 1 | Membro do Conselho | Head | Avalia decisões antes da execução |
| 2 | CEO IA | Head | Traduz visão da Founder + diretrizes do Board |

### Heads (L1)
| # | Agente | Função resumida |
|---|--------|-----------------|
| 3 | Head de Growth IA | Gera leads qualificados com previsibilidade |
| 4 | Head Comercial IA | Converte leads qualificados em receita previsível |
| 5 | Head de Operações IA | Garante entrega com qualidade e consistência |
| 6 | Head Financeiro IA | Saúde financeira, caixa, sustentabilidade |
| 7 | Head de Produto / Oferta IA | Cria e evolui ofertas que convertem |
| 8 | Head de Customer Success IA | Retenção, evolução, expansão |
| 9 | Head de Estratégia / Category Design IA | Categoria, narrativa, diferenciação |
| 10 | Head de Automação / Sistemas IA | Transforma processos em sistemas automatizados |
| 11 | Head de Inteligência de Mercado IA | Oportunidades, concorrência, mercado |

### Executores (L1)
| # | Agente | Função |
|---|--------|--------|
| 12 | SDR IA (Mariana) | Inicia conversa, diagnostica, qualifica |
| 13 | Closer IA | Diagnóstico, objeção, fechamento |
| 14 | Tráfego IA | Campanhas, CPL, escala |
| 15 | Copy IA | Mensagens que atraem, filtram, convertem |
| 16 | Criativos IA | Vídeos, imagens, ideias visuais |
| 17 | Dados IA | Performance, padrões, decisão data-driven |

### Estrutura interna de cada agent (padrão observado)
```
pensare-{role}-agent/
├── README.md
├── CLAUDE.md
├── agent/
│   ├── identity.md
│   ├── decision-framework.md (ou skills.md)
│   ├── governance-rules.md (ou rules.md)
│   ├── output-format.md
│   └── examples.md
└── prompts/
    └── {role}-action.md
```

### Exemplo concreto — Board Member IA

**README.md**: "Agente de Conselho Estratégico da Pensare Digital. Avalia, não executa. Função: determinar se uma decisão fortalece ou enfraquece o sistema da empresa."

**Pergunta central**: "Essa decisão fortalece ou enfraquece o sistema da Pensare Digital?"

**Atua em**: Governança, Estratégia, Gestão, Risco, Sustentabilidade, Coerência sistêmica.

**Nunca faz**: campanha, copy operacional, SDR, tráfego, CRM, decisão sem analisar riscos.

---

## 5. Skills (10 skills)

| # | Categoria | Skill | Descrição |
|---|-----------|-------|-----------|
| 1 | marketing | Campaign Optimization | Otimiza campanhas (CPL, conversão, escala) |
| 2 | marketing | Creative & Hook Creation | Criativos e hooks que capturam ICP |
| 3 | marketing | Positioning & Messaging | Clareza, diferenciação, percepção de valor |
| 4 | customer-success | Churn Prevention & Retention | Reduz churn, aumenta LTV |
| 5 | commercial | Commercial Diagnosis | Gargalo real (oferta/aquisição/conversão/operação/sistema) |
| 6 | commercial | Funnel Diagnosis | Maior vazamento entre aquisição → retenção |
| 7 | commercial | Lead Qualification | SQL / MQL / Desqualificado |
| 8 | commercial | Objection Handling | Investiga e destrava objeções sem confronto |
| 9 | commercial | Offer Creation | Cria/ajusta ofertas de alta conversão |
| 10 | commercial | Pricing Strategy | Preço por valor, não por custo |

**Nota**: a página de detalhe individual de cada skill no Lovable ainda não está implementada (carrega o listing).

---

## 6. Memory (17 arquivos)

`README.md, CLAUDE.md, memory-system.md, data-structure.md, learning-loop.md, update-rules.md, icp-real.md, objections.md, winning-offers.md, best-creatives.md, funnel-insights.md, pricing-insights.md, churn-insights.md, campaign-patterns.md, register-learning.md, retrieve-insight.md, update-memory.md`

### Tipos de memória (memory-system.md)

| Camada | Categorias |
|--------|-----------|
| **Operacional** | Leads, Conversas, Vendas |
| **Estratégica** | ICP, Oferta, Posicionamento |
| **Otimização** | Criativos, Campanhas, Conversão |
| **Retenção** | Churn, Evolução de clientes |

**Regra**: tudo que se repete vira padrão.

### Learning Loop
Evento → Execução → Resultado → Registro → Padrão → Ajuste → ajusta (Oferta, Criativo, Comercial, Estratégia).

### Update Rules
**Registrar quando**: algo deu muito certo / muito errado / padrão se repetiu / métrica saiu do normal.
**Não registrar**: ruído, evento isolado sem relevância.

### Pergunta central
"O que o sistema aprendeu com isso?"

---

## 7. Heartbeats (13 arquivos)

`daily.md, weekly.md, monthly.md, metrics.md, alerts.md, thresholds.md, escalation.md, cadence.md, run-daily.md, run-weekly.md, run-monthly.md, README.md, CLAUDE.md`

### Cadência

| Ritmo | Foco | Métricas | Ações típicas |
|-------|------|----------|---------------|
| **Daily** | Execução | Leads, conversas, taxa-resposta SDR, SQL, vendas, CPL, CTR | CTR baixo→creative-hook · CPL alto→campaign-optimization · Poucos SQL→lead-qualification · Sem vendas→commercial-diagnosis |
| **Weekly** | Otimização tática | Conversão geral, MQL→SQL, SQL→venda, CAC, receita semanal | Conversão baixa→funnel-diagnosis · Oferta→offer-creation · Objeções→objection-handling |
| **Monthly** | Estratégia | Receita, crescimento, margem, LTV, churn | Churn→churn-retention · Margem→pricing-strategy · Crescimento travado→CEO+Strategy |

### Alerts
- **Crítico**: CPL >+30%, conversão -20%, churn alto → CEO
- **Moderado**: CTR baixo, poucos SQL → ajuste tático
- **Leve**: oscilação normal → monitorar

### Thresholds de referência
- CTR ideal: 1.5%
- Conversão SQL → venda: 10%

### Pergunta central
"O sistema está melhorando ou piorando?"

---

## 8. Tools (15 arquivos)

`tools-system.md, integration-principles.md, data-sync.md, error-handling.md, ghl.md, whatsapp.md, meta-ads.md, google-sheets.md, webhooks.md, analytics.md, choose-tool.md, execute-action.md, debug-tool.md, README.md, CLAUDE.md`

### Stack atual (módulos)

| Tool | Função | Quem usa | Regra |
|------|--------|---------|-------|
| **GHL (Go High Level)** | CRM e automação central | SDR, Closer, CS | Todo lead deve existir no GHL |
| **WhatsApp** | Comunicação direta | SDR, Closer, Suporte | Respostas rápidas, humanas, sem spam |
| **Meta Ads** | Aquisição de leads | Tráfego | Nunca escalar campanha não validada |
| **Google Sheets** | Armazenamento + análise | Dados, Operações | Organizados e atualizados |
| **Webhooks** | Integração entre sistemas | Automação | Eventos devem disparar ações |
| **Analytics** | Monitoramento de performance | Dados, Heads | Decisão baseada em dados |

### Princípios de integração (core)
1. Simplicidade — evitar ferramentas desnecessárias
2. Conectividade — tudo se comunica
3. Rastreabilidade — toda ação rastreável
4. Automação — automatizar o repetitivo
5. Controle — permitir intervenção manual

**Pergunta central**: "Qual ferramenta executa isso com mais eficiência?"

---

## 9. Soul (7 arquivos)

`mission.md, principles.md, non-negotiables.md, decision-philosophy.md, brand-voice.md, soul-check.md, README.md`

### Missão (mission.md)
> A missão da Pensare Digital é transformar **conhecimento, serviço e expertise em Capital Digital**.
>
> A Pensare ajuda empresas que já possuem valor real, mas ainda dependem de indicação, improviso comercial ou tráfego isolado, a construir sistemas previsíveis de aquisição, conversão, entrega e crescimento.
>
> A Pensare não vende apenas marketing. **A Pensare estrutura sistemas de crescimento.**

### Os 8 Princípios
1. **Sistema antes de volume** — nunca escalar tráfego antes de validar oferta, conversão e capacidade
2. **Fit antes de venda** — nem todo lead deve virar cliente
3. **Valor antes de preço** — não competimos por preço
4. **Clareza antes de complexidade** — se precisa explicar demais, está confuso
5. **Dados antes de opinião** — evidência, não ansiedade ou ego
6. **Qualidade antes de escala** — escalar frágil acelera o problema
7. **Capital Digital antes de marketing isolado** — ativo, não campanha
8. **Evolução contínua** — toda execução gera aprendizado

### Non-Negotiables (a Pensare NUNCA deve)
- Vender para lead sem fit
- Escalar campanha sem qualidade de lead
- Prometer resultado impossível
- Reduzir preço para compensar falta de valor percebido
- Criar oferta genérica
- Ignorar gargalo de entrega
- Crescer com prejuízo invisível
- Automatizar processo ruim
- Tratar lead como número
- Ignorar sinais de churn
- Tomar decisão crítica sem dados
- Copiar concorrente como estratégia
- Virar commodity

### Decision Philosophy — 7 perguntas para toda decisão
1. Isso fortalece o sistema?
2. Isso aumenta previsibilidade?
3. Isso preserva qualidade?
4. Isso reduz dependência da founder?
5. Isso melhora o Capital Digital?
6. Isso respeita o posicionamento?
7. Isso tem dados suficientes?

**Regra final**: se a decisão gera crescimento mas enfraquece o sistema, deve ser ajustada ou bloqueada.

### Brand Voice
Estratégica · Direta · Segura · Clara · Consultiva · Profunda sem ser complicada · Provocativa sem ser agressiva · Sofisticada sem ser distante.

**Tom**: A Pensare não grita. **A Pensare diagnostica.**

**Frases-modelo**:
- "Você não precisa de mais tráfego. Você precisa de um sistema que transforme atenção em receita."
- "Venda previsível não nasce de campanha isolada. Nasce de oferta, aquisição, conversão e operação funcionando juntas."
- "O problema não é falta de lead. É falta de sistema."

**NÃO usar**: "Ganhe dinheiro rápido", "Fórmula secreta", "Método milagroso", "Marketing que vende no automático sem esforço", "Últimas vagas só hoje" (sem verdade operacional).

---

## 10. Tasks (Kanban real — 33+ tasks)

O Kanban tem 3 colunas (Pendente / Em execução / Concluído) e contém **tasks reais da operação atual da Pensare**, mostrando o estado estratégico do negócio.

### Foco atual identificado (das tasks)

**Iniciativa principal**: AI Systemizer (MVP em validação + escala controlada)
- 1º cliente MVP fechado ✓
- 1º onboarding em curso (Workshop de Co-criação)
- Closer focado em fechar +2 MVPs
- Board aprovou escala controlada
- CEO coordenando estratégia de escala

**Segunda iniciativa em avaliação**: SaaS de Posicionamento e Oferta
- Ticket alvo: R$ 5k + recorrência
- ICP alvo: "expert"
- Board solicitou plano de viabilidade em 10 dias úteis
- Heads envolvidos: Estratégia, Produto, Inteligência de Mercado, Financeiro, Automação
- Tasks pendentes: arquitetura/tecnologia, projeção financeira, mapeamento ICP, proposta de valor

### Tasks marcadas como URGENT
- Refinar proposta "Sistema Operacional IA-first" (CEO IA)

### Tasks HIGH
- Definir Arquitetura e Tecnologia para MVP do SaaS (Head de Automação)
- Análise Financeira e Modelo de Precificação do SaaS (Head Financeiro)
- Mapear ICP e Análise de Mercado para SaaS (Head de Inteligência)
- Avaliar Estrutura e Escopo do SaaS (Head de Produto)
- Monitoramento Financeiro AI Systemizer em Escala
- Plano de Marketing e Aquisição para Escala do AI Systemizer
- Estratégia de Escala do AI Systemizer (CEO)
- Otimização da Oferta AI Systemizer para Escala

### Tasks Concluídas
- Revisão do Board para "AI Systemizer" concluída
- Primeiro cliente MVP "AI Systemizer" fechado
- Avaliação de Projeto "Soluções IA para Experts"

---

## 11. Chat

3 conversas existentes: "First OS", "Novo Saas", "Pensare". É um chat 1:1 ou em grupo com agentes do Pensare OS.

---

## Insights Estratégicos Descobertos

### Sobre a operação atual da Pensare
1. **AI Systemizer está em fase de validação MVP** → 1 cliente fechado, +2 em pipeline, Board já aprovou escala controlada
2. **Segundo produto em avaliação**: SaaS de Posicionamento e Oferta (R$ 5k + recorrência) — risco de canibalização da consultoria mapeado
3. **ICP do segundo produto**: "expert" — diferente do ICP atual (PMEs de serviço B2B)
4. **Operação multi-agent já é prática real** — não é só conceito; as tasks são distribuídas e executadas por agentes

### Sobre arquitetura
- **Padrão de cada agent**: identity + decision-framework + governance-rules + output-format + examples + prompts/{role}-action
- **Carga padrão observada no Lovable**: Soul + Orchestrator + Memory + Heartbeats + Tools (5 sistemas core)
- **A "Carga Padrão" do conceito original (AGENTS/SOUL/TOOLS/IDENTITY/HEARTBEAT/MEMORY/SKILLS) está parcialmente implementada** — falta IDENTITY como sistema próprio e SKILLS está em fase listing-only

### Sobre vocabulário e posicionamento
- **A marca real é "Pensare Digital"** (não só "Pensare OS")
- **Conceito central**: "Capital Digital" (transformar conhecimento em ativo)
- **Categoria criada**: "Capital Digital" — mais ampla que "Systemização de IA"
- **Brand voice**: "A Pensare não grita. A Pensare diagnostica."

### Gaps observados no Lovable
1. Skills não tem página de detalhe (só cards)
2. Dashboard sem dados conectados
3. Memória estruturada, mas sem ingestão de dados reais visível
4. Heartbeats descritos mas não automatizados (sem cron/daemon visível)

---

## O Que Replicar do Lovable no Pensare OS Local

### Diretamente aplicável
- [x] Os 8 Princípios → atualizar `SOUL.md`
- [x] Os 13 Non-Negotiables → atualizar `SOUL.md`
- [x] As 7 perguntas de Decision Philosophy → adicionar ao `SOUL.md`
- [x] Brand Voice completa → atualizar `IDENTITY.md`
- [x] Fluxo macro de 10 etapas (system-flow) → adicionar ao `AGENTS.md`
- [x] Event triggers → mapear no `HEARTBEAT.md`
- [x] Tipos de memória (operacional/estratégica/otimização/retenção) → estruturar `memory/`
- [x] Stack de Tools (GHL, WhatsApp, Meta Ads, Sheets, Webhooks, Analytics) → atualizar `TOOLS.md`
- [x] Estrutura interna padrão de cada agent → padronizar SKILL.md dos agentes
- [x] Os 17 agents com hierarquia → já implementado no local

### A evoluir além do Lovable (nosso local)
1. **Skills com profundidade real** (já temos 10 SKILLs completos com frameworks)
2. **Heartbeat automatizado** (já temos daemon.py + launchd)
3. **Dashboard com dados reais conectados** (já temos FastAPI + endpoints)
4. **Memória estruturada em arquivos** (Letta-inspired) com NDJSON log
5. **Reflexão por agente** (memory/per-agent/{name}/reflections.md)
6. **Cost discipline** (10/20/70 tier budget)

---

## Arquivos do Mapeamento

Todos os outputs brutos estão em `_contexto/lovable-map/`:
- `orchestrator-map.txt`
- `agents-overview.txt`, `agents-detail.txt` (81KB — conteúdo completo dos 17 agents)
- `memory-map.txt`
- `heartbeats-map.txt`
- `tools-map.txt`
- `soul-detail.txt`
- `tasks-map.txt`
- `chat-map.txt`

---

*Mapeamento gerado via Playwright MCP em 2026-05-13*
