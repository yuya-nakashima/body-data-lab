from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.db import get_conn
from app.core.timeutil import JST, parse_iso8601

router = APIRouter(prefix="/reflections", tags=["reflections"])


class ReflectionIn(BaseModel):
    recorded_at: str
    want_to_do: Optional[str] = None
    anxiety: Optional[str] = None
    unconscious_desire: Optional[str] = None
    free_text: Optional[str] = None
    woop_wish: Optional[str] = None
    woop_outcome: Optional[str] = None
    woop_obstacle: Optional[str] = None
    woop_plan: Optional[str] = None
    implementation_intention: Optional[str] = None


class ReflectionPatch(BaseModel):
    want_to_do: Optional[str] = None
    anxiety: Optional[str] = None
    unconscious_desire: Optional[str] = None
    free_text: Optional[str] = None
    woop_wish: Optional[str] = None
    woop_outcome: Optional[str] = None
    woop_obstacle: Optional[str] = None
    woop_plan: Optional[str] = None
    implementation_intention: Optional[str] = None


def _row_to_dict(row) -> dict:
    return dict(row)


@router.get("")
def list_reflections(limit: int = 30, offset: int = 0):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM reflections ORDER BY day DESC, id DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    conn.close()
    return {"ok": True, "reflections": [_row_to_dict(r) for r in rows]}


@router.post("", status_code=201)
def create_reflection(body: ReflectionIn):
    all_fields = [
        body.want_to_do, body.anxiety, body.unconscious_desire, body.free_text,
        body.woop_wish, body.woop_outcome, body.woop_obstacle, body.woop_plan,
        body.implementation_intention,
    ]
    if all(f is None or f.strip() == "" for f in all_fields):
        raise HTTPException(status_code=400, detail="At least one field must be non-empty")

    dt = parse_iso8601(body.recorded_at)
    if dt is None:
        raise HTTPException(status_code=400, detail="Invalid recorded_at format")

    day = dt.astimezone(JST).date().isoformat()
    created_at = datetime.now(JST).isoformat()

    conn = get_conn()
    cursor = conn.execute(
        """
        INSERT INTO reflections (
            recorded_at, day, want_to_do, anxiety, unconscious_desire, free_text,
            woop_wish, woop_outcome, woop_obstacle, woop_plan, implementation_intention,
            created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            body.recorded_at, day, body.want_to_do, body.anxiety,
            body.unconscious_desire, body.free_text,
            body.woop_wish, body.woop_outcome, body.woop_obstacle, body.woop_plan,
            body.implementation_intention, created_at,
        ),
    )
    row_id = cursor.lastrowid
    conn.commit()
    row = conn.execute("SELECT * FROM reflections WHERE id = ?", (row_id,)).fetchone()
    conn.close()
    return {"ok": True, "reflection": _row_to_dict(row)}


@router.get("/today")
def get_today_reflection():
    today = datetime.now(JST).date().isoformat()
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM reflections WHERE day = ? ORDER BY id DESC LIMIT 1",
        (today,),
    ).fetchone()
    conn.close()
    if row is None:
        return {"ok": True, "reflection": None}
    return {"ok": True, "reflection": _row_to_dict(row)}


@router.get("/{date}")
def get_reflection_by_date(date: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM reflections WHERE day = ? ORDER BY id DESC LIMIT 1",
        (date,),
    ).fetchone()
    conn.close()
    if row is None:
        return {"ok": True, "reflection": None}
    return {"ok": True, "reflection": _row_to_dict(row)}


@router.patch("/{reflection_id}")
def patch_reflection(reflection_id: int, body: ReflectionPatch):
    conn = get_conn()
    row = conn.execute("SELECT * FROM reflections WHERE id = ?", (reflection_id,)).fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})

    updates = body.model_dump(exclude_unset=True)
    if not updates:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [reflection_id]
    conn.execute(f"UPDATE reflections SET {set_clause} WHERE id = ?", values)
    conn.commit()
    updated = conn.execute("SELECT * FROM reflections WHERE id = ?", (reflection_id,)).fetchone()
    conn.close()
    return {"ok": True, "reflection": _row_to_dict(updated)}
