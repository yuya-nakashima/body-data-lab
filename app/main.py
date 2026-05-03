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
from app.core.db import ensure_db
from app.routers.aggregate import router as aggregate_router
from app.routers.focus import router as focus_router
from app.routers.ingest import router as ingest_router
from app.routers.metrics import router as metrics_router
from app.routers.normalize import router as normalize_router
from app.routers.quality import router as quality_router
from app.routers.raw import router as raw_router
from app.routers.reflections import router as reflections_router
from app.routers.ui import router as ui_router
from app.routers.wishes import router as wishes_router

app = FastAPI(title="Body Data Lab")


@app.on_event("startup")
def on_startup():
    ensure_db()


@app.get("/")
def root():
    return {"status": "ok", "db_path": DB_PATH}


app.include_router(focus_router)
app.include_router(ingest_router)
app.include_router(raw_router)
app.include_router(normalize_router)
app.include_router(aggregate_router)
app.include_router(quality_router)
app.include_router(metrics_router)
app.include_router(reflections_router)
app.include_router(wishes_router)
app.include_router(ui_router)
