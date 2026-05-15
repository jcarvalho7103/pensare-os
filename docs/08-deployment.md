# Deployment — Pensare OS

> GitHub + Vercel + Supabase: deploy completo do Pensare OS.

---

## Visão geral

O Pensare OS tem **2 modos de deploy**:

| Modo | Onde | O que funciona | O que não funciona |
|------|------|----------------|-------------------|
| **Local** | Windows do operador | Tudo (inclui chat via Claude CLI) | — |
| **Vercel (produção)** | Edge serverless | Dashboard, métricas, tasks, eventos (tudo via Supabase) | Chat (sem Claude CLI) |

Ambos os modos leem e escrevem no **mesmo banco Supabase**, garantindo dados sincronizados.

---

## Repositório GitHub

### Onde está

**https://github.com/jcarvalho7103/pensare-os**

### Estrutura do repo

```
pensare-os/
├── README.md
├── CLAUDE.md
├── SOUL.md
├── IDENTITY.md
├── AGENTS.md
├── MEMORY.md
├── TOOLS.md
├── HEARTBEAT.md
├── requirements.txt
├── vercel.json
├── setup.sh
│
├── .claude/skills/          ← 18 agents (coordinator + 17 heads)
├── api/                     ← Vercel entry point
├── dashboard/               ← FastAPI + SPA
├── heartbeat/               ← daemon
├── memory/                  ← memória local
├── _contexto/               ← contexto de negócio
└── docs/                    ← esta documentação
```

---

## Infraestrutura

### Supabase (banco central)

| Item | Valor |
|------|-------|
| Projeto | `tplwqvvffanwsyhgufya` |
| URL | `https://tplwqvvffanwsyhgufya.supabase.co` |
| Região | Padrão |

**Tabelas**:
- `events` — log de todos os eventos do sistema
- `tasks` — tarefas com prioridade e status
- `heartbeat_state` — estado das rotinas automáticas
- `memory_files` — memória editável via dashboard

**Segurança**:
- RLS ativado em todas as tabelas
- Acesso apenas via `service_role` key
- Key nunca commitada no repo (via env var)

### Variáveis de ambiente

| Variável | Onde configurar | Descrição |
|----------|----------------|-----------|
| `SUPABASE_URL` | Vercel + local | URL do projeto Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | Vercel + local | JWT service_role |
| `OPENAI_API_KEY` | Vercel (opcional) | Para chat na Vercel |
| `OPENAI_MODEL` | Vercel (opcional) | Default: `gpt-4o-mini` |

No local, as variáveis têm defaults no código (`server.py`).
Na Vercel, configuradas via `vercel env add`.

---

## Deploy na Vercel

### `vercel.json`

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" },
    { "src": "dashboard/index.html", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/index.py" },
    { "src": "/(.*)", "dest": "dashboard/index.html" }
  ]
}
```

### CI/CD

```
push em main no GitHub
       ↓
GitHub webhook → Vercel
       ↓
Vercel build + deploy automático (~30s)
       ↓
https://pensare-os.vercel.app atualizado
```

### Deploy manual

```bash
vercel --prod
```

---

## Setup local (Windows)

### Pré-requisitos

| Requisito | Versão | Verificar |
|-----------|--------|-----------|
| Python | 3.10+ | `python --version` |
| Claude Code CLI | última | `claude --version` |
| Git | 2.30+ | `git --version` |

### Instalação

```bash
cd C:\Users\USUARIO\Documents\pensare-os
pip install -r requirements.txt
```

### Rodar dashboard

```bash
python dashboard/server.py
# → http://localhost:8360
```

### Rodar em background

```bash
nohup python dashboard/server.py > logs/dashboard.log 2>&1 &
```

---

## Backup e disaster recovery

### O que precisa backup

| Item | Estratégia |
|------|-----------|
| Código + configs | Git (push regular) |
| Eventos, tasks | Supabase (backup automático do plano) |
| `_contexto/empresa.md` + `mercado.md` | Versionado no Git |
| Skills (.claude/skills/) | Versionado no Git |

### Restore

```bash
git clone https://github.com/jcarvalho7103/pensare-os.git
cd pensare-os
pip install -r requirements.txt
python dashboard/server.py
# Dados já estão no Supabase — nada a restaurar manualmente
```

---

## Custo

| Serviço | Plano | Custo |
|---------|-------|-------|
| GitHub | Público | Grátis |
| Vercel | Hobby | Grátis |
| Supabase | Free tier | Grátis (500MB, 50k rows) |
| Claude Code | Assinatura pessoal | Já incluso |

---

*Deploy bem feito é o que separa "código rodando" de "sistema operando".*
