import json
import sqlite3
from datetime import datetime, timezone

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from app.core.db import ensure_db, get_conn, stable_hash
from app.services.aggregate_service import aggregate_daily_metrics
from app.services.normalize_service import normalize_steps

router = APIRouter(tags=["ingest"])


@router.post("/ingest")
def ingest(payload: dict = Body(...)):
    ensure_db()

    payload_hash = stable_hash(payload)
    received_at = datetime.now(timezone.utc).isoformat()
    source = payload.get("source")
    metric = payload.get("metric")
    payload_json = json.dumps(payload, ensure_ascii=False)

    conn = get_conn()
    try:
        cur = conn.execute(
            """
            INSERT INTO raw_events (received_at, source, metric, payload_json, hash)
            VALUES (?, ?, ?, ?, ?)
            """,
            (received_at, source, metric, payload_json, payload_hash),
        )
        conn.commit()
        raw_id = cur.lastrowid
    except sqlite3.IntegrityError:
        row = conn.execute(
            "SELECT id FROM raw_events WHERE hash = ?", (payload_hash,)
        ).fetchone()
        return JSONResponse(
            status_code=200,
            content={
                "ok": True,
                "inserted": False,
                "id": row["id"] if row else None,
                "hash": payload_hash,
            },
        )
    finally:
        conn.close()

    normalize_result = normalize_steps(since_id=raw_id - 1)
    aggregate_result = aggregate_daily_metrics()

    return {
        "ok": True,
        "inserted": True,
        "id": raw_id,
        "hash": payload_hash,
        "normalize": normalize_result,
        "aggregate": aggregate_result,
    }
