# TOOLS.md — Registry de Ferramentas do Pensare OS

> Referência completa das ferramentas disponíveis no runtime Claude Code CLI.
> Cada agente deve consultar este documento para saber quais ferramentas pode usar e quando.

---

## Princípios de Uso de Ferramentas

1. **Ferramenta certa para o trabalho certo** — não use Bash para o que Read faz melhor
2. **Custo de context** — cada ferramenta consome contexto; use a mais econômica que resolve o problema
3. **Sem ações destrutivas não solicitadas** — Write/Edit/Bash com mutação só quando explicitamente instruído
4. **Registro sempre** — qualquer ação relevante gera um evento em logs/events.ndjson
5. **Tier 3 tem acesso mais amplo a ferramentas de execução; Tier 0-1 usam principalmente Read e análise**

---

## Categoria 1 — Research (Pesquisa e Busca)

### WebSearch
- **Propósito**: Buscar informações na web em tempo real
- **Quando usar**: pesquisa de mercado, inteligência competitiva, notícias recentes, validação de dados, benchmarks externos
- **Quando NÃO usar**: para encontrar arquivos internos do sistema (use Read), para análises que já têm contexto carregado
- **Agentes com acesso prioritário**: /pensare-estrategia, /pensare-inteligencia, /pensare-dados, /pensare-growth
- **Agentes que raramente precisam**: /pensare-financeiro (dados internos), /pensare-cs (dados de cliente estão na memória)
- **Observação**: sempre registre fontes relevantes encontradas no evento NDJSON correspondente

### WebFetch
- **Propósito**: Ler o conteúdo de uma URL específica
- **Quando usar**: acessar landing pages de concorrentes, ler artigos linkados, fazer scraping leve de dados públicos, verificar copy de campanhas ao vivo
- **Quando NÃO usar**: busca genérica (use WebSearch), quando o conteúdo já está na memória do sistema
- **Agentes com acesso prioritário**: /pensare-estrategia, /pensare-trafego, /pensare-copy, /pensare-criativos
- **Limite de uso**: preferir 1-3 fetches por sessão para não consumir contexto excessivo

---

## Categoria 2 — File (Leitura e Escrita de Arquivos)

### Read
- **Propósito**: Ler qualquer arquivo do filesystem
- **Quando usar**: carregar SOUL.md, IDENTITY.md, MEMORY.md, contextos, planos, relatórios gerados em sessões anteriores, logs
- **Quando NÃO usar**: para checar se arquivo existe (use Bash com `ls`), para edições (use Edit)
- **Agentes com acesso**: TODOS os agentes — leitura é sempre permitida
- **Arquivos de boot obrigatório** (nesta ordem):
  1. SOUL.md
  2. IDENTITY.md
  3. MEMORY.md
  4. logs/events.ndjson (tail -10 via Bash)

### Write
- **Propósito**: Criar ou sobrescrever arquivos completos
- **Quando usar**: criar novos documentos, gerar relatórios, criar planos de ação, inicializar arquivos de memória de novos agentes
- **Quando NÃO usar**: para atualizar parte de um arquivo existente (use Edit), para arquivos de sistema críticos sem autorização explícita
- **Agentes com acesso prioritário**: /pensare-copy, /pensare-dados, /pensare-operacoes, /pensare-automacao
- **Cuidado**: Write sobrescreve — sempre leia o arquivo antes de fazer Write em arquivos existentes
- **Nunca sobrescrever**: SOUL.md, IDENTITY.md, AGENTS.md sem instrução explícita da operadora

### Edit
- **Propósito**: Editar partes específicas de arquivos existentes
- **Quando usar**: atualizar MEMORY.md ao fim da sessão, adicionar entradas em glossário, ajustar planos em andamento, corrigir erros em documentos
- **Quando NÃO usar**: para criar novos arquivos (use Write), para mudanças completas de conteúdo (Write é mais claro)
- **Agentes com acesso**: todos, com preferência para uso por /pensare (Coordinator) para atualizações de estado
- **Regra de ouro**: sempre leia o arquivo antes de editar para garantir que o old_string existe

---

## Categoria 3 — Execution (Execução de Comandos)

### Bash
- **Propósito**: Executar comandos shell no sistema
- **Quando usar**:
  - `tail -10 logs/events.ndjson` — verificar últimos eventos (boot)
  - `echo '{"ts":...}' >> logs/events.ndjson` — registrar eventos
  - `ls` — verificar estrutura de diretórios
  - `mkdir -p` — criar estrutura de diretórios
  - `find` — localizar arquivos por padrão
  - `grep` — buscar padrões em arquivos
  - `date` — obter timestamp atual para logs
- **Quando NÃO usar**: para leitura de arquivos (use Read), para edição de arquivos (use Edit/Write), para buscas web (use WebSearch)
- **Agentes com acesso prioritário**: /pensare (Coordinator), /pensare-automacao, /pensare-dados
- **Agentes com acesso restrito**: /pensare-conselho, /pensare-copy, /pensare-criativos (raramente precisam de Bash)
- **Comandos proibidos sem autorização explícita**: `rm -rf`, `git push --force`, qualquer comando destrutivo

### Agent (Sub-agente)
- **Propósito**: Spawnar sub-agentes para tarefas paralelas ou isoladas
- **Quando usar**: tarefas longas e independentes que podem rodar em paralelo, isolamento de contexto para pesquisas pesadas
- **Quando NÃO usar**: para tarefas simples que o agente atual resolve, quando o resultado precisa ser imediato
- **Agentes com acesso**: /pensare (Coordinator), /pensare-ceo para orchestração de múltiplas análises simultâneas
- **Custo**: sub-agentes consomem contexto adicional — use com disciplina

---

## Categoria 4 — Task Management

### TaskCreate / TaskUpdate / TaskStop
- **Propósito**: Criar e gerenciar tasks de longa duração no Claude Code
- **Quando usar**: projetos com múltiplas etapas, tracking de entregas do AI Systemizer, gestão de pipeline
- **Quando NÃO usar**: para tarefas que completam em uma única sessão
- **Agentes com acesso**: /pensare (Coordinator), /pensare-operacoes, /pensare-ceo
- **Observação**: Tasks criadas devem sempre ter um owner definido (agente responsável)

---

## Categoria 5 — Browser (Automação Web)

### Playwright (mcp__plugin_playwright_playwright__)
Conjunto de ferramentas para automação de navegador.

#### browser_navigate
- **Propósito**: Navegar para uma URL no browser automatizado
- **Quando usar**: acessar portais que requerem JavaScript, preencher formulários web, verificar funis ao vivo
- **Agentes**: /pensare-trafego, /pensare-automacao

#### browser_snapshot
- **Propósito**: Capturar estado atual da página (acessibilidade tree)
- **Quando usar**: análise de estrutura de páginas de concorrentes, auditoria de landing pages
- **Agentes**: /pensare-trafego, /pensare-copy, /pensare-criativos

#### browser_take_screenshot
- **Propósito**: Screenshot da página atual
- **Quando usar**: documentar estado de campanhas, capturar evidências de análises
- **Agentes**: /pensare-trafego, /pensare-dados

#### browser_fill_form / browser_click / browser_type
- **Propósito**: Interagir com elementos de páginas web
- **Quando usar**: automações de formulários, testes de fluxos
- **Quando NÃO usar**: sem autorização explícita em sistemas de terceiros
- **Agentes**: /pensare-automacao apenas, com aprovação do Head ou CEO

#### browser_network_request / browser_network_requests
- **Propósito**: Monitorar requests de rede de uma página
- **Quando usar**: auditoria técnica de funis, análise de pixels e tracking
- **Agentes**: /pensare-automacao, /pensare-trafego

---

## Categoria 6 — Comunicação e MCP

### Gmail (mcp__claude_ai_Gmail__)
- **Propósito**: Gerenciar emails via Gmail
- **Subtools disponíveis**: search_threads, get_thread, create_draft, list_labels, label_thread
- **Quando usar**: pesquisa de emails de clientes, criação de rascunhos de follow-up, organização de labels por projeto
- **Quando NÃO usar**: envio de emails sem aprovação da operadora (sempre criar draft, nunca enviar diretamente)
- **Agentes**: /pensare-sdr, /pensare-comercial, /pensare-cs
- **Regra crítica**: NUNCA enviar emails automaticamente. Sempre criar draft para revisão da Isis.

### Canva (mcp__claude_ai_Canva__)
- **Propósito**: Criar e editar designs no Canva
- **Quando usar**: criação de criativos para campanhas, materiais de apresentação do AI Systemizer, templates de proposta
- **Agentes**: /pensare-criativos, /pensare-copy

---

## Categoria 7 — Scheduling e Monitoramento

### CronCreate / CronDelete / CronList
- **Propósito**: Gerenciar rotinas agendadas
- **Quando usar**: configurar rotinas do HEARTBEAT.md, agendar relatórios periódicos
- **Agentes**: /pensare-automacao apenas (com aprovação do CEO)

### Monitor
- **Propósito**: Monitorar output de processos em background
- **Quando usar**: acompanhar tarefas longas, aguardar resultado de operações assíncronas
- **Agentes**: /pensare, /pensare-automacao

### PushNotification
- **Propósito**: Enviar notificações para a operadora
- **Quando usar**: alertas críticos, conclusão de tarefas importantes, alertas de churn ou risco
- **Agentes**: /pensare (Coordinator), /pensare-financeiro (alertas financeiros), /pensare-cs (alertas de risco de cliente)

---

## Tabela Rápida — Acesso por Tier

| Ferramenta | Tier 0 (Coordinator) | Tier 1 (C-Suite) | Tier 2 (Heads) | Tier 3 (Execution) |
|------------|---------------------|------------------|----------------|-------------------|
| Read | Sempre | Sempre | Sempre | Sempre |
| Write | Com cautela | Raramente | Com cautela | Frequente |
| Edit | Frequente | Com cautela | Frequente | Frequente |
| Bash | Frequente | Raramente | Com propósito | Com propósito |
| WebSearch | Com propósito | Com propósito | Frequente | Frequente |
| WebFetch | Com propósito | Com propósito | Com propósito | Frequente |
| Agent | Frequente | Com aprovação | Raramente | Nunca |
| Gmail | Com aprovação | Nunca direto | Draft apenas | Draft apenas |
| Browser | Nunca direto | Nunca | /automacao | /automacao, /trafego |
| Cron | Nunca | Nunca | Raramente | /automacao apenas |

---

*Atualizar quando novas ferramentas forem integradas ao runtime.*
*Versão atual: Claude Code CLI — sem OpenClaw, sem Paperclip.*
