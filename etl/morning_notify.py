from __future__ import annotations

import logging
import os
import sys
from datetime import date, timedelta
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

    yesterday = (date.today() - timedelta(days=1)).isoformat()
    logger.info("Fetching reflection for %s", yesterday)

    try:
        reflection = fetch_reflection(yesterday)
        message = build_reflection_message(reflection, yesterday)
        wish_section = build_wish_list_section(fetch_wish_list())
        if wish_section:
            message = message + "\n" + wish_section
        send_line(message)
        logger.info("LINE notification sent for %s", yesterday)
    except Exception:
        logger.exception("Failed to send morning LINE notification")
        raise


if __name__ == "__main__":
    main()
