# Getting Started — Pensare OS

> Setup completo do Pensare OS do zero até a primeira operação real.

---

## Pré-requisitos

| Requisito | Versão mínima | Como verificar |
|-----------|--------------|----------------|
| **Windows** | 10/11 | — |
| **Python** | 3.10+ | `python --version` |
| **Git** | 2.30+ | `git --version` |
| **Claude Code CLI** | última versão | `claude --version` |
| **Node.js** (opcional, p/ Vercel CLI) | 18+ | `node --version` |

### Instalação dos pré-requisitos

```bash
# Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Vercel CLI (opcional)
npm install -g vercel
```

---

## Setup completo (passo a passo)

### 1. Clone o repositório

```bash
git clone https://github.com/jcarvalho7103/pensare-os.git
cd pensare-os
```

### 2. Instale as dependências Python

```bash
pip install -r requirements.txt
```

Dependências: `fastapi`, `uvicorn`, `pyyaml`, `python-multipart`, `openai`, `supabase`

### 3. Suba o dashboard

```bash
python dashboard/server.py
```

Acesse: **http://localhost:8360**

### 4. Use o Claude Code no diretório

```bash
cd pensare-os
claude
> /pensare ola, qual o status do sistema?
```

---

## Verificação rápida

Após o setup, verifique:

```bash
# Dashboard respondendo
curl http://localhost:8360/api/metrics

# Agentes carregados
curl http://localhost:8360/api/agents

# Chat funcionando (via Claude CLI)
curl -X POST http://localhost:8360/api/chat \
  -H "Content-Type: application/json" \
  -d '{"agent":"pensare-ceo","message":"status do sistema"}'
```

---

## Banco de dados (Supabase)

O sistema usa Supabase como banco central para dados dinâmicos (eventos, tasks, heartbeat).

- **URL**: `https://tplwqvvffanwsyhgufya.supabase.co`
- **Tabelas**: `events`, `tasks`, `heartbeat_state`, `memory_files`

As credenciais já estão configuradas no `server.py` (defaults) e na Vercel (env vars).

---

## Primeiro uso

### Via dashboard (http://localhost:8360)

1. Acesse a aba **Chat**
2. Selecione um agente (ex: `pensare-ceo`)
3. Envie uma mensagem
4. O Claude CLI processa e responde

### Via terminal (Claude Code CLI)

```bash
cd pensare-os
claude

# Usar o coordinator (roteia automaticamente)
> /pensare preciso de uma estrategia de lancamento para o produto X

# Usar agente específico
> /pensare-ceo quais são as prioridades da semana?
> /pensare-growth monte um funil de aquisição para SaaS B2B
> /pensare-financeiro analise o P&L do último trimestre
```

---

## Agentes disponíveis

| Agente | Função |
|--------|--------|
| `/pensare` | Coordinator — roteia para o agente correto |
| `/pensare-ceo` | CEO — orquestra todos os Heads |
| `/pensare-conselho` | Conselho — decisões estratégicas de alto nível |
| `/pensare-growth` | Growth — aquisição e funil |
| `/pensare-comercial` | Comercial — pipeline de vendas |
| `/pensare-produto` | Produto — oferta e roadmap |
| `/pensare-financeiro` | Financeiro — P&L e pricing |
| `/pensare-operacoes` | Operações — processos e SLAs |
| `/pensare-estrategia` | Estratégia — posicionamento |
| `/pensare-cs` | Customer Success — retenção |
| `/pensare-inteligencia` | Inteligência — pesquisa de mercado |
| `/pensare-automacao` | Automação — sistemas e integrações |
| `/pensare-trafego` | Tráfego — campanhas pagas |
| `/pensare-copy` | Copy — textos persuasivos |
| `/pensare-criativos` | Criativos — direção criativa |
| `/pensare-dados` | Dados — analytics |
| `/pensare-sdr` | SDR — prospecção |
| `/pensare-closer` | Closer — fechamento de vendas |

---

## Produção (Vercel)

O dashboard está deployado em **https://pensare-os.vercel.app**.

Funciona: métricas, eventos, tasks, visualização de agentes/soul.
Não funciona: chat (requer Claude CLI ou API key).

Cada `git push origin main` redeploya automaticamente.

---

## Próximos passos

Após o setup:
1. Edite `_contexto/empresa.md` com os dados reais do seu negócio
2. Edite `_contexto/mercado.md` com seu mercado-alvo
3. Use `/pensare` para começar a operar
4. Acompanhe pelo dashboard as métricas e eventos
