# Heartbeat Runbook — Pensare OS

> Operação do daemon de heartbeat: instalação, monitoramento, troubleshooting.

---

## O que é o Heartbeat

O **Heartbeat** é o **sistema nervoso autônomo** do Pensare OS. Sem ele, o sistema só responde quando você chama. Com ele, o sistema antecipa.

### Função
1. **Monitora** métricas continuamente
2. **Identifica** desvios e padrões
3. **Aciona** os agentes corretos
4. **Mantém** ritmo de execução
5. **Registra** aprendizado

### Pergunta central
> "O sistema está melhorando ou piorando?"

---

## Arquitetura

```
┌────────────────────────────────────────────────────┐
│  Mac launchd (StartInterval: 60s)                  │
│  Plist: ~/Library/LaunchAgents/com.pensare.heartbeat.plist │
└────────────────────┬───────────────────────────────┘
                     │ chama a cada 60s
                     ▼
┌────────────────────────────────────────────────────┐
│  heartbeat/daemon.py                               │
│                                                    │
│  1. Lê HEARTBEAT.md                                │
│  2. Lê heartbeat/state.json                        │
│  3. Para cada rotina:                              │
│       should_run() ?                               │
│  4. Se sim:                                        │
│       subprocess: claude --print /agente {prompt}  │
│  5. Atualiza state.json                            │
│  6. Registra evento em logs/events.ndjson          │
└────────────────────────────────────────────────────┘
```

---

## Instalação

### Setup automatizado (recomendado)

```bash
cd /Users/alicycarvalho/pensare-os
bash setup.sh
```

Quando perguntar:
```
Instalar heartbeat automático? (s/n):
```
Digite `s`.

### Instalação manual

```bash
# 1. Garantir permissões
chmod +x heartbeat/daemon.py
chmod +x heartbeat/install.sh

# 2. Instalar o LaunchAgent
bash heartbeat/install.sh

# 3. Verificar que carregou
launchctl list | grep pensare
# deve mostrar: com.pensare.heartbeat
```

### Conteúdo do plist gerado

`~/Library/LaunchAgents/com.pensare.heartbeat.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.pensare.heartbeat</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/alicycarvalho/pensare-os/heartbeat/daemon.py</string>
    </array>
    <key>StartInterval</key>
    <integer>60</integer>
    <key>StandardOutPath</key>
    <string>/Users/alicycarvalho/pensare-os/logs/heartbeat.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/alicycarvalho/pensare-os/logs/heartbeat-error.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

---

## Comandos operacionais

### Preview (não executa nada)

```bash
python heartbeat/daemon.py --dry-run
```

Lista quais rotinas rodariam agora.

### Execução única (debug)

```bash
python heartbeat/daemon.py --once
```

Roda uma iteração completa e sai. Útil para testar.

### Daemon contínuo (foreground)

```bash
python heartbeat/daemon.py
```

Loop infinito, verifica a cada 60s. Use `Ctrl+C` para parar.

### Status do LaunchAgent

```bash
launchctl list com.pensare.heartbeat
```

Saída esperada:
```
{
    "StandardOutPath" = "/Users/.../heartbeat.log";
    "Label" = "com.pensare.heartbeat";
    "OnDemand" = false;
    "LastExitStatus" = 0;
    "PID" = 12345;
}
```

`LastExitStatus = 0` significa última execução bem-sucedida.

### Ver logs

```bash
# Output normal
tail -f logs/heartbeat.log

# Erros
tail -f logs/heartbeat-error.log

# Eventos gerados
tail -f logs/events.ndjson
```

### Parar temporariamente

```bash
launchctl unload ~/Library/LaunchAgents/com.pensare.heartbeat.plist
```

### Reiniciar

```bash
launchctl unload ~/Library/LaunchAgents/com.pensare.heartbeat.plist
launchctl load ~/Library/LaunchAgents/com.pensare.heartbeat.plist
```

### Desinstalar permanentemente

```bash
launchctl unload ~/Library/LaunchAgents/com.pensare.heartbeat.plist
rm ~/Library/LaunchAgents/com.pensare.heartbeat.plist
```

---

## Rotinas configuradas

Definidas em `HEARTBEAT.md`. Resumo:

### Daily

| Horário | Agente | Função |
|---------|--------|--------|
| 08:00 | `/pensare-inteligencia` | Daily Brief — resumo + métricas + foco do dia |
| 09:00 | `/pensare-comercial` | Pipeline review — leads sem movimentação, propostas vencendo |
| 16:00 | `/pensare-cs` | Check de clientes — risco de churn |
| 18:00 | `/pensare` | Fechamento — atualiza MEMORY.md + evento session_close |

### Weekly

| Quando | Agente | Função |
|--------|--------|--------|
| Seg 08:30 | `/pensare-ceo` | Weekly planning — 5 prioridades da semana |
| Qua 10:00 | `/pensare-inteligencia` | Market intel — concorrência, oportunidades |
| Sex 17:00 | `/pensare-conselho` | Weekly review — lições + ajuste de rota |

### Monthly

| Quando | Agente | Função |
|--------|--------|--------|
| Dia 1, 09:00 | `/pensare-financeiro` | Monthly close — receita, unit economics |
| Dia 15, 09:00 | `/pensare-produto` | Mid-month review — NPS, feedback, oferta |

### Gatilhos por evento (sem horário fixo)

Disparam **imediatamente** quando o evento aparece em `logs/events.ndjson`:

- `lead_captured` → SDR
- `proposal_sent` → Closer (setup follow-up)
- `client_inactive_7d` → CS (churn-prevention)
- `conversion_dropped` → Comercial (funnel-diagnosis)
- `cpl_increased` → Tráfego
- `offer_not_converting` → Produto
- `strategic_decision_required` → Conselho
- `financial_alert` → Financeiro
- `session_no_closing` → Coordinator (closing retroativo)

---

## Thresholds e Alertas

Definidos em `HEARTBEAT.md`. Resumo:

| Métrica | Saudável | Alerta | Crítico |
|---------|----------|--------|---------|
| CTR | ≥1.5% | <1.5% | <1.0% |
| CPL | dentro meta | +15% vs meta | +30% vs meta |
| Conversão SQL→venda | ≥10% | <10% | <7% |
| Churn mensal | <5% | 5–10% | >10% |
| NPS | >70 | 50–70 | <50 |
| Capacidade utilizada | ≤80% | 80–95% | >95% |
| LTV:CAC | >3x | 2–3x | <2x |
| Runway | >6 meses | 3–6 | <3 |

### Níveis de alerta

| Nível | Quem é notificado | Ação |
|-------|------------------|------|
| **Crítico** | CEO + Conselho + Isis (PushNotification) | Decisão estratégica imediata |
| **Moderado** | Head da área responsável | Ajuste tático |
| **Leve** | Apenas log | Monitorar |

---

## Editando rotinas

### Adicionar rotina nova

Edite `HEARTBEAT.md` adicionando bloco:

```yaml
### [HH:MM] Nome da Rotina
```yaml
agente: /pensare-<agente>
foco: Descrição breve
ler:
  - arquivo1.md
  - arquivo2.md
acoes:
  - ação 1
  - ação 2
output: memory/shared/output-{YYYY-MM-DD}.md
condition: condição opcional
```

Salve. O daemon detecta na próxima iteração (≤60s).

### Modificar threshold

Edite a tabela em `HEARTBEAT.md` na seção "Thresholds". A próxima execução do daemon usa o novo valor.

### Desativar rotina temporariamente

Comente o bloco em `HEARTBEAT.md`:

```markdown
<!--
### [08:00] Daily Brief
...
-->
```

---

## Estado do daemon

### `heartbeat/state.json`

Mantém última execução de cada rotina:

```json
{
  "routines": {
    "daily-brief-0800": {
      "last_run": "2026-05-13T08:00:14Z",
      "last_status": "ok",
      "consecutive_failures": 0
    },
    "pipeline-review-0900": {
      "last_run": "2026-05-13T09:00:22Z",
      "last_status": "ok",
      "consecutive_failures": 0
    }
  },
  "version": 1
}
```

**Está no `.gitignore`** — é estado local da máquina.

### Limpar estado (forçar re-execução)

```bash
rm heartbeat/state.json
# próxima iteração do daemon vai rodar tudo que está no horário
```

---

## Troubleshooting

### Daemon não está rodando

```bash
launchctl list | grep pensare
```

Se não retornar nada:

```bash
bash heartbeat/install.sh
```

### Rotinas não executam

Verifique:

```bash
# 1. Daemon está vivo?
ps aux | grep "heartbeat/daemon"

# 2. Tem erro nos logs?
tail -30 logs/heartbeat-error.log

# 3. HEARTBEAT.md é parseável?
python heartbeat/daemon.py --dry-run

# 4. State.json não está corrompido?
cat heartbeat/state.json | python -m json.tool
```

### Claude CLI não responde

```bash
# Teste manualmente
claude --print /pensare "teste"
```

Se travar:
- Verifique autenticação: `claude auth status`
- Verifique rate limits da Anthropic
- Aumente timeout em `daemon.py` (`subprocess.run(..., timeout=120)`)

### Permissões negadas

```bash
chmod +x heartbeat/daemon.py
chmod +x .claude/skills/_shared/bin/*
```

### LaunchAgent não carrega ao reiniciar Mac

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.pensare.heartbeat.plist
```

(macOS Sonoma+ pode exigir essa sintaxe ao invés de `load`.)

---

## Boas práticas

### 1. Não acumule rotinas desnecessárias
Cada rotina ativa consome custo. Pergunte: **"Se eu não tivesse essa rotina, eu sentiria falta?"** Se a resposta for "não", remova.

### 2. Alinhe horários com seu ritmo real
Se você dorme até 9h, não faz sentido daily brief às 7h. Ajuste `HEARTBEAT.md` à sua realidade.

### 3. Monitor o cost vs valor
```bash
pensare-cost --alert
```
Se uma rotina gera muito custo mas pouco valor (você não age sobre o output), desative.

### 4. Revise mensalmente
No fim de cada mês, pergunte:
- Quais rotinas eu li nos últimos 30 dias?
- Quais geraram ação real?
- Quais foram ignoradas?

Desative as ignoradas.

---

## Métricas de saúde do próprio Heartbeat

```bash
pensare-status
```

Retorna estado agregado:
```json
{
  "status": "ok",
  "heartbeat": {
    "daemon_running": true,
    "last_routine_executed": "2026-05-13T09:00:22Z",
    "failures_last_24h": 0,
    "scheduled_today": 4,
    "executed_today": 3,
    "next_scheduled": "16:00 — CS Check"
  }
}
```

---

*Heartbeat bem configurado é a diferença entre "ter um sistema" e "operar dentro de um sistema". Configure uma vez, revise mensalmente.*
