from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta, timezone

from app.core.db import ensure_db, get_conn
from app.core.timeutil import parse_iso8601, utc_iso_to_jst_day

DEFAULT_OTHER_PRIORITY = 3


def _load_source_priority(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        """
        SELECT source_type, priority
        FROM source_priority
        """
    ).fetchall()
    return {row["source_type"]: row["priority"] for row in rows}


def _priority_for(source_type: str | None, priority_map: dict[str, int]) -> int:
    source_key = (source_type or "other").lower()
    return priority_map.get(source_key, DEFAULT_OTHER_PRIORITY)


def _build_steps_candidate(
    row: sqlite3.Row, metric: str, priority_map: dict[str, int]
) -> dict | None:
    ts_start_raw = row["ts_start"]
    if not ts_start_raw:
        return None

    try:
        day = utc_iso_to_jst_day(ts_start_raw)
    except ValueError:
        return None

    unit = row["unit"]
    if unit and unit != "count":
        return None

    source = row["source"] or "unknown"
    source_type = (row["source_type"] or "other").lower()
    created_at_dt = parse_iso8601(row["created_at"])
    if created_at_dt is None:
        created_at_dt = datetime.min.replace(tzinfo=timezone.utc)

    compare_dt = parse_iso8601(row["ts_end"] or row["ts_start"])
    if compare_dt is None:
        compare_dt = created_at_dt

    return {
        "measurement_id": row["id"],
        "day": day,
        "source": source,
        "source_type": source_type,
        "metric": metric,
        "value": row["value"],
        "unit": unit,
        "created_at_dt": created_at_dt,
        "priority": _priority_for(source_type, priority_map),
        "derived_ts_end": compare_dt.astimezone(timezone.utc).isoformat(),
    }


def _is_steps_candidate_better(candidate: dict, current: dict | None) -> bool:
    if current is None:
        return True
    if candidate["priority"] != current["priority"]:
        return candidate["priority"] < current["priority"]
    if candidate["created_at_dt"] != current["created_at_dt"]:
        return candidate["created_at_dt"] > current["created_at_dt"]
    return candidate["measurement_id"] > current["measurement_id"]


def _select_best_existing_steps_daily(
    conn: sqlite3.Connection,
    day: str,
    metric: str,
    source: str | None,
    priority_map: dict[str, int],
) -> dict | None:
    sql = [
        """
        SELECT
            d.source AS daily_source,
            d.value AS daily_value,
            d.unit AS daily_unit,
            d.updated_at AS daily_updated_at,
            d.derived_from_measurement_id,
            m.id AS measurement_id,
            m.source AS measurement_source,
            COALESCE(m.source_type, 'other') AS measurement_source_type,
            m.created_at AS measurement_created_at
        FROM daily_metrics d
        LEFT JOIN measurements m
          ON m.id = d.derived_from_measurement_id
        WHERE d.day = ? AND d.metric = ?
        """
    ]
    params: list = [day, metric]
    if source is not None:
        sql.append("AND d.source = ?")
        params.append(source)

    rows = conn.execute(" ".join(sql), tuple(params)).fetchall()
    best: dict | None = None
    for row in rows:
        source_name = row["measurement_source"] or row["daily_source"] or "unknown"
        source_type = (row["measurement_source_type"] or "other").lower()
        created_at_dt = parse_iso8601(row["measurement_created_at"])
        if created_at_dt is None:
            created_at_dt = parse_iso8601(row["daily_updated_at"])
        if created_at_dt is None:
            created_at_dt = datetime.min.replace(tzinfo=timezone.utc)
        measurement_id = row["measurement_id"] or row["derived_from_measurement_id"] or 0
        candidate = {
            "measurement_id": measurement_id,
            "day": day,
            "source": source_name,
            "source_type": source_type,
            "metric": metric,
            "value": row["daily_value"],
            "unit": row["daily_unit"],
            "created_at_dt": created_at_dt,
            "priority": _priority_for(source_type, priority_map),
        }
        if _is_steps_candidate_better(candidate, best):
            best = candidate
    return best


def _fetch_measurements_for_aggregation(
    conn: sqlite3.Connection,
    metric: str,
    source: str | None,
    since_measurement_id: int,
    limit: int,
) -> list[sqlite3.Row]:
    if source:
        return conn.execute(
            """
            SELECT id, source, source_type, metric, ts_start, ts_end, value, unit, created_at
            FROM measurements
            WHERE id > ? AND metric = ? AND source = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (since_measurement_id, metric, source, limit),
        ).fetchall()

    return conn.execute(
        """
        SELECT id, source, source_type, metric, ts_start, ts_end, value, unit, created_at
        FROM measurements
        WHERE id > ? AND metric = ?
        ORDER BY id ASC
        LIMIT ?
        """,
        (since_measurement_id, metric, limit),
    ).fetchall()


def _collect_daily_candidates(
    rows: list[sqlite3.Row],
    metric: str,
    source: str | None,
    priority_map: dict[str, int],
) -> dict:
    selected_by_day: dict = {}

    for row in rows:
        if metric == "steps_total":
            candidate = _build_steps_candidate(row, metric, priority_map)
            if candidate is None:
                continue
            if source is None:
                key = (candidate["day"], metric)
            else:
                key = (candidate["day"], source, metric)
            current = selected_by_day.get(key)
            if _is_steps_candidate_better(candidate, current):
                selected_by_day[key] = candidate
            continue

        row_source = row["source"] or "unknown"
        ts_start_raw = row["ts_start"]
        if not ts_start_raw:
            continue

        try:
            day = utc_iso_to_jst_day(ts_start_raw)
        except ValueError:
            continue

        compare_ts_raw = row["ts_end"] or row["ts_start"]
        compare_dt = parse_iso8601(compare_ts_raw)
        if compare_dt is None:
            continue

        key = (day, row_source, metric)
        current = selected_by_day.get(key)
        if current is None or compare_dt > current["compare_dt"]:
            selected_by_day[key] = {
                "measurement_id": row["id"],
                "day": day,
                "source": row_source,
                "metric": metric,
                "value": row["value"],
                "unit": row["unit"],
                "derived_ts_end": compare_dt.astimezone(timezone.utc).isoformat(),
                "compare_dt": compare_dt,
            }

    return selected_by_day


def _upsert_daily_candidates(
    conn: sqlite3.Connection,
    selected_by_day: dict,
    metric: str,
    source: str | None,
    priority_map: dict[str, int],
) -> int:
    upserted_count = 0
    now_utc = datetime.now(timezone.utc).isoformat()

    for item in selected_by_day.values():
        if metric == "steps_total":
            existing_best = _select_best_existing_steps_daily(
                conn=conn,
                day=item["day"],
                metric=metric,
                source=source,
                priority_map=priority_map,
            )
            if not _is_steps_candidate_better(item, existing_best):
                continue

            daily_source = source or item["source"]
            if source is None:
                conn.execute(
                    """
                    DELETE FROM daily_metrics
                    WHERE day = ? AND metric = ?
                    """,
                    (item["day"], metric),
                )

            conn.execute(
                """
                INSERT INTO daily_metrics
                    (day, source, metric, value, unit, derived_from_measurement_id, derived_ts_end, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(day, source, metric) DO UPDATE SET
                    value = excluded.value,
                    unit = excluded.unit,
                    derived_from_measurement_id = excluded.derived_from_measurement_id,
                    derived_ts_end = excluded.derived_ts_end,
                    updated_at = excluded.updated_at
                """,
                (
                    item["day"],
                    daily_source,
                    metric,
                    item["value"],
                    item["unit"],
                    item["measurement_id"],
                    item["derived_ts_end"],
                    now_utc,
                ),
            )
            upserted_count += 1
            continue

        existing = conn.execute(
            """
            SELECT derived_ts_end
            FROM daily_metrics
            WHERE day = ? AND source = ? AND metric = ?
            """,
            (item["day"], item["source"], item["metric"]),
        ).fetchone()

        should_upsert = True
        if existing and existing["derived_ts_end"]:
            existing_dt = parse_iso8601(existing["derived_ts_end"])
            if existing_dt is not None and existing_dt >= item["compare_dt"]:
                should_upsert = False

        if not should_upsert:
            continue

        conn.execute(
            """
            INSERT INTO daily_metrics
                (day, source, metric, value, unit, derived_from_measurement_id, derived_ts_end, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(day, source, metric) DO UPDATE SET
                value = excluded.value,
                unit = excluded.unit,
                derived_from_measurement_id = excluded.derived_from_measurement_id,
                derived_ts_end = excluded.derived_ts_end,
                updated_at = excluded.updated_at
            """,
            (
                item["day"],
                item["source"],
                item["metric"],
                item["value"],
                item["unit"],
                item["measurement_id"],
                item["derived_ts_end"],
                now_utc,
            ),
        )
        upserted_count += 1

    return upserted_count


def _deduplicate_measurements_by_metric(conn: sqlite3.Connection, metric: str) -> int:
    return conn.execute(
        """
        DELETE FROM measurements
        WHERE metric = ?
          AND id NOT IN (
              SELECT MAX(id)
              FROM measurements
              WHERE metric = ?
              GROUP BY
                  COALESCE(source_type, 'other'),
                  source,
                  metric,
                  ts_start,
                  ts_end
          )
        """,
        (metric, metric),
    ).rowcount


def _ensure_measurement_range_index(conn: sqlite3.Connection) -> None:
    try:
        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS uq_measurements_source_range
            ON measurements(source_type, source, metric, ts_start, ts_end);
            """
        )
    except sqlite3.IntegrityError:
        pass


def aggregate_daily_metrics(
    metric: str = "steps_total",
    source: str | None = None,
    limit: int = 500,
    since_measurement_id: int = 0,
) -> dict:
    ensure_db()

    conn = get_conn()
    rows = _fetch_measurements_for_aggregation(
        conn=conn,
        metric=metric,
        source=source,
        since_measurement_id=since_measurement_id,
        limit=limit,
    )
    target_count = len(rows)
    last_measurement_id = rows[-1]["id"] if rows else since_measurement_id
    priority_map = _load_source_priority(conn)
    selected_by_day = _collect_daily_candidates(rows, metric, source, priority_map)
    day_groups = len(selected_by_day)
    upserted_count = _upsert_daily_candidates(
        conn=conn,
        selected_by_day=selected_by_day,
        metric=metric,
        source=source,
        priority_map=priority_map,
    )
    conn.commit()
    conn.close()

    return {
        "ok": True,
        "metric": metric,
        "source": source,
        "target_count": target_count,
        "day_groups": day_groups,
        "upserted_count": upserted_count,
        "skipped_count": target_count - upserted_count,
        "last_measurement_id": last_measurement_id,
    }


def deduplicate_steps_total_measurements_job() -> dict:
    ensure_db()

    metric = "steps_total"
    conn = get_conn()
    deleted_count = _deduplicate_measurements_by_metric(conn, metric)
    kept_count = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM measurements
        WHERE metric = ?
        """,
        (metric,),
    ).fetchone()["c"]
    _ensure_measurement_range_index(conn)
    conn.commit()
    conn.close()

    return {
        "ok": True,
        "metric": metric,
        "deleted_count": deleted_count,
        "kept_count": kept_count,
    }


def rebuild_steps_total_daily_metrics(limit: int = 5000) -> dict:
    ensure_db()

    metric = "steps_total"
    conn = get_conn()
    priority_map = _load_source_priority(conn)

    _deduplicate_measurements_by_metric(conn, metric)
    _ensure_measurement_range_index(conn)

    deleted_count = conn.execute(
        """
        DELETE FROM daily_metrics
        WHERE metric = ?
        """,
        (metric,),
    ).rowcount

    since_measurement_id = 0
    candidate_count = 0
    selected_by_day: dict[str, dict] = {}

    while True:
        rows = conn.execute(
            """
            SELECT id, source, source_type, ts_start, ts_end, value, unit, created_at
            FROM measurements
            WHERE id > ? AND metric = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (since_measurement_id, metric, limit),
        ).fetchall()
        if not rows:
            break

        candidate_count += len(rows)
        since_measurement_id = rows[-1]["id"]
        for row in rows:
            candidate = _build_steps_candidate(row, metric, priority_map)
            if candidate is None:
                continue
            day = candidate["day"]
            current = selected_by_day.get(day)
            if _is_steps_candidate_better(candidate, current):
                selected_by_day[day] = candidate

        if len(rows) < limit:
            break

    day_groups = len(selected_by_day)
    upserted_count = 0
    now_utc = datetime.now(timezone.utc).isoformat()
    for item in selected_by_day.values():
        conn.execute(
            """
            INSERT INTO daily_metrics
                (day, source, metric, value, unit, derived_from_measurement_id, derived_ts_end, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(day, source, metric) DO UPDATE SET
                value = excluded.value,
                unit = excluded.unit,
                derived_from_measurement_id = excluded.derived_from_measurement_id,
                derived_ts_end = excluded.derived_ts_end,
                updated_at = excluded.updated_at
            """,
            (
                item["day"],
                item["source"],
                metric,
                item["value"],
                item["unit"],
                item["measurement_id"],
                item["derived_ts_end"],
                now_utc,
            ),
        )
        upserted_count += 1

    conn.commit()
    conn.close()

    return {
        "ok": True,
        "metric": metric,
        "deleted_count": deleted_count,
        "candidate_count": candidate_count,
        "day_groups": day_groups,
        "upserted_count": upserted_count,
    }


def get_daily_summary(
    target_day: str | None = None,
    metric: str = "steps_total",
) -> dict:
    """
    target_day の集計値・前日差分・週平均差を返す。
    target_day が None の場合は前日（今日 - 1日）を使う。
    週平均は target_day を含む過去 7 日分が全て揃っている場合のみ計算する。
    """
    ensure_db()

    if target_day is None:
        target_day = (date.today() - timedelta(days=1)).isoformat()

    target_dt = date.fromisoformat(target_day)
    prev_day = (target_dt - timedelta(days=1)).isoformat()
    days_7 = [(target_dt - timedelta(days=i)).isoformat() for i in range(7)]

    conn = get_conn()

    def fetch_value(day: str) -> float | None:
        row = conn.execute(
            """
            SELECT value FROM daily_metrics
            WHERE day = ? AND metric = ?
            ORDER BY updated_at DESC LIMIT 1
            """,
            (day, metric),
        ).fetchone()
        return row["value"] if row else None

    current_value = fetch_value(target_day)
    prev_value = fetch_value(prev_day)

    week_values = [fetch_value(d) for d in days_7]
    conn.close()

    if all(v is not None for v in week_values):
        week_avg: float | None = sum(week_values) / 7  # type: ignore[arg-type]
    else:
        week_avg = None

    day_diff = (
        current_value - prev_value
        if current_value is not None and prev_value is not None
        else None
    )
    week_diff = (
        current_value - week_avg
        if current_value is not None and week_avg is not None
        else None
    )

    return {
        "target_day": target_day,
        "metric": metric,
        "current_value": current_value,
        "prev_day": prev_day,
        "prev_value": prev_value,
        "day_diff": day_diff,
        "week_avg": week_avg,
        "week_diff": week_diff,
    }


def list_daily_metrics(
    day: str | None = None, metric: str | None = None, limit: int = 50
) -> dict:
    ensure_db()

    sql = [
        """
        SELECT
            day,
            source,
            metric,
            value,
            unit,
            derived_from_measurement_id,
            derived_ts_end,
            updated_at
        FROM daily_metrics
        WHERE 1 = 1
        """
    ]
    params: list = []
    if day:
        sql.append("AND day = ?")
        params.append(day)
    if metric:
        sql.append("AND metric = ?")
        params.append(metric)
    sql.append("ORDER BY updated_at DESC LIMIT ?")
    params.append(limit)

    conn = get_conn()
    rows = conn.execute(" ".join(sql), tuple(params)).fetchall()
    conn.close()
    return {"items": [dict(row) for row in rows]}
