from __future__ import annotations

import smtplib
from unittest.mock import MagicMock, patch

import pytest

from etl.notifier import notify_error, notify_success, send_mail


MAIL_ENV = {
    "MAIL_HOST": "smtp.example.com",
    "MAIL_PORT": "587",
    "MAIL_USERNAME": "user@example.com",
    "MAIL_PASSWORD": "secret",
    "MAIL_FROM": "from@example.com",
    "MAIL_TO": "to@example.com",
}


# ---------------------------------------------------------------------------
# send_mail
# ---------------------------------------------------------------------------

class TestSendMail:
    def test_sends_message_with_correct_fields(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        mock_smtp = MagicMock()
        with patch("smtplib.SMTP", return_value=mock_smtp.__enter__.return_value):
            mock_instance = MagicMock()
            mock_smtp.__enter__ = MagicMock(return_value=mock_instance)
            mock_smtp.__exit__ = MagicMock(return_value=False)

            with patch("smtplib.SMTP") as smtp_cls:
                smtp_cls.return_value.__enter__ = lambda s: mock_instance
                smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

                send_mail(subject="Test Subject", body="Test Body")

        mock_instance.ehlo.assert_called()
        mock_instance.starttls.assert_called_once()
        mock_instance.login.assert_called_once_with("user@example.com", "secret")
        mock_instance.send_message.assert_called_once()

        sent_msg = mock_instance.send_message.call_args[0][0]
        assert sent_msg["Subject"] == "Test Subject"
        assert sent_msg["From"] == "from@example.com"
        assert sent_msg["To"] == "to@example.com"

    def test_raises_when_env_vars_missing(self, monkeypatch):
        for k in MAIL_ENV:
            monkeypatch.delenv(k, raising=False)

        with pytest.raises(ValueError, match="Missing mail settings"):
            send_mail(subject="x", body="y")

    # MAIL_PORT has a built-in default ("587") so omitting it never raises.
    @pytest.mark.parametrize(
        "missing_key",
        [k for k in MAIL_ENV if k != "MAIL_PORT"],
    )
    def test_raises_for_each_missing_var(self, monkeypatch, missing_key):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)
        monkeypatch.delenv(missing_key)

        with pytest.raises(ValueError, match=missing_key):
            send_mail(subject="x", body="y")

    def test_reraises_smtp_exception(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        with patch("smtplib.SMTP") as smtp_cls:
            smtp_cls.return_value.__enter__ = MagicMock(
                side_effect=smtplib.SMTPException("connection refused")
            )
            smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

            with pytest.raises(smtplib.SMTPException):
                send_mail(subject="x", body="y")


# ---------------------------------------------------------------------------
# notify_success / notify_error
# ---------------------------------------------------------------------------

# TODO: etl/main.py の main() に対するテストが未実装
# - ETL 成功時に notify_success が呼ばれることの確認
# - ETL 失敗時に notify_error が呼ばれることの確認
# - notify_error 自体が失敗した場合（サイレント障害）の挙動確認


class TestNotifyHelpers:
    def test_notify_success_subject(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        with patch("etl.notifier.send_mail") as mock_send:
            notify_success("all good")

        mock_send.assert_called_once_with(
            subject="[Body Data Lab] ETL Success", body="all good"
        )

    def test_notify_success_custom_subject(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        with patch("etl.notifier.send_mail") as mock_send:
            notify_success("all good", subject="[Body Data Lab] 日次サマリー 2026-04-07")

        mock_send.assert_called_once_with(
            subject="[Body Data Lab] 日次サマリー 2026-04-07", body="all good"
        )

    def test_notify_error_subject(self, monkeypatch):
        for k, v in MAIL_ENV.items():
            monkeypatch.setenv(k, v)

        with patch("etl.notifier.send_mail") as mock_send:
            notify_error("something went wrong")

        mock_send.assert_called_once_with(
            subject="[Body Data Lab] ETL Error", body="something went wrong"
        )
