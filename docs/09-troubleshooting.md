# Troubleshooting — Pensare OS

> Problemas comuns e soluções. Atualizado conforme aparecem novos casos.

---

## Diagnóstico rápido

Antes de mergulhar em problemas específicos, rode:

```bash
pensare-status
```

Saída esperada: `{ "status": "ok", ... }`

Se vier `degraded`, `blocked` ou `error`, veja o `summary` retornado.

---

## Problema: Claude Code não carrega os agentes

### Sintoma
Digito `/pensare` no Claude Code e ele não reconhece.

### Diagnóstico
```bash
# Você está no diretório certo?
pwd
# deve ser: /Users/alicycarvalho/pensare-os

# Os agentes existem?
ls .claude/skills/pensare*/SKILL.md
# deve listar 17 arquivos

# O CLAUDE.md está sendo carregado?
head -5 CLAUDE.md
```

### Solução
1. Sempre invoque `claude` **dentro** do diretório `/Users/alicycarvalho/pensare-os`
2. Verifique que `.claude/skills/` está presente
3. Reinicie o Claude Code (`exit` e abra de novo)

---

## Problema: Heartbeat não executa rotinas

### Sintoma
`launchctl list | grep pensare` mostra o daemon, mas nenhuma rotina roda.

### Diagnóstico
```bash
# Daemon está vivo?
ps aux | grep "heartbeat/daemon"

# Logs de erro?
tail -50 logs/heartbeat-error.log

# State.json não corrompeu?
cat heartbeat/state.json | python -m json.tool

# Quais rotinas rodariam agora?
python heartbeat/daemon.py --dry-run
```

### Soluções comuns

**Daemon morto**:
```bash
launchctl unload ~/Library/LaunchAgents/com.pensare.heartbeat.plist
launchctl load ~/Library/LaunchAgents/com.pensare.heartbeat.plist
```

**State.json corrompido**:
```bash
rm heartbeat/state.json
# próxima execução recria
```

**Erros de permissão**:
```bash
chmod +x heartbeat/daemon.py
chmod +x .claude/skills/_shared/bin/*
```

**Python não encontrado**:
Verifique que o plist usa o Python certo:
```bash
which python3
# atualize ProgramArguments no plist se necessário
```

---

## Problema: Dashboard não sobe

### Sintoma
`python dashboard/server.py` retorna erro.

### Diagnóstico
```bash
# Deps instaladas?
pip list | grep -E "fastapi|uvicorn|pyyaml"

# Porta 8360 livre?
lsof -i :8360

# Erros do server?
python dashboard/server.py 2>&1 | head -30
```

### Soluções

**Deps faltando**:
```bash
pip install -r dashboard/requirements.txt
```

**Porta ocupada**:
```bash
# Identificar processo
lsof -i :8360

# Matar
kill -9 <PID>

# Ou usar outra porta
PORT=8361 python dashboard/server.py
```

**Erro de import**:
Verifique que está rodando do diretório certo:
```bash
cd /Users/alicycarvalho/pensare-os
python dashboard/server.py
```

---

## Problema: Chat do dashboard não responde

### Sintoma
Dashboard `/chat`: envio mensagem e fica carregando indefinidamente.

### Diagnóstico
```bash
# Claude CLI está autenticado?
claude auth status

# Teste manual
claude --print /pensare "teste"

# Veja logs do server
tail -30 logs/dashboard.log
```

### Soluções

**Claude CLI sem auth**:
```bash
claude auth login
```

**Rate limit da Anthropic**:
Espere alguns minutos ou troque para outra conta.

**Timeout muito curto**:
Edite `dashboard/server.py`, encontre `subprocess.run(..., timeout=120)` e aumente para 240.

**Em produção (Vercel)**:
**Não funciona** — Vercel serverless não tem Claude CLI. Use localmente.

---

## Problema: `pensare-log` não encontrado

### Sintoma
```
$ pensare-log lead_captured "..."
zsh: command not found: pensare-log
```

### Solução
```bash
# Verifique o PATH
echo $PATH | tr ':' '\n' | grep pensare

# Se não tiver, adicione:
echo 'export PATH="/Users/alicycarvalho/pensare-os/.claude/skills/_shared/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verifique permissões
ls -la /Users/alicycarvalho/pensare-os/.claude/skills/_shared/bin/
# todos devem ter +x

# Se não tiverem:
chmod +x /Users/alicycarvalho/pensare-os/.claude/skills/_shared/bin/*
```

---

## Problema: Memória corrompida ou inconsistente

### Sintoma
`MEMORY.md` parece bagunçado ou faltam dados. Agentes têm contexto errado.

### Diagnóstico
```bash
# Veja git log do arquivo
git log --oneline MEMORY.md

# Veja último estado conhecido bom
git show HEAD~1:MEMORY.md > /tmp/last-good-memory.md
diff MEMORY.md /tmp/last-good-memory.md
```

### Solução

**Restaurar versão anterior**:
```bash
git checkout HEAD~1 -- MEMORY.md
```

**Reconstruir do log**:
```bash
# tail dos últimos eventos
tail -50 logs/events.ndjson | jq -r '.summary'
# manualmente atualize MEMORY.md com isso
```

**Pedir para o sistema reconstruir**:
```
/pensare reconstrua MEMORY.md a partir dos últimos 50 eventos
```

---

## Problema: Vercel deploy falha

### Sintoma
`vercel --prod` retorna erro de build.

### Diagnóstico
```bash
# Ver logs do último deploy
vercel logs https://pensare-os.vercel.app

# Validar vercel.json
cat vercel.json | python -m json.tool
```

### Soluções

**Build do Python falha**:
- Verifique `requirements.txt` na raiz (não em dashboard/)
- Vercel usa Python 3.12 por padrão; certifique-se que deps suportam

**Path errado em rotas**:
Confirme que `vercel.json` aponta para arquivos que existem:
```bash
ls api/index.py dashboard/index.html
```

**Scope error**:
```bash
vercel --prod --scope <seu-team>
```

---

## Problema: Git push é rejeitado

### Sintoma
```
$ git push origin main
remote: ! [rejected] main -> main (fetch first)
```

### Solução
Alguém (ou outro device) deu push. Faça pull primeiro:
```bash
git pull --rebase origin main
git push origin main
```

Se der conflito de merge:
```bash
# Veja conflitos
git status

# Resolva manualmente os arquivos com <<<<<<< marker
# Depois:
git add <arquivos-resolvidos>
git rebase --continue
git push origin main
```

---

## Problema: Custo explodindo

### Sintoma
`pensare-cost --alert` está disparando frequentemente.

### Diagnóstico
```bash
# Breakdown por tier
pensare-cost

# Quais rotinas estão consumindo mais?
grep -c "agent.*pensare-ceo" logs/events.ndjson
grep -c "agent.*pensare-conselho" logs/events.ndjson
# CEO e Conselho deveriam ser <10% do total
```

### Soluções

**T0/T1 inflado**:
- Coordinator/CEO/Conselho estão fazendo trabalho de Head ou Execution
- Revise prompts: estão pedindo análises longas demais?

**Heartbeat rodando rotinas desnecessárias**:
- Desative rotinas que você não lê
- Aumente intervalos (de daily para weekly)

**Muitas iterações entre tiers**:
- Coordinator não está entregando contexto suficiente em handoffs
- Adicione mais `quality_gates` para evitar idas e vindas

---

## Problema: Heartbeat trigger não dispara

### Sintoma
Registro um evento via `pensare-log lead_captured "..."` mas o `/pensare-sdr` não é acionado.

### Diagnóstico
```bash
# Evento foi registrado?
tail -1 logs/events.ndjson

# HEARTBEAT.md tem o trigger configurado?
grep -A 5 "lead_captured" HEARTBEAT.md

# Daemon detectou?
tail -20 logs/heartbeat.log
```

### Solução

**Daemon ainda não rodou** (espera o próximo ciclo de 60s).

**Trigger mal configurado**:
Edite `HEARTBEAT.md`. Formato correto:
```yaml
### lead_captured → /pensare-sdr
```yaml
event_type: "lead_captured"
agente: /pensare-sdr
prompt: |
  ...
```

**Forçar execução**:
```bash
python heartbeat/daemon.py --once
```

---

## Problema: Arquivo grande no `.gitignore` foi commitado por engano

### Sintoma
`logs/events.ndjson` ou `heartbeat/state.json` está no Git.

### Solução
```bash
# Remover do tracking (mantendo local)
git rm --cached logs/events.ndjson
git rm --cached heartbeat/state.json
git commit -m "chore: remove tracked files that should be gitignored"
git push origin main
```

Se o arquivo é muito grande e está no histórico:
```bash
# Use git-filter-repo (instalar via brew)
brew install git-filter-repo
git filter-repo --path logs/events.ndjson --invert-paths

# OBS: reescreve histórico — coordene com colaboradores
git push --force origin main
```

---

## Problema: Reflexões vazias ou agentes "esquecidos"

### Sintoma
`memory/per-agent/{nome}/reflections.md` está vazio ou desatualizado.

### Causa
Agentes não estão registrando reflexão pós-ação.

### Solução

**Forçar reflexão manualmente**:
```
/pensare-comercial revise as últimas 5 vendas em logs/events.ndjson e
atualize sua reflections.md com lições significativas
```

**Adicionar reflexão como passo obrigatório**:
No `SKILL.md` do agente, adicione:
```yaml
quality_gates:
  - "Reflexão registrada em memory/per-agent/{nome}/reflections.md se houve aprendizado"
```

---

## Problema: Skill não está sendo aplicada

### Sintoma
Invoco agente, mas ele não usa a skill esperada.

### Diagnóstico
```bash
# Skill existe?
ls .claude/skills/skills/<nome-skill>/SKILL.md

# Está no skills_used do agente?
grep -A 5 skills_used .claude/skills/pensare-<agente>/SKILL.md
```

### Solução

**Skill não declarada no agente**:
Edite frontmatter do agente:
```yaml
skills_used:
  - lead-qualification
  - commercial-diagnosis
```

**Invocar skill explicitamente**:
```
/pensare-sdr aplique a skill lead-qualification para este lead: ...
```

---

## Problema: Workspace path errado (em outro Mac/conta)

### Sintoma
Erros tipo "FileNotFoundError: /Users/alicycarvalho/pensare-os/..."

### Solução
Use a env var `PENSARE_WORKSPACE`:

```bash
export PENSARE_WORKSPACE=/Users/seu-user/pensare-os
python dashboard/server.py
```

Ou edite `dashboard/server.py` para usar path relativo:
```python
WORKSPACE_ROOT = Path(__file__).parent.parent
```

---

## Quando pedir ajuda

Se nenhuma solução acima resolveu, colete o seguinte e envie:

```bash
# 1. Status do sistema
pensare-status > /tmp/diagnostic.txt

# 2. Últimos eventos
tail -30 logs/events.ndjson >> /tmp/diagnostic.txt

# 3. Erros recentes
tail -30 logs/heartbeat-error.log >> /tmp/diagnostic.txt
tail -30 logs/dashboard.log >> /tmp/diagnostic.txt 2>/dev/null

# 4. Estado do Git
git status >> /tmp/diagnostic.txt
git log --oneline -10 >> /tmp/diagnostic.txt

# 5. Versões
echo "Python: $(python --version)" >> /tmp/diagnostic.txt
echo "Claude: $(claude --version 2>/dev/null || echo 'not found')" >> /tmp/diagnostic.txt

cat /tmp/diagnostic.txt
```

Envie esse output. **Não envie tokens, chaves, ou dados de clientes**.

---

## Comandos úteis de emergência

### Resetar completamente

```bash
# CUIDADO: apaga estado local mas não memória
rm -rf logs/events.ndjson heartbeat/state.json
git checkout HEAD -- MEMORY.md
```

### Verificar integridade dos arquivos canônicos

```bash
for f in SOUL.md IDENTITY.md AGENTS.md HEARTBEAT.md TOOLS.md CLAUDE.md MEMORY.md; do
  [ -f "$f" ] && echo "✓ $f" || echo "✗ $f MISSING"
done
```

### Reinstalar tudo

```bash
cd /Users/alicycarvalho/pensare-os
bash setup.sh
# responde "s" para heartbeat
```

---

*Adicione novos casos aqui conforme aparecem — esse arquivo evolui com o uso.*
