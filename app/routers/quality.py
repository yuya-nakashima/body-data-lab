import json
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException

from app.core.db import ensure_db, get_conn

router = APIRouter(tags=["quality"])


def _parse_iso8601(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


def _percentile(sorted_values: list[float], p: float) -> float | None:
    if not sorted_values:
        return None
    if len(sorted_values) == 1:
        return sorted_values[0]

    pos = (len(sorted_values) - 1) * p
    low = int(pos)
    high = min(low + 1, len(sorted_values) - 1)
    weight = pos - low
    return sorted_values[low] + (sorted_values[high] - sorted_values[low]) * weight


def _to_raw_metric(metric: str) -> str:
    if metric == "steps_total":
        return "steps"
    return metric


def _parse_day(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"invalid {field_name}: {value}") from exc


@router.get("/quality")
def get_quality(
    metric: str = "steps_total",
    source: str = "health_connect",
    days: int = 30,
    limit: int = 2000,
):
    ensure_db()
    days = max(1, min(days, 3650))
    limit = max(1, min(limit, 20000))

    conn = get_conn()

    counts = {
        "raw_events": conn.execute("SELECT COUNT(*) AS c FROM raw_events").fetchone()["c"],
        "measurements": conn.execute("SELECT COUNT(*) AS c FROM measurements").fetchone()["c"],
        "daily_metrics": conn.execute("SELECT COUNT(*) AS c FROM daily_metrics").fetchone()["c"],
    }

    coverage_row = conn.execute(
        """
        SELECT
            MIN(day) AS daily_min_day,
            MAX(day) AS daily_max_day,
            COUNT(*) AS daily_days
        FROM daily_metrics
        WHERE metric = ? AND source = ?
        """,
        (metric, source),
    ).fetchone()
    coverage = {
        "daily_min_day": coverage_row["daily_min_day"],
        "daily_max_day": coverage_row["daily_max_day"],
        "daily_days": coverage_row["daily_days"],
    }

    dup_row = conn.execute(
        """
        SELECT COALESCE(SUM(cnt - 1), 0) AS dup
        FROM (
            SELECT hash, COUNT(*) AS cnt
            FROM raw_events
            GROUP BY hash
            HAVING cnt > 1
        )
        """
    ).fetchone()
    raw_hash_duplicate_count = dup_row["dup"] or 0

    raw_metric = _to_raw_metric(metric)
    norm_row = conn.execute(
        """
        SELECT
            COUNT(*) AS target_raw,
            COALESCE(SUM(CASE WHEN m.raw_event_id IS NOT NULL THEN 1 ELSE 0 END), 0) AS normalized_raw
        FROM raw_events r
        LEFT JOIN (
            SELECT DISTINCT raw_event_id
            FROM measurements
            WHERE metric = ?
        ) m ON m.raw_event_id = r.id
        WHERE COALESCE(r.source, '') = ? AND COALESCE(r.metric, '') = ?
        """,
        (metric, source, raw_metric),
    ).fetchone()

    target_raw = norm_row["target_raw"] or 0
    normalized_raw = norm_row["normalized_raw"] or 0
    normalize_skipped_estimate = max(target_raw - normalized_raw, 0)

    latency_rows = conn.execute(
        """
        SELECT id, received_at, payload_json
        FROM raw_events
        WHERE COALESCE(source, '') = ? AND COALESCE(metric, '') = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (source, raw_metric, limit),
    ).fetchall()

    latency_values: list[float] = []
    latency_parse_error_count = 0
    latency_missing_end_count = 0

    for row in latency_rows:
        try:
            payload = json.loads(row["payload_json"])
        except Exception:
            latency_parse_error_count += 1
            continue

        end_ts = payload.get("end_at") or payload.get("ts")
        if not end_ts:
            latency_missing_end_count += 1
            continue

        received_dt = _parse_iso8601(row["received_at"])
        payload_end_dt = _parse_iso8601(end_ts)
        if received_dt is None or payload_end_dt is None:
            latency_parse_error_count += 1
            continue

        latency_values.append((received_dt - payload_end_dt).total_seconds())

    latency_values.sort()
    latency_stats = {
        "samples": len(latency_values),
        "p50": _percentile(latency_values, 0.5),
        "p90": _percentile(latency_values, 0.9),
        "max": max(latency_values) if latency_values else None,
        "parse_error_count": latency_parse_error_count,
        "missing_end_count": latency_missing_end_count,
    }

    daily_rows = conn.execute(
        """
        SELECT day, value, unit
        FROM daily_metrics
        WHERE metric = ? AND source = ?
        ORDER BY day DESC
        LIMIT ?
        """,
        (metric, source, days),
    ).fetchall()

    conn.close()

    return {
        "ok": True,
        "counts": counts,
        "coverage": coverage,
        "duplicates": {
            "raw_hash_duplicate_count": raw_hash_duplicate_count,
            "normalize_skipped_estimate": normalize_skipped_estimate,
            "target_raw": target_raw,
            "normalized_raw": normalized_raw,
        },
        "latency_seconds": latency_stats,
        "recent_daily": [dict(row) for row in daily_rows],
    }


@router.get("/quality/gaps")
def get_quality_gaps(
    metric: str = "steps_total",
    source: str = "health_connect",
    start_day: str | None = None,
    end_day: str | None = None,
    max_span_days: int = 3660,
):
    ensure_db()
    max_span_days = max(1, min(max_span_days, 36500))

    conn = get_conn()
    bounds_row = conn.execute(
        """
        SELECT MIN(day) AS min_day, MAX(day) AS max_day
        FROM daily_metrics
        WHERE metric = ? AND source = ?
        """,
        (metric, source),
    ).fetchone()

    min_day = start_day or bounds_row["min_day"]
    max_day = end_day or bounds_row["max_day"]

    if not min_day or not max_day:
        conn.close()
        return {
            "ok": True,
            "metric": metric,
            "source": source,
            "start_day": None,
            "end_day": None,
            "expected_days": 0,
            "observed_days": 0,
            "gap_count": 0,
            "gaps": [],
        }

    start_date = _parse_day(min_day, "start_day")
    end_date = _parse_day(max_day, "end_day")
    if start_date > end_date:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="start_day must be less than or equal to end_day",
        )

    span_days = (end_date - start_date).days + 1
    if span_days > max_span_days:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"date span too large: {span_days} > {max_span_days}",
        )

    rows = conn.execute(
        """
        SELECT day
        FROM daily_metrics
        WHERE metric = ? AND source = ? AND day BETWEEN ? AND ?
        ORDER BY day ASC
        """,
        (metric, source, start_date.isoformat(), end_date.isoformat()),
    ).fetchall()
    conn.close()

    observed_days = {row["day"] for row in rows}
    gaps: list[str] = []
    cursor = start_date
    while cursor <= end_date:
        day_str = cursor.isoformat()
        if day_str not in observed_days:
            gaps.append(day_str)
        cursor += timedelta(days=1)

    return {
        "ok": True,
        "metric": metric,
        "source": source,
        "start_day": start_date.isoformat(),
        "end_day": end_date.isoformat(),
        "expected_days": span_days,
        "observed_days": len(observed_days),
        "gap_count": len(gaps),
        "gaps": gaps,
    }
