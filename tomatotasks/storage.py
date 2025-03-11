from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


DATA_DIR = Path.home() / ".tomatotasks"
DB_FILE = DATA_DIR / "tasks.json"


@dataclass
class Task:
    id: str
    title: str
    created_at: str
    done: bool = False


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DB_FILE.exists():
        DB_FILE.write_text(json.dumps({"tasks": [], "session": None}, indent=2))


def read_db() -> dict:
    ensure_storage()
    return json.loads(DB_FILE.read_text() or "{}")


def write_db(data: dict) -> None:
    ensure_storage()
    DB_FILE.write_text(json.dumps(data, indent=2))


def add_task(title: str) -> Task:
    db = read_db()
    t = Task(id=str(int(datetime.utcnow().timestamp() * 1000)), title=title, created_at=_now_iso())
    db.setdefault("tasks", []).append(asdict(t))
    write_db(db)
    return t


def list_tasks() -> List[Task]:
    db = read_db()
    return [Task(**t) for t in db.get("tasks", [])]


def mark_done(task_id: str) -> bool:
    db = read_db()
    updated = False
    for t in db.get("tasks", []):
        if t["id"] == task_id:
            t["done"] = True
            updated = True
            break
    if updated:
        write_db(db)
    return updated


def start_session(minutes: int) -> None:
    db = read_db()
    db["session"] = {
        "started_at": _now_iso(),
        "minutes": minutes,
        "active": True,
    }
    write_db(db)


def stop_session() -> None:
    db = read_db()
    sess = db.get("session")
    if sess:
        sess["active"] = False
        sess["stopped_at"] = _now_iso()
        write_db(db)


def current_session() -> Optional[dict]:
    return read_db().get("session")

