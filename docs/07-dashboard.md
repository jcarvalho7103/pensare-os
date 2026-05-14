# Dashboard — Pensare OS

> Interface web para visualizar, editar e operar o Pensare OS. FastAPI + SPA HTML/Tailwind/Alpine.js.

---

## Arquitetura

```
┌──────────────────────────────────────────┐
│  Frontend: dashboard/index.html          │
│  ─────────                               │
│  • HTML5 + Tailwind CSS (CDN)            │
│  • Alpine.js (CDN) para reatividade      │
│  • Inter font                            │
│  • SVG vanilla para charts               │
│  • Sem build step                        │
└────────────────┬─────────────────────────┘
                 │ chama via fetch()
                 ▼
┌──────────────────────────────────────────┐
│  Backend: dashboard/server.py            │
│  ─────────                               │
│  • FastAPI + uvicorn                     │
│  • 12 endpoints REST                     │
│  • pyyaml para parsear SKILL.md          │
│  • Path-traversal prevention             │
│  • subprocess para invocar claude CLI    │
└──────────────────────────────────────────┘
```

---

## Subindo o dashboard

### Local (desenvolvimento)

```bash
cd /Users/alicycarvalho/pensare-os
python dashboard/server.py
```

Saída esperada:
```
INFO:     Uvicorn running on http://0.0.0.0:8360 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Abra: **http://localhost:8360**

### Background (rodar e continuar)

```bash
nohup python dashboard/server.py > logs/dashboard.log 2>&1 &
echo $! > logs/dashboard.pid
```

Parar:
```bash
kill $(cat logs/dashboard.pid)
```

### Vercel (produção, somente leitura)

Já está deployado em **https://pensare-os.vercel.app**.

Limitações em produção:
- ❌ Sem Claude CLI disponível (chat não funciona)
- ❌ Sem write access em arquivos
- ❌ Sem daemon de heartbeat
- ✅ Visualização das configurações + estrutura

---

## Os 11 Módulos

### 1. Dashboard — `/`

Visão geral do sistema em tempo real.

**Componentes**:
- 6 cards de métricas (Leads hoje, SQL, Vendas, Receita, CPL, Conversão)
- Bar chart "Leads & Receita — últimos 14 dias"
- Tabela "Em execução" (tasks ativas)
- Lista "Heartbeats recentes"

**Fonte de dados**:
- `GET /api/metrics` (agregação de `events.ndjson` + `_contexto/empresa.md`)
- `GET /api/events` (últimos 50 eventos)
- `GET /api/heartbeats` (rotinas + estado)

### 2. Core — `/core`

Visualização hierárquica dos 4 componentes core: Orchestrator, System Flow, Decision Engine, State Machine.

**Uso**: ver responsabilidades e limites dos componentes centrais.

### 3. Orchestrator — `/orchestrator`

File explorer + editor para os arquivos de orquestração.

**Permite**: ler/editar fluxos, regras de roteamento, regras de escalação.

### 4. Agents — `/agents`

Grid dos 17 agentes agrupados por tier.

**Componentes**:
- Card por agente com tier, descrição, KPIs
- Modal de detalhe ao clicar
- Filtro por tier
- Busca por nome

**Fonte**:
- `GET /api/agents` (scaneia `.claude/skills/pensare-*/SKILL.md`, parseia YAML frontmatter)

### 5. Skills — `/skills`

Grid das 10 skills com descrição e categoria.

**Categorias**:
- `commercial` (6 skills)
- `marketing` (3 skills)
- `customer-success` (1 skill)

### 6. Memory — `/memory`

File tree + split editor para a memória.

**Permite**:
- Navegar `memory/shared/`, `memory/per-agent/`, raiz
- Editar arquivos `.md`
- Salvar com `PUT /api/memory/file`

**Segurança**: path traversal prevention — não pode editar fora de `memory/` e raiz permitida.

### 7. Heartbeats — `/heartbeats`

Visão das rotinas + status do daemon.

**Componentes**:
- Lista de rotinas Daily/Weekly/Monthly
- Status: última execução, próxima execução
- Indicador do daemon (rodando? falhando?)

**Fonte**:
- `GET /api/heartbeats` (parseia `HEARTBEAT.md` + `state.json`)
- `GET /api/heartbeat/status` (checa `launchctl`)

### 8. Tools — `/tools`

Registry de ferramentas (GHL, WhatsApp, Meta Ads, etc.) editável.

**Permite**: documentar quais tools estão em uso, propósito, regras.

### 9. Soul — `/soul`

Seções colapsáveis do `SOUL.md` + `IDENTITY.md` + `AGENTS.md`.

**Componentes**:
- 8 Princípios
- 13 Não-Negociáveis
- 7 Perguntas da Decision Philosophy
- Brand Voice
- Hierarquia visual dos 17 agentes

### 10. Tasks — `/tasks`

Kanban drag-and-drop com 3 colunas: Pendente, Em Execução, Concluído.

**Fonte**:
- `GET /api/tasks` (parseia "Next Steps" do `MEMORY.md`)
- `POST /api/tasks` (adiciona task)

### 11. Chat — `/chat`

Conversa com agentes do Pensare OS.

**Componentes**:
- Seletor de agente (dropdown com os 17)
- Histórico de mensagens (bubbles)
- Input de mensagem
- Lista de conversas anteriores

**Backend**:
- `POST /api/chat` invoca `claude --dangerously-skip-permissions --print /agente {mensagem}`
- Timeout: 120s

**⚠️ Não funciona em produção** (Vercel não tem Claude CLI).

---

## Endpoints REST

### `GET /api/metrics`
Métricas agregadas para o Dashboard.

**Resposta**:
```json
{
  "leads_hoje": 0,
  "sql": 0,
  "vendas": 0,
  "receita": 0,
  "cpl": null,
  "conversao": null,
  "chart_14d": [...]
}
```

### `GET /api/events`
Últimos 50 eventos do log NDJSON.

**Resposta**:
```json
[
  {
    "ts": "2026-05-13T14:30:00Z",
    "agent": "/pensare-sdr",
    "type": "lead_captured",
    "summary": "...",
    "payload": {...}
  }
]
```

### `GET /api/agents`
Lista dos 17 agentes com frontmatter parseado.

**Resposta**:
```json
[
  {
    "name": "pensare-ceo",
    "tier": "director",
    "description": "...",
    "reports_to": "/pensare-conselho",
    "supervises": [...],
    "skills_used": [...],
    "kpis": [...]
  }
]
```

### `GET /api/memory/tree`
File tree de memory/ + arquivos da raiz.

**Resposta**:
```json
{
  "root": ["SOUL.md", "IDENTITY.md", ...],
  "memory": {
    "shared": {...},
    "per-agent": {...}
  }
}
```

### `GET /api/memory/file?path=<path>`
Lê arquivo (com path traversal prevention).

### `PUT /api/memory/file`
Escreve arquivo.

**Body**:
```json
{
  "path": "memory/shared/decisions.md",
  "content": "..."
}
```

### `GET /api/tasks`
Tasks parseadas de `MEMORY.md`.

### `POST /api/tasks`
Adiciona task.

**Body**:
```json
{
  "title": "...",
  "description": "...",
  "priority": "high",
  "status": "pending"
}
```

### `GET /api/heartbeats`
Rotinas de `HEARTBEAT.md` + estado do `state.json`.

### `GET /api/heartbeat/status`
Checa via `launchctl list com.pensare.heartbeat`.

### `GET /api/soul`
Lê `SOUL.md` + `IDENTITY.md` + `AGENTS.md` para o módulo Soul.

### `POST /api/chat`
Invoca agente.

**Body**:
```json
{
  "agent": "/pensare-ceo",
  "message": "..."
}
```

**Resposta**:
```json
{
  "response": "..." 
}
```

---

## Configuração

### Variável de ambiente

```python
WORKSPACE_ROOT = Path(os.environ.get(
    "PENSARE_WORKSPACE",
    "/Users/alicycarvalho/pensare-os"
))
```

Use `PENSARE_WORKSPACE=/path/to/other` para apontar para outro workspace.

### Porta

Padrão: `8360`. Para mudar, edite `dashboard/server.py`:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8360)
```

### CORS

Por padrão, dashboard só responde a localhost. Para permitir outras origens, edite `server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://my-other-app.com"],
    ...
)
```

---

## Segurança

### O que está protegido
- ✅ Path traversal em `/api/memory/file` (não pode escrever fora de `memory/` + raiz permitida)
- ✅ `--dangerously-skip-permissions` só em `/api/chat` e apenas para agentes válidos
- ✅ Arquivo `.env`, credenciais, `state.json` no `.gitignore`

### O que NÃO está protegido (uso local apenas)
- ❌ Sem autenticação no dashboard
- ❌ Qualquer pessoa na sua rede local pode acessar
- ❌ Não há rate limiting

**Use apenas localhost ou em rede confiável.**

---

## Personalização

### Tema (claro/escuro)
Alterne via botão no canto superior direito. Estado persiste em `localStorage['pensare-theme']`.

### Cores
Edite `dashboard/index.html`, seção `<style>`:

```css
:root {
  --bg: #0a0a0a;
  --bg-card: #111;
  --accent: #ff6b35;  /* customize aqui */
  ...
}
```

### Adicionar módulo novo
1. Adicione card no menu lateral (HTML)
2. Crie endpoint em `server.py`
3. Adicione função Alpine no `index.html`
4. Adicione rota frontend

---

## Performance

- **Latência típica de endpoint**: <100ms para reads
- **`/api/chat`**: 5–60s (depende da resposta do Claude)
- **Memória do server**: ~80MB ocioso

Se ficar lento:
- Comprima `logs/events.ndjson` (rotação por mês)
- Limite `GET /api/events` a 20 (default já é 50)
- Adicione cache de 1min em endpoints estáticos

---

## Troubleshooting

### Server não sobe

```bash
# Verifique deps
pip install -r dashboard/requirements.txt

# Verifique porta livre
lsof -i :8360
```

### Erro 500 em algum endpoint

```bash
tail -30 logs/dashboard.log
```

### Chat não responde

```bash
# Teste manual
claude --print /pensare "teste"
```

Se travar, problema é Claude CLI, não dashboard.

### Métricas sempre zeradas

Normal se `logs/events.ndjson` está vazio. Use:

```bash
pensare-log lead_captured "teste" '{}'
```

E recarregue dashboard.

---

## Roadmap

Possíveis evoluções (não implementadas):

- [ ] Autenticação básica (BasicAuth para uso em rede)
- [ ] WebSocket para updates em tempo real (sem polling)
- [ ] Gráficos mais ricos (Chart.js ou similar)
- [ ] Export de relatórios em PDF
- [ ] Dark/light mode automático por horário
- [ ] Mobile responsive completo

---

*Dashboard é a janela do operador. Manter simples, rápido e útil é mais importante que sofisticado.*
