from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.db import get_conn
from app.core.timeutil import JST

router = APIRouter(prefix="/habit-stacks", tags=["habit-stacks"])


class HabitStackIn(BaseModel):
    day: str
    content: str
    anchor: Optional[str] = None
    actions: Optional[list] = None
    custom_action: Optional[str] = None
    sort_order: int = 0


class HabitStackPatch(BaseModel):
    content: Optional[str] = None
    done: Optional[bool] = None
    anchor: Optional[str] = None
    actions: Optional[list] = None
    custom_action: Optional[str] = None
    sort_order: Optional[int] = None


def _row_to_dict(row) -> dict:
    d = dict(row)
    if d.get("actions"):
        try:
            d["actions"] = json.loads(d["actions"])
        except Exception:
            d["actions"] = []
    else:
        d["actions"] = []
    d["done"] = bool(d["done"])
    return d


@router.get("")
def list_habit_stacks(day: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM habit_stacks WHERE day = ? ORDER BY sort_order, id",
        (day,),
    ).fetchall()
    conn.close()
    return {"ok": True, "stacks": [_row_to_dict(r) for r in rows]}


@router.post("", status_code=201)
def create_habit_stack(body: HabitStackIn):
    if not body.content.strip():
        raise HTTPException(status_code=400, detail="content is required")

    created_at = datetime.now(JST).isoformat()
    actions_json = json.dumps(body.actions or [], ensure_ascii=False)

    conn = get_conn()
    cursor = conn.execute(
        """
        INSERT INTO habit_stacks (day, content, done, anchor, actions, custom_action, sort_order, created_at)
        VALUES (?, ?, 0, ?, ?, ?, ?, ?)
        """,
        (body.day, body.content.strip(), body.anchor, actions_json, body.custom_action, body.sort_order, created_at),
    )
    row_id = cursor.lastrowid
    conn.commit()
    row = conn.execute("SELECT * FROM habit_stacks WHERE id = ?", (row_id,)).fetchone()
    conn.close()
    return {"ok": True, "stack": _row_to_dict(row)}


@router.patch("/{stack_id}")
def patch_habit_stack(stack_id: int, body: HabitStackPatch):
    conn = get_conn()
    row = conn.execute("SELECT * FROM habit_stacks WHERE id = ?", (stack_id,)).fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})

    updates = body.model_dump(exclude_unset=True)
    if not updates:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")

    if "actions" in updates:
        updates["actions"] = json.dumps(updates["actions"] or [], ensure_ascii=False)
    if "done" in updates:
        updates["done"] = 1 if updates["done"] else 0

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [stack_id]
    conn.execute(f"UPDATE habit_stacks SET {set_clause} WHERE id = ?", values)
    conn.commit()
    updated = conn.execute("SELECT * FROM habit_stacks WHERE id = ?", (stack_id,)).fetchone()
    conn.close()
    return {"ok": True, "stack": _row_to_dict(updated)}


@router.delete("/{stack_id}")
def delete_habit_stack(stack_id: int):
    conn = get_conn()
    row = conn.execute("SELECT id FROM habit_stacks WHERE id = ?", (stack_id,)).fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    conn.execute("DELETE FROM habit_stacks WHERE id = ?", (stack_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
