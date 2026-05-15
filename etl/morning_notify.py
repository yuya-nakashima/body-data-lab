from __future__ import annotations

import logging
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file(ROOT_DIR / ".env")

from app.core.db import get_conn
from app.core.timeutil import JST
from app.services.line_notifier import build_reflection_message, send_line
from etl.notifier import send_mail


def fetch_wish_list() -> list[dict]:
    conn = get_conn()
    categories = conn.execute(
        "SELECT * FROM wish_categories ORDER BY id"
    ).fetchall()
    result = []
    for cat in categories:
        items = conn.execute(
            "SELECT content FROM wish_items WHERE category_id = ? ORDER BY id",
            (cat["id"],),
        ).fetchall()
        result.append({"name": cat["name"], "items": [row["content"] for row in items]})
    conn.close()
    return result


def fetch_daily_goals(target_date: str) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT g.content, COALESCE(c.done, 0) AS done, COALESCE(c.count, 0) AS count
        FROM daily_goals g
        LEFT JOIN daily_goal_completions c ON c.goal_id = g.id AND c.day = ?
        ORDER BY g.sort_order, g.id
        """,
        (target_date,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_daily_goals_section(goals: list[dict]) -> str:
    done_goals = [g for g in goals if g["done"]]
    if not done_goals:
        return ""
    lines = ["【今日の目標】"]
    for goal in done_goals:
        count = goal.get("count", 1)
        suffix = f" × {count}" if count > 1 else ""
        lines.append(f"  ✓ {goal['content']}{suffix}")
    return "\n".join(lines)


def fetch_habits(target_date: str) -> list[dict]:
    conn = get_conn()
    groups = conn.execute(
        "SELECT * FROM habit_groups ORDER BY sort_order, id"
    ).fetchall()
    result = []
    for group in groups:
        items = conn.execute(
            """
            SELECT i.content, COALESCE(c.done, 0) AS done, COALESCE(c.count, 0) AS count
            FROM habit_group_items i
            LEFT JOIN habit_completions c ON c.item_id = i.id AND c.day = ?
            WHERE i.group_id = ?
            ORDER BY i.sort_order, i.id
            """,
            (target_date, group["id"]),
        ).fetchall()
        result.append({"name": group["name"], "items": [dict(r) for r in items]})
    conn.close()
    return result


def build_habits_section(groups: list[dict]) -> str:
    lines = []
    for group in groups:
        done_items = [i for i in group["items"] if i["done"]]
        if not done_items:
            continue
        lines.append(f"\n▷ {group['name']}")
        for item in done_items:
            count = item.get("count", 1)
            suffix = f" × {count}" if count > 1 else ""
            lines.append(f"  ✓ {item['content']}{suffix}")
    if not lines:
        return ""
    return "【今日の習慣チェック】" + "\n".join(lines)


def build_wish_list_section(categories: list[dict]) -> str:
    if not categories:
        return ""
    lines = ["\n【やりたいことリスト】"]
    for cat in categories:
        lines.append(f"\n▷ {cat['name']}")
        for item in cat["items"]:
            lines.append(f"  ・{item}")
        if not cat["items"]:
            lines.append("  （なし）")
    return "\n".join(lines)

logger = logging.getLogger(__name__)


def fetch_reflection(target_date: str) -> dict | None:
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM reflections WHERE day = ? ORDER BY id DESC LIMIT 1",
        (target_date,),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    jst_today = datetime.now(JST).date()
    yesterday = (jst_today - timedelta(days=1)).isoformat()
    logger.info("Fetching reflection for %s", yesterday)

    today = jst_today.isoformat()

    try:
        goals_section = build_daily_goals_section(fetch_daily_goals(today))
        habits_section = build_habits_section(fetch_habits(today))
        reflection_section = build_reflection_message(fetch_reflection(yesterday), yesterday)
        wish_section = build_wish_list_section(fetch_wish_list())

        parts = [goals_section, habits_section, reflection_section, wish_section]
        message = "\n".join(p for p in parts if p)
        send_line(message)
        logger.info("LINE notification sent for %s", yesterday)
        send_mail(subject=f"[Body Data Lab] 振り返り {yesterday}", body=message)
        logger.info("Mail notification sent for %s", yesterday)
    except Exception:
        logger.exception("Failed to send morning notification")
        raise


if __name__ == "__main__":
    main()
