from __future__ import annotations

import os
from pathlib import Path


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI

from app.core.config import DB_PATH
from app.core.db import run_migrations
from app.routers.focus import router as focus_router
from app.routers.daily_goals import router as daily_goals_router
from app.routers.habit_groups import router as habit_groups_router
from app.routers.reflections import router as reflections_router
from app.routers.ui import router as ui_router
from app.routers.wishes import router as wishes_router

app = FastAPI(title="Body Data Lab")


@app.on_event("startup")
def on_startup():
    run_migrations()


@app.get("/")
def root():
    return {"status": "ok", "db_path": DB_PATH}


app.include_router(focus_router)
app.include_router(daily_goals_router)
app.include_router(habit_groups_router)
app.include_router(reflections_router)
app.include_router(wishes_router)
app.include_router(ui_router)
