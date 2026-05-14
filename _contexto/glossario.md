# Glossário do Pensare OS

> Definições canônicas dos termos usados pelo sistema.
> Quando um agente usa esses termos, usa-os com este significado — sem ambiguidade.
> Atualizar sempre que um novo termo relevante for introduzido.

---

## Termos de Negócio (Siglas e Conceitos Comerciais)

### ARR (Annual Recurring Revenue)
Receita recorrente anualizada. Para o AI Systemizer: soma de todos os contratos de retainer anuais ou renovações esperadas. Diferente de MRR × 12 quando há sazonalidade. Indicador de saúde de longo prazo do negócio.

### ASP (Average Selling Price)
Preço médio de venda. Para o AI Systemizer: valor médio dos contratos fechados em um período. Métrica monitorada pelo Head Comercial para avaliar se o posicionamento está sendo executado corretamente.

### BEP (Break-Even Point / Ponto de Equilíbrio)
Nível de receita onde custos totais = receita total. Abaixo do BEP, o negócio opera no prejuízo. Métrica financeira crítica monitorada pelo Head Financeiro.

### CAC (Customer Acquisition Cost)
Custo de aquisição de cliente. Fórmula: total investido em marketing + vendas no período ÷ número de novos clientes adquiridos no mesmo período. Para o AI Systemizer, inclui: tempo da Isis em prospecção, custo de tráfego pago, ferramentas de marketing.

### CAGR (Compound Annual Growth Rate)
Taxa de crescimento anual composta. Usada para projetar crescimento de mercado ou receita ao longo de vários anos. Ex: "mercado de IA no Brasil cresce 30% CAGR" significa que o mercado dobra a cada ~3 anos.

### Churn Rate
Taxa de cancelamento ou perda de clientes. Mensal: % de clientes que encerraram contrato no mês. Para projetos únicos: taxa de clientes que não renovam ou não voltam. Monitorado pelo Head de CS.

### CPL (Cost Per Lead)
Custo por lead gerado. Total investido em aquisição ÷ número de leads gerados. Monitorado pelo Head de Growth e Gestor de Tráfego.

### CRM (Customer Relationship Management)
Sistema de gestão de relacionamento com clientes. No contexto do Pensare OS: ferramenta usada para registrar pipeline, interações e histórico de cada lead/cliente. O Pensare OS complementa (não substitui) o CRM da Isis.

### GTM (Go-to-Market)
Estratégia de entrada no mercado. Define como o produto é apresentado, para quem, por qual canal e com qual mensagem. O GTM do AI Systemizer é definido pelo CEO Agent em conjunto com Growth e Comercial.

### ICP (Ideal Customer Profile)
Perfil do cliente ideal. Combinação de critérios demográficos (segmento, tamanho, faturamento) e psicográficos (maturidade, mindset, gatilhos) que define quem o AI Systemizer serve melhor. Documentado em `_contexto/empresa.md`. Usado pela skill `lead-qualification`.

### LTV (Lifetime Value / Customer Lifetime Value)
Valor total gerado por um cliente durante todo o relacionamento com o negócio. Para o AI Systemizer: valor do projeto inicial + expansões + renovações + indicações (quando calculado com attribution). Monitorado pelo Head Financeiro.

### LTV:CAC Ratio
Razão entre LTV e CAC. Métrica de eficiência de aquisição. Meta saudável: LTV:CAC > 3x. Abaixo de 1x: o cliente custa mais do que vale. Monitorado mensalmente pelo Head Financeiro.

### MQL (Marketing Qualified Lead)
Lead qualificado pelo marketing. Demonstrou interesse (baixou material, assistiu webinar, engajou com conteúdo) mas ainda não foi contatado pelo comercial. Passa para SQL após triagem do SDR.

### MRR (Monthly Recurring Revenue)
Receita recorrente mensal. Para o AI Systemizer: soma dos valores de contratos de retainer ativos no mês. Se a maioria são projetos únicos, usar "receita mensal" como proxy.

### NPS (Net Promoter Score)
Métrica de satisfação e lealdade do cliente. Pergunta: "De 0 a 10, quanto você recomendaria a Pensare OS a um colega?" Promotores (9-10) − Detratores (0-6) = NPS. Meta: NPS > 50. Monitorado pelo Head de CS.

### ROAS (Return on Ad Spend)
Retorno sobre investimento em anúncios. Receita gerada por campanhas ÷ valor investido em anúncios. Ex: ROAS de 3x = para cada R$ 1 em anúncio, R$ 3 em receita. Monitorado pelo Gestor de Tráfego.

### Runway
Quantos meses o negócio consegue operar com o caixa atual sem novas receitas. Calculado como: caixa disponível ÷ custo fixo mensal. Monitorado pelo Head Financeiro. Alerta quando runway < 3 meses.

### SLA (Service Level Agreement)
Acordo de nível de serviço. Define prazos e padrões de qualidade comprometidos com o cliente. Ex: "entrega do diagnóstico em até 10 dias úteis". Definido e monitorado pelo Head de Operações.

### SOM (Serviceable Obtainable Market)
Ver mercado endereçável obtível — a fatia do SAM que o Pensare OS pode realisticamente capturar dado sua capacidade e recursos. Documentado em `_contexto/mercado.md`.

### SAM (Serviceable Addressable Market)
Mercado endereçável atendível — a parte do TAM que o Pensare OS pode servir dado seu modelo de negócio e capacidade atual.

### SQL (Sales Qualified Lead)
Lead qualificado para vendas. Passou pela triagem do SDR, atende ao ICP e tem interesse e budget para avançar. É passado para o Closer para a reunião de diagnóstico.

### TAM (Total Addressable Market)
Mercado total endereçável — o tamanho máximo do mercado se 100% dos clientes potenciais fossem atendidos. Referência para avaliar potencial de crescimento do nicho.

### Unit Economics
Métricas que avaliam a rentabilidade por unidade de negócio (por cliente, por projeto). Inclui: CAC, LTV, ticket médio, margem por projeto, payback period.

---

## Termos do Sistema Pensare OS

### Agente
Uma instância especializada do Claude Code com prompt, identidade, responsabilidades e acesso a ferramentas definidos. O Pensare OS tem 17 agentes organizados em 4 tiers. Cada agente é chamado via comando `/pensare-[nome]`.

### AI Systemizer
Produto principal da Pensare OS. Implementação consultiva de um sistema operacional de IA customizado para empresas de serviço. Entregável: arquitetura de agentes funcionando + documentação + treinamento da equipe.

### Archival Memory
Tipo de memória de longo prazo no Pensare OS, inspirado na arquitetura Letta. Armazenado em `memory/shared/` e `memory/per-agent/`. Não é carregado automaticamente — é consultado por demanda quando o agente precisa de contexto histórico específico.

### Boot Sequence
Sequência de inicialização do Pensare OS definida em CLAUDE.md. Cinco passos obrigatórios que todo agente deve executar ao iniciar uma sessão: (1) carregar SOUL.md e IDENTITY.md, (2) ler logs recentes, (3) carregar MEMORY.md, (4) carregar contexto de negócio se necessário, (5) exibir status do sistema.

### C-Suite
Tier 1 do Pensare OS: /pensare-conselho e /pensare-ceo. Responsáveis por decisões estratégicas e executivas. Operam com baixo volume de tokens (10% da alocação) e alto impacto de decisão.

### Capital Digital
O ativo intangível criado quando conhecimento é codificado em sistemas que operam de forma autônoma. O objetivo central da missão do Pensare OS: transformar o que a Isis e seus clientes sabem em sistemas que trabalham por eles.

### Carga Padrão
Conjunto mínimo de arquivos carregados em toda sessão: SOUL.md + IDENTITY.md + MEMORY.md + tail dos eventos. É o contexto base que garante coerência entre sessões.

### Coordinator
O agente `/pensare` — ponto de entrada obrigatório de toda sessão. Faz triagem da intenção da operadora, roteia para o agente correto, e sintetiza resultados quando múltiplos agentes são usados.

### Core Memory
Tipo de memória imutável no Pensare OS: SOUL.md e IDENTITY.md. Carregada em toda sessão, nunca sobrescrita sem autorização explícita da operadora. Define identidade e valores do sistema.

### Event Log
O arquivo `logs/events.ndjson` — registro append-only de todos os eventos do sistema. Cada linha é um JSON com: timestamp, agente, tipo do evento, resumo e payload. É a "memória episódica" do Pensare OS.

### Handoff
Transferência de trabalho entre agentes. Tem formato definido (frontmatter YAML em AGENTS.md). Pode ser upward (para tier superior), downward (para execução) ou lateral (mesmo tier via Coordinator).

### Handoff Contract
O frontmatter YAML padronizado usado em toda transferência entre agentes. Inclui: origem, destino, prioridade, contexto, entregável, decisão necessária (se aplicável), deadline.

### Head
Agentes de Tier 2 do Pensare OS: /pensare-growth, /pensare-comercial, /pensare-operacoes, /pensare-financeiro, /pensare-produto, /pensare-cs, /pensare-estrategia, /pensare-automacao, /pensare-inteligencia. Responsáveis por áreas funcionais do negócio.

### Heartbeat
As rotinas proativas do Pensare OS definidas em HEARTBEAT.md. Conjunto de execuções agendadas (crons) e gatilhos por evento que mantêm o sistema operando mesmo sem interação da Isis.

### NDJSON (Newline Delimited JSON)
Formato de arquivo onde cada linha é um JSON válido. Usado em `logs/events.ndjson`. Permite append eficiente e leitura de eventos individuais sem parsear o arquivo inteiro.

### Pensare OS
O sistema operacional de IA construído pela Isis Carvalho. Uma arquitetura de 17 agentes especializados rodando sobre Claude Code CLI. Serve como sistema de operação da própria Isis E como demonstração do que o AI Systemizer entrega para clientes.

### Pipeline
No contexto comercial: o conjunto de oportunidades em diferentes etapas do processo de vendas. Gerenciado pelo Head Comercial e monitorado pelo Coordinator no heartbeat diário.

### Recall Memory
Tipo de memória de curto/médio prazo no Pensare OS: o arquivo MEMORY.md. Contém o estado da sessão atual, projetos ativos, decisões em aberto. Atualizado ao fim de cada sessão.

### Runtime
O ambiente de execução do Pensare OS: Claude Code CLI. Sem OpenClaw, sem Paperclip, sem servidor próprio. Roda localmente no ambiente da operadora.

### Skill
Prompt reutilizável para tarefas específicas. O Pensare OS tem 10 skills: lead-qualification, commercial-diagnosis, objection-handling, offer-creation, positioning-messaging, creative-hook, campaign-optimization, funnel-diagnosis, pricing-strategy, churn-prevention. Skills são chamadas pelos agentes, não diretamente pela operadora.

### Systemização
O processo de codificar o conhecimento e os processos de uma empresa em sistemas que operam de forma autônoma e replicável. Diferente de automação (que conecta tarefas), systemização cria uma arquitetura operacional.

### Tier
Nível hierárquico no Pensare OS. Tier 0: Coordinator. Tier 1: C-Suite. Tier 2: Heads. Tier 3: Execution. A hierarquia define responsabilidades, escalonamento de decisões e alocação de custo de tokens.

---

## Termos de Marketing e Growth

### Hook
Elemento inicial de um criativo ou copy que captura a atenção em menos de 3 segundos. Criado pela skill `creative-hook`. Crítico para performance de anúncios e conteúdo orgânico.

### Funil
A jornada do lead desde a descoberta até o fechamento. Para o AI Systemizer: Descoberta → Interesse → Qualificação → Diagnóstico → Proposta → Fechamento → Onboarding. Cada etapa tem agente responsável e métrica de conversão.

### Sequência de Nutrição
Série de emails ou mensagens enviados ao longo do tempo para educar e engajar leads que ainda não estão prontos para comprar. Criada pelo /pensare-copy e operada pelo /pensare-sdr.

### Ângulo Criativo
O ponto de vista ou abordagem específica de um anúncio ou conteúdo. Ex: "dor" (o problema que resolve), "sonho" (o resultado desejado), "curiosidade" (o que você não sabe), "prova social" (quem já usou). Mapeado pela skill `creative-hook`.

---

*Atualizado por: /pensare (Coordinator) ou /pensare-estrategia*
*Adicionar novo termo: edite este arquivo com nome em negrito, definição de 2-5 linhas, contexto de uso no Pensare OS*
