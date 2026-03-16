from fastapi import FastAPI

from app.core.config import DB_PATH
from app.core.db import ensure_db
from app.routers.aggregate import router as aggregate_router
from app.routers.ingest import router as ingest_router
from app.routers.metrics import router as metrics_router
from app.routers.normalize import router as normalize_router
from app.routers.quality import router as quality_router
from app.routers.raw import router as raw_router
from app.routers.ui import router as ui_router

app = FastAPI(title="Body Data Lab")


@app.on_event("startup")
def on_startup():
    ensure_db()


@app.get("/")
def root():
    return {"status": "ok", "db_path": DB_PATH}


app.include_router(ingest_router)
app.include_router(raw_router)
app.include_router(normalize_router)
app.include_router(aggregate_router)
app.include_router(quality_router)
app.include_router(metrics_router)
app.include_router(ui_router)
