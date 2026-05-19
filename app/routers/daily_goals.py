from __future__ import annotations

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.db import get_conn
from app.core.timeutil import JST

router = APIRouter(prefix="/daily-goals", tags=["daily-goals"])


class GoalIn(BaseModel):
    content: str
    sort_order: int = 0
    minimum_goal: Optional[str] = None


class GoalPatch(BaseModel):
    minimum_goal: Optional[str] = None


class CompletionPatch(BaseModel):
    done: bool
    count: int = 1


class MinimumCompletionPatch(BaseModel):
    minimum_done: bool


class ReorderIn(BaseModel):
    ids: list[int]


def _goals_with_completion(conn, day: Optional[str] = None) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM daily_goals ORDER BY sort_order, id"
    ).fetchall()
    result = []
    for row in rows:
        d = dict(row)
        if day:
            comp = conn.execute(
                "SELECT done, count, minimum_done FROM daily_goal_completions WHERE goal_id = ? AND day = ?",
                (row["id"], day),
            ).fetchone()
            d["done"] = bool(comp["done"]) if comp else False
            d["count"] = comp["count"] if comp else 0
            d["minimum_done"] = bool(comp["minimum_done"]) if comp else False
        result.append(d)
    return result


@router.get("")
def list_goals(day: Optional[str] = None):
    conn = get_conn()
    goals = _goals_with_completion(conn, day)
    conn.close()
    return {"ok": True, "goals": goals}


@router.post("", status_code=201)
def create_goal(body: GoalIn):
    content = body.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    created_at = datetime.now(JST).isoformat()
    conn = get_conn()
    minimum_goal = body.minimum_goal.strip() if body.minimum_goal else None
    cursor = conn.execute(
        "INSERT INTO daily_goals (content, minimum_goal, sort_order, created_at) VALUES (?, ?, ?, ?)",
        (content, minimum_goal, body.sort_order, created_at),
    )
    goal_id = cursor.lastrowid
    conn.commit()
    goal = dict(conn.execute("SELECT * FROM daily_goals WHERE id = ?", (goal_id,)).fetchone())
    conn.close()
    return {"ok": True, "goal": goal}


@router.patch("/reorder")
def reorder_goals(body: ReorderIn):
    conn = get_conn()
    for i, goal_id in enumerate(body.ids):
        conn.execute("UPDATE daily_goals SET sort_order = ? WHERE id = ?", (i, goal_id))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.patch("/{goal_id}")
def patch_goal(goal_id: int, body: GoalPatch):
    if "minimum_goal" not in body.model_fields_set:
        return {"ok": True}
    conn = get_conn()
    if not conn.execute("SELECT id FROM daily_goals WHERE id = ?", (goal_id,)).fetchone():
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    minimum_goal = body.minimum_goal.strip() if body.minimum_goal else None
    conn.execute(
        "UPDATE daily_goals SET minimum_goal = ? WHERE id = ?",
        (minimum_goal, goal_id),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.delete("/{goal_id}")
def delete_goal(goal_id: int):
    conn = get_conn()
    conn.execute("PRAGMA foreign_keys = ON")
    if not conn.execute("SELECT id FROM daily_goals WHERE id = ?", (goal_id,)).fetchone():
        conn.close()
        return JSONResponse(status_code=404, content={"ok": False, "error": "not_found"})
    conn.execute("DELETE FROM daily_goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()
    return {"ok": True}


@router.patch("/{goal_id}/minimum-completion")
def patch_minimum_completion(goal_id: int, body: MinimumCompletionPatch, day: str = ""):
    if not day:
        raise HTTPException(status_code=400, detail="day is required")
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO daily_goal_completions (goal_id, day, done, count, minimum_done)
        VALUES (?, ?, 0, 0, ?)
        ON CONFLICT(goal_id, day) DO UPDATE SET minimum_done = excluded.minimum_done
        """,
        (goal_id, day, 1 if body.minimum_done else 0),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.patch("/{goal_id}/completion")
def patch_completion(goal_id: int, body: CompletionPatch, day: str = ""):
    if not day:
        raise HTTPException(status_code=400, detail="day is required")
    conn = get_conn()
    count = body.count if body.done else 0
    conn.execute(
        """
        INSERT INTO daily_goal_completions (goal_id, day, done, count, minimum_done)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(goal_id, day) DO UPDATE SET
          done = excluded.done,
          count = excluded.count,
          minimum_done = CASE WHEN excluded.done = 1 THEN 1 ELSE minimum_done END
        """,
        (goal_id, day, 1 if body.done else 0, count, 1 if body.done else 0),
    )
    conn.commit()
    conn.close()
    return {"ok": True}
