"""
Pensare OS Dashboard — FastAPI Backend
Run: python server.py
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

WORKSPACE_ROOT = Path(os.environ.get("PENSARE_WORKSPACE", "/Users/alicycarvalho/pensare-os"))
DASHBOARD_DIR = WORKSPACE_ROOT / "dashboard"
SKILLS_DIR = WORKSPACE_ROOT / ".claude" / "skills"
LOGS_DIR = WORKSPACE_ROOT / "logs"
EVENTS_FILE = LOGS_DIR / "events.ndjson"
MEMORY_DIR = WORKSPACE_ROOT / "memory"
HEARTBEAT_FILE = WORKSPACE_ROOT / "HEARTBEAT.md"
HEARTBEAT_STATE = WORKSPACE_ROOT / "heartbeat" / "state.json"
MEMORY_FILE = WORKSPACE_ROOT / "MEMORY.md"
SOUL_FILE = WORKSPACE_ROOT / "SOUL.md"
IDENTITY_FILE = WORKSPACE_ROOT / "IDENTITY.md"
AGENTS_FILE = WORKSPACE_ROOT / "AGENTS.md"
TOOLS_FILE = WORKSPACE_ROOT / "TOOLS.md"
CONTEXTO_DIR = WORKSPACE_ROOT / "_contexto"

CARGA_PADRAO = [
    WORKSPACE_ROOT / "SOUL.md",
    WORKSPACE_ROOT / "IDENTITY.md",
    WORKSPACE_ROOT / "AGENTS.md",
    WORKSPACE_ROOT / "MEMORY.md",
    WORKSPACE_ROOT / "TOOLS.md",
    WORKSPACE_ROOT / "HEARTBEAT.md",
    WORKSPACE_ROOT / "CLAUDE.md",
]

app = FastAPI(title="Pensare OS Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8360", "http://127.0.0.1:8360"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = DASHBOARD_DIR / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_read(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return default


def read_ndjson_tail(path: Path, n: int = 200) -> list[dict]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    result = []
    for line in lines[-n:]:
        line = line.strip()
        if not line:
            continue
        try:
            result.append(json.loads(line))
        except Exception:
            pass
    return result


def validate_path(rel_path: str) -> Path:
    """Prevent path traversal — ensure path stays inside WORKSPACE_ROOT."""
    target = (WORKSPACE_ROOT / rel_path).resolve()
    if not str(target).startswith(str(WORKSPACE_ROOT.resolve())):
        raise HTTPException(status_code=400, detail="Path traversal denied")
    return target


def append_event(agent: str, event_type: str, summary: str, payload: dict | None = None):
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "agent": agent,
        "type": event_type,
        "summary": summary,
        "payload": payload or {},
    }
    with EVENTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except Exception:
        return {}


def today_str() -> str:
    return date.today().isoformat()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = DASHBOARD_DIR / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(str(index_file), media_type="text/html")


# ---------------------------------------------------------------------------
# GET /api/metrics
# ---------------------------------------------------------------------------

@app.get("/api/metrics")
async def get_metrics():
    events = read_ndjson_tail(EVENTS_FILE, 200)
    today = today_str()

    events_today = [e for e in events if e.get("ts", "").startswith(today)]
    erros_hoje = sum(1 for e in events_today if e.get("type") in ("error", "erro"))
    agentes_hoje = len({e.get("agent") for e in events_today if e.get("agent")})

    empresa_text = safe_read(CONTEXTO_DIR / "empresa.md")
    empresa_nome = "Pensare"
    for line in empresa_text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            empresa_nome = line.lstrip("#").strip()
            break

    return {
        "empresa": empresa_nome,
        "leads_hoje": 0,
        "sql": 0,
        "vendas": 0,
        "receita": "R$ 0",
        "cpl": "—",
        "conversao": "0%",
        "eventos_hoje": len(events_today),
        "erros_hoje": erros_hoje,
        "agentes_hoje": agentes_hoje,
        "total_eventos": len(events),
    }


# ---------------------------------------------------------------------------
# GET /api/events
# ---------------------------------------------------------------------------

@app.get("/api/events")
async def get_events():
    events = read_ndjson_tail(EVENTS_FILE, 200)
    return {"events": events[-50:][::-1]}


# ---------------------------------------------------------------------------
# GET /api/agents
# ---------------------------------------------------------------------------

@app.get("/api/agents")
async def get_agents():
    if not SKILLS_DIR.exists():
        return {"agents": []}

    agents = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or not skill_dir.name.startswith("pensare"):
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        text = safe_read(skill_md)
        fm = parse_frontmatter(text)
        # Strip frontmatter from description body
        body = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            body = parts[2].strip() if len(parts) >= 3 else text

        agents.append({
            "id": skill_dir.name,
            "name": fm.get("name", skill_dir.name),
            "description": fm.get("description", ""),
            "tier": fm.get("tier", "unknown"),
            "reports_to": fm.get("reports_to", ""),
            "version": fm.get("version", ""),
            "allowed_tools": fm.get("allowed-tools", ""),
            "command": f"/{skill_dir.name}",
        })

    tier_order = {"coordinator": 0, "c-suite": 1, "head": 2, "execution": 3, "unknown": 4}
    agents.sort(key=lambda a: (tier_order.get(a["tier"], 4), a["name"]))
    return {"agents": agents}


# ---------------------------------------------------------------------------
# GET /api/memory/tree
# ---------------------------------------------------------------------------

@app.get("/api/memory/tree")
async def get_memory_tree():
    sections = []

    # Carga Padrão
    carga_files = []
    for f in CARGA_PADRAO:
        carga_files.append({
            "name": f.name,
            "path": str(f.relative_to(WORKSPACE_ROOT)),
            "exists": f.exists(),
            "size": f.stat().st_size if f.exists() else 0,
        })
    sections.append({"name": "Carga Padrão", "files": carga_files})

    # _contexto/
    contexto_files = []
    if CONTEXTO_DIR.exists():
        for f in sorted(CONTEXTO_DIR.rglob("*.md")):
            contexto_files.append({
                "name": f.name,
                "path": str(f.relative_to(WORKSPACE_ROOT)),
                "exists": True,
                "size": f.stat().st_size,
            })
    if contexto_files:
        sections.append({"name": "_contexto", "files": contexto_files})

    # memory/shared/
    shared_files = []
    shared_dir = MEMORY_DIR / "shared"
    if shared_dir.exists():
        for f in sorted(shared_dir.rglob("*")):
            if f.is_file():
                shared_files.append({
                    "name": f.name,
                    "path": str(f.relative_to(WORKSPACE_ROOT)),
                    "exists": True,
                    "size": f.stat().st_size,
                })
    if shared_files:
        sections.append({"name": "memory/shared", "files": shared_files})

    # memory/per-agent/
    per_agent_files = []
    per_agent_dir = MEMORY_DIR / "per-agent"
    if per_agent_dir.exists():
        for f in sorted(per_agent_dir.rglob("*")):
            if f.is_file():
                per_agent_files.append({
                    "name": f"{f.parent.name}/{f.name}",
                    "path": str(f.relative_to(WORKSPACE_ROOT)),
                    "exists": True,
                    "size": f.stat().st_size,
                })
    if per_agent_files:
        sections.append({"name": "memory/per-agent", "files": per_agent_files})

    return {"sections": sections}


# ---------------------------------------------------------------------------
# GET /api/memory/file
# ---------------------------------------------------------------------------

@app.get("/api/memory/file")
async def get_memory_file(path: str = Query(...)):
    target = validate_path(path)
    if not target.exists():
        return {"content": "", "path": path, "exists": False}
    return {"content": safe_read(target), "path": path, "exists": True}


# ---------------------------------------------------------------------------
# PUT /api/memory/file
# ---------------------------------------------------------------------------

class FileWriteRequest(BaseModel):
    path: str
    content: str


@app.put("/api/memory/file")
async def put_memory_file(req: FileWriteRequest):
    target = validate_path(req.path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(req.content, encoding="utf-8")
    append_event("dashboard", "file_write", f"Arquivo salvo: {req.path}")
    return {"ok": True, "path": req.path}


# ---------------------------------------------------------------------------
# GET /api/tasks
# ---------------------------------------------------------------------------

def parse_tasks_from_memory(text: str) -> dict:
    pending, in_progress, done = [], [], []

    in_next_steps = False
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{1,3}\s+(next steps|próximos passos|tasks|tarefas)", stripped, re.IGNORECASE):
            in_next_steps = True
            continue
        if in_next_steps and re.match(r"^#{1,3}\s+", stripped):
            in_next_steps = False
        if not in_next_steps:
            continue

        # [ ] pending  [x] done  [~] in progress
        m = re.match(r"[-*]\s+\[([ xX~])\]\s+(.*)", stripped)
        if m:
            state, title = m.group(1), m.group(2).strip()
            priority = "medium"
            pm = re.search(r"\[!(urgent|high|medium|low)\]", title, re.IGNORECASE)
            if pm:
                priority = pm.group(1).lower()
                title = re.sub(r"\[!(urgent|high|medium|low)\]", "", title, flags=re.IGNORECASE).strip()
            task = {"title": title, "priority": priority}
            if state in (" ", ""):
                pending.append(task)
            elif state in ("x", "X"):
                done.append(task)
            elif state == "~":
                in_progress.append(task)
        elif stripped.startswith(("-", "*")) and stripped[1:].strip():
            # Plain list items → pending
            title = stripped.lstrip("-* ").strip()
            if title:
                pending.append({"title": title, "priority": "medium"})

    return {"pending": pending, "in_progress": in_progress, "done": done}


@app.get("/api/tasks")
async def get_tasks():
    text = safe_read(MEMORY_FILE)
    return parse_tasks_from_memory(text)


# ---------------------------------------------------------------------------
# POST /api/tasks
# ---------------------------------------------------------------------------

class NewTask(BaseModel):
    title: str
    priority: str = "medium"
    status: str = "pending"


@app.post("/api/tasks")
async def create_task(task: NewTask):
    text = safe_read(MEMORY_FILE)
    marker = "## Next Steps"
    checkbox = "- [ ]"
    new_line = f"{checkbox} [!{task.priority}] {task.title}\n"

    if marker in text:
        text = text.replace(marker, marker + "\n" + new_line, 1)
    else:
        text = text + f"\n\n{marker}\n{new_line}"

    MEMORY_FILE.write_text(text, encoding="utf-8")
    append_event("dashboard", "task_created", f"Task criada: {task.title}")
    return {"ok": True}


# ---------------------------------------------------------------------------
# GET /api/heartbeats
# ---------------------------------------------------------------------------

def parse_heartbeat_routines(text: str) -> list[dict]:
    routines = []
    current: dict | None = None

    for line in text.splitlines():
        stripped = line.strip()
        # Detect routine heading: ### or ## with time pattern
        h = re.match(r"^#{2,3}\s+(.+)", stripped)
        if h:
            title = h.group(1)
            time_m = re.search(r"(\d{1,2}[h:]\d{0,2}|\d{1,2}:\d{2}|\bdiário\b|\bsemanal\b|\bquinzenal\b)", title, re.IGNORECASE)
            if current:
                routines.append(current)
            current = {
                "name": title,
                "schedule": time_m.group(0) if time_m else "",
                "description": "",
                "last_run": None,
                "next_run": None,
                "status": "unknown",
            }
        elif current and stripped:
            current["description"] = (current["description"] + " " + stripped).strip()

    if current:
        routines.append(current)

    return routines


@app.get("/api/heartbeats")
async def get_heartbeats():
    text = safe_read(HEARTBEAT_FILE)
    routines = parse_heartbeat_routines(text)

    state: dict = {}
    if HEARTBEAT_STATE.exists():
        try:
            state = json.loads(HEARTBEAT_STATE.read_text(encoding="utf-8"))
        except Exception:
            pass

    for r in routines:
        key = r["name"]
        if key in state:
            r["last_run"] = state[key].get("last_run")
            r["next_run"] = state[key].get("next_run")
            r["status"] = state[key].get("status", "unknown")

    return {"routines": routines}


# ---------------------------------------------------------------------------
# GET /api/soul
# ---------------------------------------------------------------------------

def split_md_sections(text: str) -> list[dict]:
    sections = []
    current_title = "Intro"
    current_body: list[str] = []

    for line in text.splitlines():
        h = re.match(r"^(#{1,3})\s+(.+)", line)
        if h:
            if current_body:
                sections.append({"title": current_title, "body": "\n".join(current_body).strip()})
            current_title = h.group(2)
            current_body = []
        else:
            current_body.append(line)

    if current_body:
        sections.append({"title": current_title, "body": "\n".join(current_body).strip()})

    return sections


@app.get("/api/soul")
async def get_soul():
    soul_text = safe_read(SOUL_FILE)
    identity_text = safe_read(IDENTITY_FILE)
    agents_text = safe_read(AGENTS_FILE)

    return {
        "soul": {
            "raw": soul_text,
            "sections": split_md_sections(soul_text),
        },
        "identity": {
            "raw": identity_text,
            "sections": split_md_sections(identity_text),
        },
        "agents": {
            "raw": agents_text,
            "sections": split_md_sections(agents_text),
        },
    }


# ---------------------------------------------------------------------------
# POST /api/chat
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    agent: str
    message: str
    conversation_id: str = ""


@app.post("/api/chat")
async def post_chat(req: ChatRequest):
    # Sanitize agent name
    agent = re.sub(r"[^a-z0-9\-]", "", req.agent.lower())
    if not agent.startswith("pensare"):
        raise HTTPException(status_code=400, detail="Only pensare-* agents allowed")

    prompt = f"/{agent} {req.message}"
    ts = datetime.now(timezone.utc).isoformat()

    try:
        result = subprocess.run(
            ["claude", "--dangerously-skip-permissions", "--print", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(WORKSPACE_ROOT),
        )
        response = result.stdout.strip() if result.stdout else result.stderr.strip()
        if not response:
            response = "(sem resposta)"
    except subprocess.TimeoutExpired:
        response = "Timeout: o agente demorou mais de 120s para responder."
    except FileNotFoundError:
        response = "Erro: `claude` CLI não encontrado no PATH."
    except Exception as e:
        response = f"Erro ao invocar agente: {e}"

    append_event(agent, "chat", f"Mensagem enviada ao agente {agent}", {"message": req.message[:200]})

    return {"response": response, "agent": agent, "timestamp": ts}


# ---------------------------------------------------------------------------
# GET /api/heartbeat/status
# ---------------------------------------------------------------------------

@app.get("/api/heartbeat/status")
async def get_heartbeat_status():
    try:
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        running = "pensareos" in result.stdout.lower()
        pid = None
        if running:
            for line in result.stdout.splitlines():
                if "pensareos" in line.lower():
                    parts = line.split()
                    try:
                        pid = int(parts[0]) if parts[0] != "-" else None
                    except Exception:
                        pass
                    break
        return {"running": running, "pid": pid}
    except Exception:
        return {"running": False, "pid": None}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8360, reload=False)
