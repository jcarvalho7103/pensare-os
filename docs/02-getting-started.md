# Getting Started — Pensare OS

> Setup completo do Pensare OS do zero até a primeira operação real.

---

## Pré-requisitos

| Requisito | Versão mínima | Como verificar |
|-----------|--------------|----------------|
| **macOS** | Big Sur (11.x) ou superior | `sw_vers` |
| **Python** | 3.10+ | `python --version` |
| **Git** | 2.30+ | `git --version` |
| **Claude Code CLI** | última versão | `claude --version` |
| **Node.js** (opcional, p/ Vercel CLI) | 18+ | `node --version` |
| **gh CLI** (opcional, p/ GitHub) | 2.40+ | `gh --version` |

### Instalação dos pré-requisitos

```bash
# Claude Code CLI
brew install anthropic/claude/claude-code   # macOS
# ou: npm install -g @anthropic/claude-code

# gh CLI
brew install gh

# Vercel CLI (opcional)
npm install -g vercel
```

---

## Setup completo (passo a passo)

### 1. Clone o repositório

```bash
cd ~
git clone https://github.com/jcarvalho7103/pensare-os.git
cd pensare-os
```

**Se você é a Isis** e já tem o diretório local, pule este passo.

### 2. Execute o setup automatizado

```bash
bash setup.sh
```

O script faz:
- Instala dependências do dashboard (`pip install -r dashboard/requirements.txt`)
- Dá permissão de execução aos scripts em `.claude/skills/_shared/bin/`
- Adiciona `~/.zshrc` (ou `~/.bashrc`) o PATH dos bin scripts
- Pergunta se deseja instalar o heartbeat como daemon automático (LaunchAgent)

### 3. Recarregue o shell

```bash
source ~/.zshrc       # ou ~/.bashrc
```

Verifique que os comandos auxiliares estão disponíveis:

```bash
which pensare-status pensare-log pensare-cost pensare-reflect
# deve mostrar paths em .claude/skills/_shared/bin/
```

### 4. Preencha o contexto de negócio

Edite os arquivos com dados reais:

```bash
$EDITOR _contexto/empresa.md     # dados da Pensare Digital
$EDITOR _contexto/mercado.md     # contexto de mercado
$EDITOR MEMORY.md                # estado atual da sessão
```

Esses arquivos são lidos por agentes estratégicos e comerciais. Sem eles preenchidos, as análises serão genéricas.

### 5. Verifique a saúde do sistema

```bash
pensare-status
# saída esperada: { "status": "ok", ... }
```

---

## Primeiros usos

### A. Inicie o dashboard

Em um terminal:

```bash
cd /Users/alicycarvalho/pensare-os
python dashboard/server.py
```

Abra: **http://localhost:8360**

Você verá os 11 módulos: Dashboard, Core, Orchestrator, Agents, Skills, Memory, Heartbeats, Tools, Soul, Tasks, Chat.

### B. Invoque seu primeiro agente

Em outro terminal:

```bash
cd /Users/alicycarvalho/pensare-os
claude
```

No prompt do Claude Code, digite:

```
/pensare ola, faça um diagnóstico do status atual do sistema
```

O Coordinator deve:
1. Carregar SOUL.md + IDENTITY.md
2. Ler tail -10 de logs/events.ndjson
3. Ler MEMORY.md
4. Responder com status estruturado

### C. Execute o heartbeat manualmente

Preview do que rodaria agora:

```bash
python heartbeat/daemon.py --dry-run
```

Execução real (uma vez):

```bash
python heartbeat/daemon.py --once
```

Daemon contínuo (foreground, Ctrl+C para parar):

```bash
python heartbeat/daemon.py
```

### D. Registre um evento manualmente

```bash
pensare-log lead_captured "Novo lead: empresa X" '{"score":8,"segment":"consultoria"}'
```

Vai gerar uma linha em `logs/events.ndjson`. O daemon do heartbeat detecta no próximo ciclo (≤60s) e aciona o gatilho correspondente.

---

## Estrutura mental do operador

Você (operadora) interage com o sistema de 3 formas:

### 1. Comando direto via Claude Code
```
/pensare-comercial me dê o status do pipeline
```

### 2. Visualização via Dashboard
Abra http://localhost:8360, navegue pelos módulos.

### 3. Edição manual de arquivos
Para mudanças deliberadas:
- Edite `MEMORY.md` para atualizar o estado da sessão
- Edite `_contexto/empresa.md` para atualizar dados de negócio
- Edite `SOUL.md`/`IDENTITY.md` apenas para evolução estratégica deliberada

O sistema **lê** o que você edita. **Não edite arquivos em `memory/per-agent/`** manualmente — esses são memória dos agentes.

---

## Validação completa

Checklist após o setup:

```bash
# 1. Carga padrão presente
ls -la SOUL.md IDENTITY.md AGENTS.md MEMORY.md HEARTBEAT.md TOOLS.md CLAUDE.md
# ✓ Todos devem existir

# 2. Agentes carregados
ls .claude/skills/pensare*/SKILL.md | wc -l
# ✓ Deve retornar 17

# 3. Skills carregadas
ls .claude/skills/skills/*/SKILL.md | wc -l
# ✓ Deve retornar 10

# 4. Bin scripts executáveis
ls -la .claude/skills/_shared/bin/
# ✓ pensare-log, pensare-status, pensare-cost, pensare-reflect com +x

# 5. Heartbeat funcional
python heartbeat/daemon.py --dry-run
# ✓ Deve listar rotinas que rodariam agora

# 6. Dashboard funcional
curl -s http://localhost:8360/api/agents | jq 'length'
# ✓ Deve retornar 17 (com server rodando)

# 7. Status geral
pensare-status
# ✓ { "status": "ok", ... }
```

---

## Primeira sessão real recomendada

Sequência sugerida para a primeira sessão produtiva:

```
1. /pensare diagnóstico inicial do sistema

2. /pensare-conselho avalie a estratégia atual de escala
   do AI Systemizer dado o estado das tasks pendentes

3. /pensare-ceo defina as 3 prioridades para a semana

4. /pensare-comercial me mostre o pipeline atual e
   identifique o lead mais quente

5. /pensare encerre a sessão e atualize MEMORY.md
```

Cada comando deve:
- Carregar contexto correto (SOUL + IDENTITY + memória relevante)
- Produzir output estruturado
- Registrar evento em `logs/events.ndjson`

---

## Próximos passos

Depois do setup:

1. Leia [`docs/01-architecture.md`](01-architecture.md) para entender as 5 camadas
2. Leia [`docs/03-agents-guide.md`](03-agents-guide.md) para dominar os 17 agentes
3. Configure o heartbeat permanente: `bash heartbeat/install.sh`
4. Atualize `_contexto/empresa.md` com dados reais e atualize quando mudarem
5. Deixe o dashboard rodando em background:
   ```bash
   nohup python dashboard/server.py > logs/dashboard.log 2>&1 &
   ```

---

## Problemas? Veja troubleshooting

Se algo não funciona, consulte [`docs/09-troubleshooting.md`](09-troubleshooting.md).
