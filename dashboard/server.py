"""
Pensare OS Dashboard — FastAPI Backend (Supabase-backed)
Run: python server.py
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Any

import openai
import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Supabase client
# ---------------------------------------------------------------------------

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://tplwqvvffanwsyhgufya.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwbHdxdnZmZmFud3N5aGd1ZnlhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3ODc4NzIwOSwiZXhwIjoyMDk0MzYzMjA5fQ.bGp-ym88m7Rku62FLoXP0gVpaW2v_6WxIGZiYyZq0JQ")

_sb = None

def get_sb():
    global _sb
    if _sb is None:
        from supabase import create_client
        _sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _sb

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

_default_workspace = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = Path(os.environ.get("PENSARE_WORKSPACE", str(_default_workspace)))
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
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = DASHBOARD_DIR / "static"
try:
    static_path.mkdir(exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
except (OSError, PermissionError):
    pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_read(path: Path, default: str = "") -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return default


def validate_path(rel_path: str) -> Path:
    target = (WORKSPACE_ROOT / rel_path).resolve()
    if not str(target).startswith(str(WORKSPACE_ROOT.resolve())):
        raise HTTPException(status_code=400, detail="Path traversal denied")
    return target


def append_event(agent: str, event_type: str, summary: str, payload: dict | None = None):
    ts = datetime.now(timezone.utc).isoformat()
    try:
        get_sb().table("events").insert({
            "ts": ts, "agent": agent, "type": event_type,
            "summary": summary, "payload": payload or {},
        }).execute()
    except Exception:
        pass
    # Also write local file as fallback
    try:
        EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        event = {"ts": ts, "agent": agent, "type": event_type, "summary": summary, "payload": payload or {}}
        with EVENTS_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass


def parse_frontmatter(text: str) -> dict:
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
    sb = get_sb()
    today = today_str()
    today_start = f"{today}T00:00:00+00:00"
    today_end = f"{today}T23:59:59+00:00"

    try:
        total_r = sb.table("events").select("id", count="exact").execute()
        total_eventos = total_r.count or 0
    except Exception:
        total_eventos = 0

    try:
        today_r = sb.table("events").select("agent,type", count="exact").gte("ts", today_start).lte("ts", today_end).execute()
        eventos_hoje = today_r.count or 0
        events_today = today_r.data or []
        erros_hoje = sum(1 for e in events_today if e.get("type") in ("error", "erro"))
        agentes_hoje = len({e.get("agent") for e in events_today if e.get("agent")})
    except Exception:
        eventos_hoje = 0
        erros_hoje = 0
        agentes_hoje = 0

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
        "eventos_hoje": eventos_hoje,
        "erros_hoje": erros_hoje,
        "agentes_hoje": agentes_hoje,
        "total_eventos": total_eventos,
    }


# ---------------------------------------------------------------------------
# GET /api/events
# ---------------------------------------------------------------------------

@app.get("/api/events")
async def get_events():
    try:
        r = get_sb().table("events").select("*").order("ts", desc=True).limit(50).execute()
        return {"events": r.data or []}
    except Exception:
        return {"events": []}


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

@app.get("/api/tasks")
async def get_tasks():
    sb = get_sb()
    try:
        r = sb.table("tasks").select("*").order("created_at", desc=True).limit(100).execute()
        rows = r.data or []
    except Exception:
        rows = []
    pending = [{"id": t["id"], "title": t["title"], "priority": t["priority"]} for t in rows if t["status"] == "pending"]
    in_progress = [{"id": t["id"], "title": t["title"], "priority": t["priority"]} for t in rows if t["status"] == "in_progress"]
    done = [{"id": t["id"], "title": t["title"], "priority": t["priority"]} for t in rows if t["status"] == "done"]
    return {"pending": pending, "in_progress": in_progress, "done": done}


# ---------------------------------------------------------------------------
# POST /api/tasks
# ---------------------------------------------------------------------------

class NewTask(BaseModel):
    title: str
    priority: str = "medium"
    status: str = "pending"


@app.post("/api/tasks")
async def create_task(task: NewTask):
    try:
        get_sb().table("tasks").insert({
            "title": task.title,
            "priority": task.priority,
            "status": task.status,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    append_event("dashboard", "task_created", f"Task criada: {task.title}")
    return {"ok": True}


class TaskUpdate(BaseModel):
    status: str


@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: int, req: TaskUpdate):
    try:
        get_sb().table("tasks").update({
            "status": req.status,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", task_id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
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

    # Load state from Supabase
    try:
        r = get_sb().table("heartbeat_state").select("*").execute()
        state = {row["name"]: row for row in (r.data or [])}
    except Exception:
        state = {}

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
# OpenAI API client + agent system prompt builder
# ---------------------------------------------------------------------------

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "codex-mini")


def build_agent_system_prompt(agent: str) -> str:
    """Build a system prompt for the given agent from SKILL.md + SOUL.md + IDENTITY.md."""
    parts: list[str] = []

    # 1. Soul + Identity (shared context for all agents)
    soul = safe_read(SOUL_FILE)
    identity = safe_read(IDENTITY_FILE)
    if soul:
        parts.append(soul)
    if identity:
        parts.append(identity)

    # 2. Agent-specific SKILL.md (strip YAML frontmatter, keep the prompt body)
    skill_file = SKILLS_DIR / agent / "SKILL.md"
    if skill_file.exists():
        text = safe_read(skill_file)
        # Strip frontmatter
        if text.startswith("---"):
            fm_parts = text.split("---", 2)
            body = fm_parts[2].strip() if len(fm_parts) >= 3 else text
        else:
            body = text
        parts.append(body)

    # 3. Business context
    empresa = safe_read(CONTEXTO_DIR / "empresa.md")
    mercado = safe_read(CONTEXTO_DIR / "mercado.md")
    if empresa:
        parts.append(f"## Contexto da Empresa\n\n{empresa}")
    if mercado:
        parts.append(f"## Contexto de Mercado\n\n{mercado}")

    # 4. Current memory state (abbreviated)
    memory = safe_read(MEMORY_FILE)
    if memory:
        # Keep only first 2000 chars to avoid bloating the prompt
        parts.append(f"## Estado Atual da Memória\n\n{memory[:2000]}")

    if not parts:
        return f"Você é o agente {agent} do Pensare OS. Responda em português."

    return "\n\n---\n\n".join(parts)


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

    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured. Set it as environment variable in Vercel.",
        )

    ts = datetime.now(timezone.utc).isoformat()
    system_prompt = build_agent_system_prompt(agent)

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            max_tokens=4096,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message},
            ],
        )
        choice = completion.choices[0] if completion.choices else None
        response = choice.message.content if choice and choice.message.content else "(sem resposta)"
    except openai.AuthenticationError:
        response = "Erro: OPENAI_API_KEY inválida."
    except openai.RateLimitError:
        response = "Erro: rate limit atingido na API. Tente novamente em alguns segundos."
    except Exception as e:
        response = f"Erro ao invocar agente: {e}"

    append_event(agent, "chat", f"Mensagem enviada ao agente {agent}", {"message": req.message[:200]})

    return {"response": response, "agent": agent, "timestamp": ts}


# ---------------------------------------------------------------------------
# GET /api/heartbeat/status
# ---------------------------------------------------------------------------

@app.get("/api/heartbeat/status")
async def get_heartbeat_status():
    """In serverless mode, heartbeat daemon is not available."""
    return {"running": False, "pid": None, "mode": "serverless"}


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8360, reload=False)
