from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.db import get_conn
from app.core.timeutil import JST

router = APIRouter(prefix="/wishes", tags=["wishes"])


class CategoryIn(BaseModel):
    name: str


class ItemIn(BaseModel):
    content: str


def _category_with_items(conn, category_id: int) -> Optional[dict]:
    row = conn.execute(
        "SELECT * FROM wish_categories WHERE id = ?", (category_id,)
    ).fetchone()
    if row is None:
        return None
    items = conn.execute(
        "SELECT * FROM wish_items WHERE category_id = ? ORDER BY id",
        (category_id,),
    ).fetchall()
    return {**dict(row), "items": [dict(i) for i in items]}


@router.get("/categories")
def list_categories():
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM wish_categories ORDER BY id"
    ).fetchall()
    result = []
    for row in rows:
        items = conn.execute(
            "SELECT * FROM wish_items WHERE category_id = ? ORDER BY id",
            (row["id"],),
        ).fetchall()
        result.append({**dict(row), "items": [dict(i) for i in items]})
    conn.close()
    return {"ok": True, "categories": result}


@router.post("/categories", status_code=201)
def create_category(body: CategoryIn):
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    created_at = datetime.now(JST).isoformat()
    conn = get_conn()
    try:
        cursor = conn.execute(
            "INSERT INTO wish_categories (name, created_at) VALUES (?, ?)",
            (name, created_at),
        )
        category_id = cursor.lastrowid
        conn.commit()
    except Exception:
        conn.close()
        raise HTTPException(status_code=409, detail="category already exists")

    category = _category_with_items(conn, category_id)
    conn.close()
    return {"ok": True, "category": category}


@router.delete("/categories/{category_id}", status_code=200)
def delete_category(category_id: int):
    conn = get_conn()
    conn.execute("PRAGMA foreign_keys = ON")
    row = conn.execute(
        "SELECT id FROM wish_categories WHERE id = ?", (category_id,)
    ).fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    conn.execute("DELETE FROM wish_categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/categories/{category_id}/items", status_code=201)
def create_item(category_id: int, body: ItemIn):
    content = body.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")

    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM wish_categories WHERE id = ?", (category_id,)
    ).fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "category_not_found"})

    created_at = datetime.now(JST).isoformat()
    cursor = conn.execute(
        "INSERT INTO wish_items (category_id, content, created_at) VALUES (?, ?, ?)",
        (category_id, content, created_at),
    )
    item_id = cursor.lastrowid
    conn.commit()
    item = conn.execute("SELECT * FROM wish_items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return {"ok": True, "item": dict(item)}


@router.delete("/items/{item_id}", status_code=200)
def delete_item(item_id: int):
    conn = get_conn()
    row = conn.execute(
        "SELECT id FROM wish_items WHERE id = ?", (item_id,)
    ).fetchone()
    if row is None:
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    conn.execute("DELETE FROM wish_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"ok": True}
