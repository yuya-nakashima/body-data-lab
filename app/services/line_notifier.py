from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger(__name__)

LINE_API_URL = "https://api.line.me/v2/bot/message/push"


def _line_settings() -> dict[str, str]:
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
    user_id = os.environ.get("LINE_USER_ID", "").strip()

    missing = [name for name, val in (("LINE_CHANNEL_ACCESS_TOKEN", token), ("LINE_USER_ID", user_id)) if not val]
    if missing:
        raise ValueError(f"Missing LINE settings: {', '.join(missing)}")

    return {"token": token, "user_id": user_id}


def send_line(text: str) -> None:
    settings = _line_settings()
    headers = {
        "Authorization": f"Bearer {settings['token']}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": settings["user_id"],
        "messages": [{"type": "text", "text": text}],
    }
    response = httpx.post(LINE_API_URL, headers=headers, json=payload, timeout=15)
    if not response.is_success:
        logger.error("LINE API error %s: %s", response.status_code, response.text)
    response.raise_for_status()


def build_reflection_message(reflection: dict | None, date: str) -> str:
    if reflection is None:
        return f"【振り返り {date}】\n記録がありません。"

    field_labels = [
        ("want_to_do", "やりたいこと"),
        ("anxiety", "不安なこと"),
        ("unconscious_desire", "無意識が求めること"),
        ("free_text", "自由記述"),
    ]

    lines = [f"【振り返り {date}】"]
    for key, label in field_labels:
        value = reflection.get(key)
        if value and value.strip():
            lines.append(f"\n▷ {label}")
            lines.append(value.strip())

    if len(lines) == 1:
        lines.append("\n（入力なし）")

    return "\n".join(lines)
