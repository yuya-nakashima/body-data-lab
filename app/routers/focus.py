from datetime import datetime, timezone

from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.db import get_conn

router = APIRouter(prefix="/focus", tags=["focus"])


class FocusSessionIn(BaseModel):
    start_at: str  # ISO 8601
    end_at: str    # ISO 8601


@router.post("/sessions")
def create_session(body: FocusSessionIn):
    try:
        start = datetime.fromisoformat(body.start_at)
        end = datetime.fromisoformat(body.end_at)
    except ValueError as e:
        return JSONResponse(status_code=422, content={"ok": False, "error": str(e)})

    if end <= start:
        return JSONResponse(
            status_code=422,
            content={"ok": False, "error": "end_at must be after start_at"},
        )

    duration_seconds = int((end - start).total_seconds())
    created_at = datetime.now(timezone.utc).isoformat()

    conn = get_conn()
    cur = conn.execute(
        """
        INSERT INTO focus_sessions (start_at, end_at, duration_seconds, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (body.start_at, body.end_at, duration_seconds, created_at),
    )
    conn.commit()
    session_id = cur.lastrowid
    conn.close()

    return {"ok": True, "id": session_id, "duration_seconds": duration_seconds}


@router.get("/sessions")
def list_sessions(date: str = Query(..., description="YYYY-MM-DD")):
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT id, start_at, end_at, duration_seconds
        FROM focus_sessions
        WHERE date(start_at) = ?
        ORDER BY start_at
        """,
        (date,),
    ).fetchall()
    conn.close()

    return {"ok": True, "date": date, "sessions": [dict(r) for r in rows]}


@router.get("/daily")
def daily_summary(date: str = Query(..., description="YYYY-MM-DD")):
    conn = get_conn()

    def fetch_day(day: str):
        rows = conn.execute(
            """
            SELECT duration_seconds
            FROM focus_sessions
            WHERE date(start_at) = ?
            """,
            (day,),
        ).fetchall()
        return [r["duration_seconds"] for r in rows]

    today_durations = fetch_day(date)

    # 7日分（対象日を含む直近7日）
    week_rows = conn.execute(
        """
        SELECT date(start_at) AS day, SUM(duration_seconds) AS total
        FROM focus_sessions
        WHERE date(start_at) <= ?
          AND date(start_at) > date(?, '-7 days')
        GROUP BY day
        ORDER BY day DESC
        """,
        (date, date),
    ).fetchall()
    conn.close()

    if not today_durations:
        total_today = None
        max_today = None
    else:
        total_today = sum(today_durations)
        max_today = max(today_durations)

    # 前日
    yesterday_row = next(
        (r for r in week_rows if r["day"] < date),
        None,
    )
    total_yesterday = yesterday_row["total"] if yesterday_row else None

    # 7日平均（対象日を除く）
    past_totals = [r["total"] for r in week_rows if r["day"] < date]
    avg_7d = int(sum(past_totals) / len(past_totals)) if past_totals else None

    def diff(a, b):
        if a is None or b is None:
            return None
        return a - b

    return {
        "ok": True,
        "date": date,
        "total_seconds": total_today,
        "max_seconds": max_today,
        "diff_from_yesterday_seconds": diff(total_today, total_yesterday),
        "diff_from_7d_avg_seconds": diff(total_today, avg_7d),
        "session_count": len(today_durations),
    }
