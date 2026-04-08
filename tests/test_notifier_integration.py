"""Integration tests for etl.notifier against a real Mailpit SMTP server.

Run these only when Mailpit is available:

    docker compose up -d mailpit
    MAILPIT_API_URL=http://localhost:8025 pytest tests/test_notifier_integration.py -v

Or inside the app container (Mailpit reachable as "mailpit"):

    MAILPIT_API_URL=http://mailpit:8025 pytest tests/test_notifier_integration.py -v
"""
from __future__ import annotations

import os

import httpx
import pytest

from etl.notifier import notify_error, notify_success


MAILPIT_API_URL = os.environ.get("MAILPIT_API_URL", "http://localhost:8025")

# Skip the whole module when Mailpit is not reachable.
def _mailpit_reachable() -> bool:
    try:
        httpx.get(f"{MAILPIT_API_URL}/api/v1/info", timeout=2).raise_for_status()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _mailpit_reachable(),
    reason="Mailpit not reachable — start it with: docker compose up -d mailpit",
)

# Always point to the local Mailpit instance — never use real SMTP credentials.
MAIL_ENV = {
    "MAIL_HOST": "127.0.0.1",
    "MAIL_PORT": "1025",
    "MAIL_USERNAME": "dummy",
    "MAIL_PASSWORD": "dummy",
    "MAIL_FROM": "etl@local",
    "MAIL_TO": "dev@local",
    "MAIL_TLS": "false",  # Mailpit does not support STARTTLS by default
}


@pytest.fixture(autouse=True)
def clear_mailpit():
    """各テスト前後にMailpitの受信ボックスをクリアする。"""
    httpx.delete(f"{MAILPIT_API_URL}/api/v1/messages")
    yield
    httpx.delete(f"{MAILPIT_API_URL}/api/v1/messages")


def _latest_message() -> dict:
    resp = httpx.get(f"{MAILPIT_API_URL}/api/v1/messages")
    resp.raise_for_status()
    messages = resp.json().get("messages", [])
    assert messages, "Mailpit received no messages"
    return messages[0]


class TestNotifySuccessIntegration:
    def test_subject(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        notify_success("ETL completed: 42 rows processed")

        msg = _latest_message()
        assert msg["Subject"] == "[Body Data Lab] ETL Success"

    def test_from_and_to(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        notify_success("ok")

        msg = _latest_message()
        assert msg["From"]["Address"] == MAIL_ENV["MAIL_FROM"]
        assert msg["To"][0]["Address"] == MAIL_ENV["MAIL_TO"]


class TestNotifyErrorIntegration:
    def test_subject(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        notify_error("Something went wrong: TimeoutError")

        msg = _latest_message()
        assert msg["Subject"] == "[Body Data Lab] ETL Error"

    def test_body_contains_error_message(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        notify_error("DB connection failed")

        msg_id = _latest_message()["ID"]
        detail = httpx.get(f"{MAILPIT_API_URL}/api/v1/message/{msg_id}").json()
        assert "DB connection failed" in detail["Text"]
