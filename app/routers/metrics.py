from fastapi import APIRouter, Query

from app.core.db import get_conn

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/daily")
def get_daily_metrics(
    metric: str = Query(...),
    source: str = Query(...),
    days: int = Query(90, ge=1, le=3650),
):
    conn = get_conn()

    rows = conn.execute(
        """
        SELECT day, value, unit
        FROM daily_metrics
        WHERE metric = ?
          AND source = ?
        ORDER BY day DESC
        LIMIT ?
        """,
        (metric, source, days),
    ).fetchall()

    rows = [dict(r) for r in rows]
    rows.reverse()

    start_day = rows[0]["day"] if rows else None
    end_day = rows[-1]["day"] if rows else None

    conn.close()

    return {
        "ok": True,
        "metric": metric,
        "source": source,
        "start_day": start_day,
        "end_day": end_day,
        "rows": rows,
    }
