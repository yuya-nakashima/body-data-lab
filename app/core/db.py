import hashlib
import json
import sqlite3
from pathlib import Path

from app.core.config import DB_PATH


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row["name"] for row in rows}


def _ensure_measurements_columns(conn: sqlite3.Connection) -> None:
    columns = _table_columns(conn, "measurements")

    if "source_type" not in columns:
        conn.execute("ALTER TABLE measurements ADD COLUMN source_type TEXT;")
    if "source_detail" not in columns:
        conn.execute("ALTER TABLE measurements ADD COLUMN source_detail TEXT;")

    conn.execute("UPDATE measurements SET source_type = 'other' WHERE source_type IS NULL;")


def _seed_source_priority(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS source_priority (
            source_type TEXT PRIMARY KEY,
            priority INTEGER NOT NULL
        );
        """
    )
    conn.executemany(
        """
        INSERT INTO source_priority (source_type, priority)
        VALUES (?, ?)
        ON CONFLICT(source_type) DO UPDATE SET
            priority = excluded.priority
        """,
        [
            ("watch", 1),
            ("phone", 2),
            ("other", 3),
        ],
    )


def ensure_db() -> None:
    db_path = Path(DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS raw_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            received_at TEXT NOT NULL,
            source TEXT,
            metric TEXT,
            payload_json TEXT NOT NULL,
            hash TEXT NOT NULL UNIQUE
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_event_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            source_type TEXT,
            source_detail TEXT,
            metric TEXT NOT NULL,
            ts_start TEXT,
            ts_end TEXT,
            value REAL,
            unit TEXT,
            quality_flag INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE(raw_event_id, metric, ts_start, ts_end)
        );
        """
    )
    _ensure_measurements_columns(conn)

    _seed_source_priority(conn)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            source TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL,
            unit TEXT,
            derived_from_measurement_id INTEGER,
            derived_ts_end TEXT,
            updated_at TEXT NOT NULL,
            UNIQUE(day, source, metric)
        );
        """
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_raw_events_received_at ON raw_events(received_at);"
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_raw_events_source ON raw_events(source);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_raw_events_metric ON raw_events(metric);")

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_measurements_ts_start ON measurements(ts_start);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_measurements_metric ON measurements(metric);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_measurements_source ON measurements(source);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_measurements_raw_event_id ON measurements(raw_event_id);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_measurements_source_type ON measurements(source_type);"
    )
    try:
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS uq_measurements_source_range
            ON measurements(source_type, source, metric, ts_start, ts_end);
            """
        )
    except sqlite3.IntegrityError:
        # Legacy duplicate rows can be cleaned by /measurements/deduplicate-steps-total.
        pass
    conn.execute("CREATE INDEX IF NOT EXISTS idx_daily_metrics_day ON daily_metrics(day);")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_daily_metrics_metric ON daily_metrics(metric);"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_daily_metrics_source ON daily_metrics(source);"
    )

    conn.commit()
    conn.close()


def stable_hash(payload: dict) -> str:
    normalized = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()
