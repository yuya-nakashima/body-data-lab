from __future__ import annotations

import logging
import os
import sys
from datetime import datetime
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

from app.core.timeutil import JST
from app.services.aggregate_service import aggregate_daily_metrics, get_daily_summary
from app.services.normalize_service import normalize_steps
from etl.notifier import notify_error, notify_success


logger = logging.getLogger(__name__)


def _fmt_steps(value: float | None) -> str:
    if value is None:
        return "未"
    return f"{int(value):,} 歩"


def _fmt_diff(value: float | None) -> str:
    if value is None:
        return "未"
    sign = "+" if value >= 0 else ""
    return f"{sign}{int(value):,} 歩"


def build_summary_message(summary: dict) -> str:
    target_day = summary["target_day"]
    now_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M")

    lines = [
        f"[Body Data Lab] 日次サマリー {target_day}",
        "",
        "--- 歩数 (steps_total) ---",
        f"当日値    : {_fmt_steps(summary['current_value'])}",
        f"前日差分  : {_fmt_diff(summary['day_diff'])}",
        f"週平均差  : {_fmt_diff(summary['week_diff'])}",
        "",
        "---",
        f"取得日時: {now_jst} JST",
    ]
    return "\n".join(lines)


def run_etl() -> dict[str, dict]:
    normalize_result = normalize_steps()
    aggregate_result = aggregate_daily_metrics()
    return {
        "normalize": normalize_result,
        "aggregate": aggregate_result,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    try:
        run_etl()
        summary = get_daily_summary()
        message = build_summary_message(summary)
        target_day = summary["target_day"]
        notify_success(message, subject=f"[Body Data Lab] 日次サマリー {target_day}")
    except Exception as exc:
        logger.exception("ETL failed")
        try:
            notify_error(str(exc))
        except Exception:
            logger.exception("Failed to send ETL error notification")
        raise


if __name__ == "__main__":
    main()
