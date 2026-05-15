# Dashboard — Pensare OS

> Interface web para visualizar, editar e operar o Pensare OS. FastAPI + Supabase + SPA HTML/Tailwind/Alpine.js.

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
│  • Supabase (Postgres) para persistência │
│  • pyyaml para parsear SKILL.md          │
│  • Path-traversal prevention             │
│  • Claude CLI para chat (local)          │
│  • OpenAI API fallback (Vercel)          │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  Supabase (tplwqvvffanwsyhgufya)         │
│  ─────────                               │
│  • events — log de eventos               │
│  • tasks — tarefas do sistema            │
│  • heartbeat_state — estado das rotinas  │
│  • memory_files — memória editável       │
└──────────────────────────────────────────┘
```

---

## Subindo o dashboard

### Local (desenvolvimento)

```bash
cd C:\Users\USUARIO\Documents\pensare-os
python dashboard/server.py
# ou com o Python do sistema:
"C:\Users\USUARIO\AppData\Local\Programs\Python\Python311\python.exe" -m uvicorn dashboard.server:app --host 0.0.0.0 --port 8360
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

### Vercel (produção)

Deployado em **https://pensare-os.vercel.app**.

| Funcionalidade | Local | Vercel |
|---------------|-------|--------|
| Dashboard / métricas | OK | OK |
| Eventos (Supabase) | OK | OK |
| Tasks (Supabase) | OK | OK |
| Agentes / Soul | OK | OK |
| Chat com Claude CLI | OK | -- |
| Chat com OpenAI API | fallback | OK (se key configurada) |

---

## Banco de dados (Supabase)

### Tabelas

| Tabela | Descrição | Campos principais |
|--------|-----------|-------------------|
| `events` | Log de eventos | `ts`, `agent`, `type`, `summary`, `payload` |
| `tasks` | Tarefas do sistema | `title`, `priority`, `status`, `created_at` |
| `heartbeat_state` | Estado das rotinas | `name`, `last_run`, `next_run`, `status` |
| `memory_files` | Memória editável | `path`, `content`, `updated_at` |

### Variáveis de ambiente

```
SUPABASE_URL=https://tplwqvvffanwsyhgufya.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...  (service_role JWT)
```

---

## Os 11 Módulos

### 1. Dashboard — `/`

Visão geral do sistema em tempo real.

**Componentes**:
- 6 cards de métricas (Leads hoje, SQL, Vendas, Receita, CPL, Conversão)
- Tabela "Em execução" (tasks ativas)
- Lista "Heartbeats recentes"

**Fonte de dados**:
- `GET /api/metrics` (contagem de eventos no Supabase + `_contexto/empresa.md`)
- `GET /api/events` (últimos 50 eventos do Supabase)
- `GET /api/heartbeats` (rotinas + estado)

### 2. Agents — `/agents`

Grid dos 18 agentes agrupados por tier.

**Fonte**:
- `GET /api/agents` (scaneia `.claude/skills/pensare-*/SKILL.md`, parseia YAML frontmatter)

### 3. Tasks — `/tasks`

Kanban com 3 colunas: Pendente, Em Execução, Concluído.

**Fonte**:
- `GET /api/tasks` (lê tabela `tasks` do Supabase)
- `POST /api/tasks` (cria task)
- `PATCH /api/tasks/{id}` (atualiza status)

### 4. Chat — `/chat`

Conversa com agentes do Pensare OS.

**Backend**:
- Local: `claude -p "/agente mensagem"` (usa sua assinatura Claude Code)
- Vercel: OpenAI API com system prompt construído de SOUL.md + SKILL.md
- Timeout: 120s

### 5. Memory — `/memory`

File tree + split editor para a memória.

### 6. Soul — `/soul`

Seções colapsáveis do SOUL.md + IDENTITY.md + AGENTS.md.

### 7. Heartbeats — `/heartbeats`

Rotinas + status (estado lido do Supabase).

---

## Endpoints REST

| Método | Path | Descrição |
|--------|------|-----------|
| `GET` | `/api/metrics` | Métricas agregadas do dia |
| `GET` | `/api/events` | Últimos 50 eventos |
| `GET` | `/api/agents` | Lista dos 18 agentes |
| `GET` | `/api/tasks` | Tasks agrupadas por status |
| `POST` | `/api/tasks` | Criar task |
| `PATCH` | `/api/tasks/{id}` | Atualizar status da task |
| `GET` | `/api/memory/tree` | Árvore de arquivos de memória |
| `GET` | `/api/memory/file?path=` | Ler arquivo |
| `PUT` | `/api/memory/file` | Escrever arquivo |
| `GET` | `/api/heartbeats` | Rotinas + estado |
| `GET` | `/api/heartbeat/status` | Status do daemon |
| `GET` | `/api/soul` | SOUL + IDENTITY + AGENTS |
| `POST` | `/api/chat` | Invocar agente |

---

## Configuração

### Porta

Padrão: `8360`. Para mudar, edite `dashboard/server.py`:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8360)
```

### CORS

Permite todas as origens por padrão (uso local). Para restringir:

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
- Path traversal em `/api/memory/file`
- RLS ativado em todas as tabelas do Supabase (acesso via service_role apenas)
- Credenciais via variáveis de ambiente

### O que NÃO está protegido (uso local apenas)
- Sem autenticação no dashboard
- Qualquer pessoa na rede local pode acessar
- Não há rate limiting

**Use apenas localhost ou em rede confiável.**

---

## Troubleshooting

### Server não sobe

```bash
pip install -r dashboard/requirements.txt
# Verifique porta livre
netstat -ano | findstr :8360
```

### Chat não responde

```bash
# Teste manual
claude -p "/pensare-ceo teste"
```

### Métricas sempre zeradas

Verifique conexão com Supabase:
```bash
curl https://tplwqvvffanwsyhgufya.supabase.co/rest/v1/events?select=id&limit=1 \
  -H "apikey: <service_role_key>" \
  -H "Authorization: Bearer <service_role_key>"
```

---

*Dashboard é a janela do operador. Manter simples, rápido e útil é mais importante que sofisticado.*
