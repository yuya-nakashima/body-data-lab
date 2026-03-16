import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.db import ensure_db, get_conn

router = APIRouter(tags=["raw"])


@router.get("/raw")
def list_raw(limit: int = 20):
    ensure_db()
    limit = max(1, min(limit, 200))

    conn = get_conn()
    rows = conn.execute(
        """
        SELECT id, received_at, source, metric, hash
        FROM raw_events
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()

    return {"items": [dict(row) for row in rows]}


@router.get("/raw/{event_id}")
def get_raw(event_id: int):
    ensure_db()

    conn = get_conn()
    row = conn.execute(
        """
        SELECT id, received_at, source, metric, hash, payload_json
        FROM raw_events
        WHERE id = ?
        """,
        (event_id,),
    ).fetchone()
    conn.close()

    if not row:
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})

    data = dict(row)
    data["payload"] = json.loads(data.pop("payload_json"))
    return data
