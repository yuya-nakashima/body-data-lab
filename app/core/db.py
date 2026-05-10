import hashlib
import json
import sqlite3
from pathlib import Path

from app.core.config import DB_PATH

MIGRATIONS_DIR = Path(__file__).parent.parent.parent / "migrations"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_migrations() -> None:
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = get_conn()
    for f in sorted(MIGRATIONS_DIR.glob("*.sql")):
        conn.executescript(f.read_text(encoding="utf-8"))
    conn.close()


def stable_hash(payload: dict) -> str:
    normalized = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
