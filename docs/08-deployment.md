# Deployment — Pensare OS

> GitHub + Vercel + LaunchAgent: deploy completo do Pensare OS.

---

## Visão geral

O Pensare OS tem **2 modos de deploy**:

| Modo | Onde | O que funciona | O que não funciona |
|------|------|----------------|-------------------|
| **Local** | Mac da operadora | Tudo | — |
| **Vercel (produção)** | Edge serverless | Visualização das configs | Chat, daemon, write em arquivos |

O sistema real opera **localmente**. O Vercel é apenas vitrine pública.

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
├── .gitignore
│
├── .claude/skills/          ← 17 agents + 10 skills
├── api/                     ← Vercel entry point
├── dashboard/               ← FastAPI + SPA
├── heartbeat/               ← daemon + install
├── memory/                  ← memória persistente
├── _contexto/               ← contexto de negócio
└── docs/                    ← esta documentação
```

### Arquivos ignorados pelo Git (`.gitignore`)

```
# Runtime — não versionar
logs/events.ndjson
heartbeat/state.json
daily/
memory/per-agent/*/state.md

# Python
__pycache__/
*.py[cod]
.env
.venv

# Node
node_modules/
.vercel/output/
.vercel

# Segredos
.env.local
.env.production
```

---

## Setup do GitHub (do zero)

### Pré-requisito: gh CLI

```bash
brew install gh
~/bin/gh auth login   # ou: gh auth login
```

Escolha: GitHub.com → HTTPS → Login with web browser.

### Configurar Git localmente

```bash
cd /Users/alicycarvalho/pensare-os
git config user.name "Isis Carvalho"
git config user.email "jcesar.ccarvalho@gmail.com"
```

### Primeiro push

```bash
git init
git add .gitignore *.md *.sh *.json _contexto/ api/ dashboard/ heartbeat/ memory/ .claude/

git commit -m "feat: Pensare OS v1.0 — sistema completo"

gh repo create pensare-os --public --source=. --remote=origin --push
```

### Pushes subsequentes

```bash
git add <arquivos>
git commit -m "feat|fix|docs: descrição"
git push origin main
```

### Branches

- `main` — produção (deploy automático na Vercel)
- Para mudanças experimentais, use branches: `feat/nome`, `fix/nome`

---

## Deploy na Vercel

### Pré-requisito: Vercel CLI

```bash
npm install -g vercel
vercel login
```

Escolha: Continue with GitHub.

### `vercel.json` (já criado)

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "dashboard/index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "dashboard/index.html"
    }
  ]
}
```

### Entry point (`api/index.py`)

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "dashboard"))

from server import app
```

### Primeiro deploy

```bash
vercel --prod
```

Vai pedir scope. Se já está conectado:

```bash
vercel --prod --yes --scope <seu-team>
```

### Deploys subsequentes

**Automático**: cada push em `main` no GitHub dispara redeploy na Vercel (CI/CD).

**Manual**:
```bash
vercel --prod
```

### URLs

- Produção: `https://pensare-os.vercel.app`
- Preview (cada PR/branch): `https://pensare-os-{branch}-{team}.vercel.app`

### Limitações do Vercel

| Funcionalidade | Status |
|----------------|--------|
| Listar agentes | ✅ Funciona |
| Visualizar Soul/Identity | ✅ Funciona |
| Ver Heartbeat config | ✅ Funciona |
| **Chat com agentes** | ❌ Sem Claude CLI no serverless |
| **Editar memória** | ❌ Filesystem é read-only |
| **Daemon do heartbeat** | ❌ Vercel não roda processos longos |

Para operação real, use **localmente**.

---

## Setup do LaunchAgent (Heartbeat)

### Instalação

```bash
cd /Users/alicycarvalho/pensare-os
bash heartbeat/install.sh
```

O script:
1. Cria `~/Library/LaunchAgents/com.pensare.heartbeat.plist`
2. `launchctl load` no plist
3. Daemon começa a rodar (loop de 60s)

### Verificar

```bash
launchctl list | grep pensare
# deve mostrar: com.pensare.heartbeat
```

### Logs

```bash
tail -f logs/heartbeat.log         # stdout
tail -f logs/heartbeat-error.log   # stderr
tail -f logs/events.ndjson         # eventos gerados
```

### Desinstalar

```bash
launchctl unload ~/Library/LaunchAgents/com.pensare.heartbeat.plist
rm ~/Library/LaunchAgents/com.pensare.heartbeat.plist
```

---

## Variáveis de ambiente

### Local

Crie `.env.local` (gitignored):

```bash
PENSARE_WORKSPACE=/Users/alicycarvalho/pensare-os
PENSARE_LOG_LEVEL=info
```

Carregue:
```bash
export $(cat .env.local | xargs)
```

### Vercel

Configure via dashboard:
1. Vercel → Project Settings → Environment Variables
2. Adicione `PENSARE_WORKSPACE` se quiser apontar para outro caminho

**Note**: variáveis sensíveis (chaves de API) **nunca** devem ser commitadas em `.env`. Use Vercel env vars ou macOS Keychain.

---

## CI/CD

### Atual

```
push em main no GitHub
       ↓
GitHub webhook → Vercel
       ↓
Vercel build + deploy automático
       ↓
https://pensare-os.vercel.app atualizado em ~30s
```

### Próximos passos (não implementados)

Quando vier necessidade:
- **Tests automatizados** via GitHub Actions
  - `pytest` para `dashboard/server.py`
  - Linting de `.md` (frontmatter válido?)
- **Deploy de preview** automático em PRs
- **Branch protection** em `main`

---

## Backup e disaster recovery

### O que precisa backup

| Item | Estratégia |
|------|-----------|
| Código + configs | Git (push regular) |
| `logs/events.ndjson` | ⚠️ Gitignored → backup manual ou rsync |
| `memory/per-agent/*/state.md` | ⚠️ Gitignored → considerar versionar trimestralmente |
| `memory/per-agent/*/reflections.md` | ✅ Versionado |
| `heartbeat/state.json` | ⚠️ Gitignored — descartável |
| `_contexto/empresa.md` + `mercado.md` | ✅ Versionado |

### Backup manual recomendado

Crontab semanal:
```bash
# Domingo 22h
0 22 * * 0 rsync -a /Users/alicycarvalho/pensare-os/logs/ /Volumes/Backup/pensare-os-logs/
0 22 * * 0 rsync -a /Users/alicycarvalho/pensare-os/memory/per-agent/ /Volumes/Backup/pensare-os-memory/
```

### Restore

Para restaurar de zero:
```bash
git clone https://github.com/jcarvalho7103/pensare-os.git
cd pensare-os
bash setup.sh
# restaurar logs/events.ndjson e memory/per-agent/*/state.md do backup
```

---

## Domínio customizado (opcional)

### Comprar domínio
Exemplo: `pensare-os.com` ou `pensare.digital`.

### Conectar à Vercel

1. Vercel → Project Settings → Domains
2. Adicionar domínio
3. Apontar DNS do provedor (Cloudflare, Registro.br, etc.) para Vercel
4. Aguardar propagação (até 24h, geralmente <1h)

### SSL
Automático via Vercel (Let's Encrypt).

---

## Monitoramento (opcional)

### Vercel Analytics
Habilitar em: Vercel → Project → Analytics. Gratuito até X requests.

### Uptime monitoring
- **UptimeRobot** (free) — ping a cada 5min em `https://pensare-os.vercel.app`
- **BetterUptime** — alertas via Slack/email

### Logs em produção
```bash
vercel logs https://pensare-os.vercel.app --follow
```

---

## Custo

### GitHub
- Repo público: **grátis**
- Repo privado (se mudar): grátis até 3 colaboradores

### Vercel
- Hobby plan: **grátis** (suficiente para uso atual)
- Pro plan: $20/mês (se precisar mais bandwidth/builds)

### Claude API (via Claude Code CLI)
- Custo varia por uso
- Monitor via `pensare-cost`
- Target sugerido: monitorar mensalmente

### Mac local
- Heartbeat consome ~50MB RAM ocioso
- Custo elétrico desprezível

---

## Próximos passos sugeridos

### Quando ficar pronto para clientes (AI Systemizer)

1. **Multi-tenant**: estruturar `clients/{nome}/pensare-os/` para isolar
2. **CI/CD com tests**: GitHub Actions para validar antes de deploy
3. **Domínio próprio**: `pensare.digital` (não `vercel.app`)
4. **Observability**: Grafana ou Datadog para monitorar latency e erros
5. **Compliance**: LGPD review do que vai pra logs e memory

### Quando escalar internamente

1. **Repo privado** (se conteúdo de cliente entrar)
2. **Branch protection** em `main`
3. **Code review obrigatório** em PRs

---

*Deploy bem feito é o que separa "código rodando" de "sistema operando". Documente as decisões de deploy aqui à medida que evoluir.*
