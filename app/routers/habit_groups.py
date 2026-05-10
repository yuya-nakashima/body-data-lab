from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.db import get_conn
from app.core.timeutil import JST

router = APIRouter(prefix="/habit-groups", tags=["habit-groups"])


class GroupIn(BaseModel):
    name: str
    sort_order: int = 0


class GroupPatch(BaseModel):
    name: Optional[str] = None
    sort_order: Optional[int] = None
    woop_wish: Optional[str] = None
    woop_outcome: Optional[str] = None
    woop_obstacle: Optional[str] = None
    woop_plan: Optional[str] = None


class ItemIn(BaseModel):
    content: str
    sort_order: int = 0


class CompletionPatch(BaseModel):
    done: bool
    count: int = 1


class ReorderIn(BaseModel):
    ids: list[int]


def _group_with_items(conn, group_id: int, day: Optional[str] = None) -> Optional[dict]:
    row = conn.execute("SELECT * FROM habit_groups WHERE id = ?", (group_id,)).fetchone()
    if row is None:
        return None
    items = conn.execute(
        "SELECT * FROM habit_group_items WHERE group_id = ? ORDER BY sort_order, id",
        (group_id,),
    ).fetchall()
    item_list = []
    for item in items:
        d = dict(item)
        if day:
            comp = conn.execute(
                "SELECT done, count FROM habit_completions WHERE item_id = ? AND day = ?",
                (item["id"], day),
            ).fetchone()
            d["done"] = bool(comp["done"]) if comp else False
            d["count"] = comp["count"] if comp else 0
        item_list.append(d)
    return {**dict(row), "items": item_list}


@router.get("")
def list_groups(day: Optional[str] = None):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM habit_groups ORDER BY sort_order, id"
    ).fetchall()
    result = [_group_with_items(conn, row["id"], day) for row in rows]
    conn.close()
    return {"ok": True, "groups": result}


@router.post("", status_code=201)
def create_group(body: GroupIn):
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")
    created_at = datetime.now(JST).isoformat()
    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO habit_groups (name, sort_order, created_at) VALUES (?, ?, ?)",
        (name, body.sort_order, created_at),
    )
    group_id = cursor.lastrowid
    conn.commit()
    group = _group_with_items(conn, group_id)
    conn.close()
    return {"ok": True, "group": group}


@router.patch("/reorder")
def reorder_groups(body: ReorderIn):
    conn = get_conn()
    for i, group_id in enumerate(body.ids):
        conn.execute("UPDATE habit_groups SET sort_order = ? WHERE id = ?", (i, group_id))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.patch("/{group_id}")
def patch_group(group_id: int, body: GroupPatch):
    conn = get_conn()
    if not conn.execute("SELECT id FROM habit_groups WHERE id = ?", (group_id,)).fetchone():
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    updates = body.model_dump(exclude_unset=True)
    if not updates:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields to update")
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    conn.execute(f"UPDATE habit_groups SET {set_clause} WHERE id = ?", [*updates.values(), group_id])
    conn.commit()
    group = _group_with_items(conn, group_id)
    conn.close()
    return {"ok": True, "group": group}


@router.delete("/{group_id}")
def delete_group(group_id: int):
    conn = get_conn()
    conn.execute("PRAGMA foreign_keys = ON")
    if not conn.execute("SELECT id FROM habit_groups WHERE id = ?", (group_id,)).fetchone():
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    conn.execute("DELETE FROM habit_groups WHERE id = ?", (group_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/{group_id}/items", status_code=201)
def create_item(group_id: int, body: ItemIn):
    content = body.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    if not get_conn().execute("SELECT id FROM habit_groups WHERE id = ?", (group_id,)).fetchone():
        return JSONResponse(status_code=404, content={"ok": False, "error": "group_not_found"})
    created_at = datetime.now(JST).isoformat()
    conn = get_conn()
    cursor = conn.execute(
        "INSERT INTO habit_group_items (group_id, content, sort_order, created_at) VALUES (?, ?, ?, ?)",
        (group_id, content, body.sort_order, created_at),
    )
    item_id = cursor.lastrowid
    conn.commit()
    item = conn.execute("SELECT * FROM habit_group_items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return {"ok": True, "item": dict(item)}


@router.patch("/{group_id}/items/reorder")
def reorder_items(group_id: int, body: ReorderIn):
    conn = get_conn()
    for i, item_id in enumerate(body.ids):
        conn.execute("UPDATE habit_group_items SET sort_order = ? WHERE id = ?", (i, item_id))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = get_conn()
    conn.execute("PRAGMA foreign_keys = ON")
    if not conn.execute("SELECT id FROM habit_group_items WHERE id = ?", (item_id,)).fetchone():
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    conn.execute("DELETE FROM habit_group_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.patch("/items/{item_id}/completion")
def patch_completion(item_id: int, body: CompletionPatch, day: str = ""):
    if not day:
        raise HTTPException(status_code=400, detail="day is required")
    conn = get_conn()
    count = body.count if body.done else 0
    conn.execute(
        """
        INSERT INTO habit_completions (item_id, day, done, count)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(item_id, day) DO UPDATE SET done = excluded.done, count = excluded.count
        """,
        (item_id, day, 1 if body.done else 0, count),
    )
    conn.commit()
    conn.close()
    return {"ok": True}
