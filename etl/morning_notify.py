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
        send_line(message)
        logger.info("LINE notification sent for %s", yesterday)
    except Exception:
        logger.exception("Failed to send morning LINE notification")
        raise


if __name__ == "__main__":
    main()
