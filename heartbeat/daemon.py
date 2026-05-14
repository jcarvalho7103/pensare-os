#!/usr/bin/env python3
"""
heartbeat/daemon.py — Daemon de heartbeat do Pensare OS.

Lê HEARTBEAT.md, parseia rotinas agendadas e as executa via `claude --print`.
Mantém estado em heartbeat/state.json para não re-executar rotinas no mesmo dia.

Usage:
    python daemon.py           # loop infinito (daemon real)
    python daemon.py --once    # executa pendentes agora e sai
    python daemon.py --dry-run # mostra o que rodaria sem executar
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Caminhos base
BASE_DIR = Path("/Users/alicycarvalho/pensare-os")
HEARTBEAT_MD = BASE_DIR / "HEARTBEAT.md"
STATE_FILE = BASE_DIR / "heartbeat" / "state.json"
LOG_FILE = BASE_DIR / "logs" / "heartbeat.log"
EVENTS_LOG = BASE_DIR / "logs" / "events.ndjson"
PENSARE_LOG_BIN = BASE_DIR / ".claude" / "skills" / "_shared" / "bin" / "pensare-log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("pensare.heartbeat")


# ---------------------------------------------------------------------------
# Parsing do HEARTBEAT.md
# ---------------------------------------------------------------------------

ROUTINE_HEADER_RE = re.compile(r"^###\s+\[(\d{2}:\d{2})\]\s+(.+)$")
FIELD_RE = re.compile(r"^(skill|prompt|condition):\s*(.+)$")


def parse_heartbeat_md(path: Path) -> list[dict]:
    """
    Parseia HEARTBEAT.md e retorna lista de rotinas.

    Formato esperado:
        ### [HH:MM] Nome da Rotina
        skill: pensare-xxx
        prompt: "texto do prompt"
        condition: "expressão Python opcional"

    Retorna lista de dicts:
        {
            "time": "HH:MM",
            "name": "Nome da Rotina",
            "skill": "pensare-xxx",
            "prompt": "texto",
            "condition": "expr ou None",
        }
    """
    if not path.exists():
        log.warning("HEARTBEAT.md não encontrado em %s", path)
        return []

    routines: list[dict] = []
    current: Optional[dict] = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            header_match = ROUTINE_HEADER_RE.match(line)
            if header_match:
                # Salva rotina anterior se estava em construção
                if current and current.get("prompt"):
                    routines.append(current)
                current = {
                    "time": header_match.group(1),
                    "name": header_match.group(2).strip(),
                    "skill": None,
                    "prompt": None,
                    "condition": None,
                }
                continue

            if current is None:
                continue

            field_match = FIELD_RE.match(line)
            if field_match:
                key = field_match.group(1)
                val = field_match.group(2).strip().strip('"')
                current[key] = val

    # Salva a última rotina
    if current and current.get("prompt"):
        routines.append(current)

    log.info("Parseadas %d rotinas de %s", len(routines), path)
    return routines


# ---------------------------------------------------------------------------
# Estado
# ---------------------------------------------------------------------------

def load_state() -> dict:
    """Carrega state.json. Retorna {} se não existir."""
    if not STATE_FILE.exists():
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        log.warning("Falha ao ler state.json: %s — iniciando estado limpo.", e)
        return {}


def save_state(state: dict) -> None:
    """Persiste state.json."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def state_key(routine: dict) -> str:
    """Chave única para identificar uma rotina no estado."""
    return f"{routine['time']}:{routine['name']}"


def update_state(routine: dict, state: dict) -> None:
    """Marca rotina como executada hoje."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    key = state_key(routine)
    state[key] = {"last_run": today, "name": routine["name"]}
    save_state(state)


# ---------------------------------------------------------------------------
# Decisão de execução
# ---------------------------------------------------------------------------

def should_run(routine: dict, state: dict) -> bool:
    """
    Retorna True se a rotina deve rodar agora.

    Critérios:
    1. Horário agendado já passou no dia de hoje (comparação HH:MM).
    2. Rotina ainda não rodou hoje.
    3. Se tem condition, avalia como Python — False impede execução.
    """
    now = datetime.now(timezone.utc)
    today_str = now.strftime("%Y-%m-%d")
    current_hhmm = now.strftime("%H:%M")

    # Verifica se o horário já chegou
    if current_hhmm < routine["time"]:
        return False

    # Verifica se já rodou hoje
    key = state_key(routine)
    entry = state.get(key, {})
    if entry.get("last_run") == today_str:
        return False

    # Avalia condição opcional
    condition = routine.get("condition")
    if condition:
        try:
            # Contexto mínimo disponível para a condição
            ctx = {
                "now": now,
                "today": today_str,
                "weekday": now.weekday(),  # 0=segunda, 6=domingo
            }
            result = eval(condition, {"__builtins__": {}}, ctx)  # noqa: S307
            if not result:
                log.debug("Condição falsa para '%s': %s", routine["name"], condition)
                return False
        except Exception as e:
            log.warning("Erro ao avaliar condição '%s': %s — ignorando rotina.", condition, e)
            return False

    return True


# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------

def emit_event(agent: str, action: str, **kwargs) -> None:
    """Loga evento via pensare-log se o binário existir."""
    if not PENSARE_LOG_BIN.exists():
        return
    args = [str(PENSARE_LOG_BIN), agent, action]
    args.extend(f"{k}={v}" for k, v in kwargs.items())
    try:
        subprocess.run(args, check=False, timeout=5)
    except Exception as e:
        log.debug("pensare-log falhou: %s", e)


def execute_routine(routine: dict) -> dict:
    """
    Executa a rotina via:
        claude --dangerously-skip-permissions --print "<prompt>" | tee -a logs/heartbeat.log

    Retorna dict com:
        success: bool
        returncode: int
        stdout: str (primeiros 500 chars)
        error: str (se falhou)
    """
    prompt = routine["prompt"]
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    cmd = (
        f'claude --dangerously-skip-permissions --print {json.dumps(prompt)}'
        f' | tee -a {LOG_FILE}'
    )

    log.info("Executando rotina '%s' [%s]", routine["name"], routine["time"])
    emit_event("heartbeat", "start", routine=routine["name"])

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutos máximo por rotina
        )
        success = result.returncode == 0
        if success:
            emit_event("heartbeat", "complete", routine=routine["name"])
        else:
            emit_event(
                "heartbeat", "error",
                routine=routine["name"],
                returncode=str(result.returncode),
            )
        return {
            "success": success,
            "returncode": result.returncode,
            "stdout": result.stdout[:500],
            "error": result.stderr[:200] if not success else "",
        }
    except subprocess.TimeoutExpired:
        msg = f"Rotina '{routine['name']}' excedeu timeout de 300s."
        log.error(msg)
        emit_event("heartbeat", "error", routine=routine["name"], reason="timeout")
        return {"success": False, "returncode": -1, "stdout": "", "error": msg}
    except Exception as e:
        msg = str(e)
        log.error("Erro inesperado ao executar '%s': %s", routine["name"], msg)
        emit_event("heartbeat", "error", routine=routine["name"], reason=msg[:100])
        return {"success": False, "returncode": -1, "stdout": "", "error": msg}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_pending(routines: list[dict], state: dict, dry_run: bool) -> int:
    """
    Verifica e executa rotinas pendentes.
    Retorna o número de rotinas processadas.
    """
    ran = 0
    for routine in routines:
        if not should_run(routine, state):
            continue
        if dry_run:
            log.info("[DRY-RUN] Rodaria: '%s' [%s] — prompt: %s",
                     routine["name"], routine["time"], routine["prompt"][:80])
            ran += 1
            continue
        result = execute_routine(routine)
        if result["success"]:
            log.info("Rotina '%s' concluída com sucesso.", routine["name"])
        else:
            log.error("Rotina '%s' falhou: %s", routine["name"], result["error"])
        update_state(routine, state)
        ran += 1
    return ran


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Heartbeat daemon do Pensare OS."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que rodaria sem executar nada.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Executa todas as rotinas pendentes agora e sai.",
    )
    args = parser.parse_args()

    log.info("Pensare OS Heartbeat iniciando. dry_run=%s, once=%s",
             args.dry_run, args.once)

    if args.once or args.dry_run:
        routines = parse_heartbeat_md(HEARTBEAT_MD)
        state = load_state()
        ran = run_pending(routines, state, dry_run=args.dry_run)
        log.info("Modo --once/%s: %d rotina(s) processada(s). Saindo.",
                 "dry-run" if args.dry_run else "once", ran)
        sys.exit(0)

    # Modo daemon: loop infinito
    log.info("Modo daemon ativo. Verificando a cada 30 segundos.")
    while True:
        try:
            routines = parse_heartbeat_md(HEARTBEAT_MD)
            state = load_state()
            ran = run_pending(routines, state, dry_run=False)
            if ran:
                log.info("Ciclo: %d rotina(s) executada(s).", ran)
        except KeyboardInterrupt:
            log.info("Heartbeat encerrado pelo usuário.")
            sys.exit(0)
        except Exception as e:
            # Nunca deixa o daemon morrer por erro de uma iteração
            log.error("Erro no ciclo do daemon: %s", e)

        time.sleep(30)


if __name__ == "__main__":
    main()
