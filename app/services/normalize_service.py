from __future__ import annotations

import json
from datetime import datetime, timezone

from app.core.db import ensure_db, get_conn


def _as_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _as_text(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        text = str(value).strip()
        return text or None
    return None


def _classify_source(payload: dict) -> tuple[str, str | None]:
    metadata = _as_dict(payload.get("metadata"))
    device = _as_dict(metadata.get("device"))
    data_origin = _as_dict(metadata.get("dataOrigin") or metadata.get("data_origin"))

    device_type = _as_text(device.get("type") or device.get("device_type"))
    device_model = _as_text(device.get("model"))
    device_manufacturer = _as_text(device.get("manufacturer"))
    package_name = _as_text(
        data_origin.get("packageName")
        or data_origin.get("package_name")
        or payload.get("packageName")
        or payload.get("package_name")
    )

    type_lower = (device_type or "").lower()
    model_lower = (device_model or "").lower()
    manufacturer_lower = (device_manufacturer or "").lower()
    package_lower = (package_name or "").lower()

    watch_keywords = (
        "watch",
        "wear os",
        "wearos",
        "wrist",
        "fitbit",
        "galaxy watch",
        "pixel watch",
    )
    phone_keywords = (
        "phone",
        "smartphone",
        "mobile",
        "android phone",
    )

    source_type = "other"
    if any(keyword in type_lower for keyword in watch_keywords) or any(
        keyword in model_lower for keyword in watch_keywords
    ) or any(keyword in manufacturer_lower for keyword in ("fitbit",)):
        source_type = "watch"
    elif any(keyword in type_lower for keyword in phone_keywords) or any(
        keyword in model_lower for keyword in phone_keywords
    ):
        source_type = "phone"
    elif model_lower.startswith("pixel") and "watch" not in model_lower:
        source_type = "phone"
    elif ".wear" in package_lower or "wearos" in package_lower:
        source_type = "watch"

    details: list[str] = []
    if device_type:
        details.append(f"device_type={device_type}")
    if device_manufacturer:
        details.append(f"manufacturer={device_manufacturer}")
    if device_model:
        details.append(f"model={device_model}")
    if package_name:
        details.append(f"package={package_name}")

    source_detail = "; ".join(details) if details else None
    return source_type, source_detail


def _fetch_raw_events_for_normalization(limit: int, since_id: int):
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT id, received_at, source, metric, payload_json
        FROM raw_events
        WHERE id > ?
          AND COALESCE(source, '') = 'health_connect'
          AND COALESCE(metric, '') = 'steps'
        ORDER BY id ASC
        LIMIT ?
        """,
        (since_id, limit),
    ).fetchall()
    return conn, rows


def _build_measurement_from_raw(row, payload: dict, created_at: str) -> tuple:
    source_type, source_detail = _classify_source(payload)

    return (
        row["id"],
        payload.get("source") or row["source"] or "unknown",
        source_type,
        source_detail,
        "steps_total",
        payload.get("start_at"),
        payload.get("end_at"),
        payload.get("value"),
        payload.get("unit"),
        created_at,
    )


def normalize_steps(limit: int = 100, since_id: int = 0) -> dict:
    ensure_db()

    conn, rows = _fetch_raw_events_for_normalization(limit=limit, since_id=since_id)
    target_count = len(rows)
    inserted_count = 0
    skipped_count = 0
    parse_error_count = 0
    created_at = datetime.now(timezone.utc).isoformat()

    for row in rows:
        try:
            payload = json.loads(row["payload_json"])
        except Exception:
            parse_error_count += 1
            continue

        measurement = _build_measurement_from_raw(
            row=row,
            payload=payload,
            created_at=created_at,
        )

        cur = conn.execute(
            """
            INSERT OR IGNORE INTO measurements
              (
                raw_event_id,
                source,
                source_type,
                source_detail,
                metric,
                ts_start,
                ts_end,
                value,
                unit,
                quality_flag,
                created_at
              )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?)
            """,
            measurement,
        )
        if cur.rowcount == 1:
            inserted_count += 1
        else:
            skipped_count += 1

    conn.commit()
    conn.close()

    return {
        "ok": True,
        "target_count": target_count,
        "inserted_count": inserted_count,
        "skipped_count": skipped_count,
        "parse_error_count": parse_error_count,
    }
