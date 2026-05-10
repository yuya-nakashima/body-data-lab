import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.core.config import DB_PATH
from app.core.timeutil import JST

MIGRATIONS_DIR = Path(__file__).parent.parent.parent / "migrations"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def run_migrations() -> None:
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version    TEXT PRIMARY KEY,
            applied_at TEXT NOT NULL
        )
        """
    )

    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    applied = {row["version"] for row in conn.execute("SELECT version FROM schema_migrations")}

    # Bootstrap: existing DB predates the migration system — mark all as applied
    if not applied:
        is_existing = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='raw_events'"
        ).fetchone()
        if is_existing:
            now = datetime.now(JST).isoformat()
            for f in migration_files:
                conn.execute(
                    "INSERT OR IGNORE INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                    (f.stem, now),
                )
            conn.commit()
            conn.close()
            return

    now = datetime.now(JST).isoformat()
    for f in migration_files:
        if f.stem not in applied:
            conn.executescript(f.read_text(encoding="utf-8"))
            conn.execute(
                "INSERT INTO schema_migrations (version, applied_at) VALUES (?, ?)",
                (f.stem, now),
            )
            conn.commit()

    conn.close()


def stable_hash(payload: dict) -> str:
    normalized = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
