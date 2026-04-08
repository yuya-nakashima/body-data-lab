from __future__ import annotations

import logging
import os
import smtplib
from email.message import EmailMessage


logger = logging.getLogger(__name__)


def _mail_settings() -> dict[str, object]:
    host = os.environ.get("MAIL_HOST", "").strip()
    port = int(os.environ.get("MAIL_PORT", "587"))
    username = os.environ.get("MAIL_USERNAME", "").strip()
    password = os.environ.get("MAIL_PASSWORD", "")
    mail_from = os.environ.get("MAIL_FROM", "").strip()
    mail_to = os.environ.get("MAIL_TO", "").strip()
    use_tls = os.environ.get("MAIL_TLS", "true").strip().lower() != "false"

    missing = [
        name
        for name, value in (
            ("MAIL_HOST", host),
            ("MAIL_PORT", str(port)),
            ("MAIL_USERNAME", username),
            ("MAIL_PASSWORD", password),
            ("MAIL_FROM", mail_from),
            ("MAIL_TO", mail_to),
        )
        if not value
    ]
    if missing:
        raise ValueError(f"Missing mail settings: {', '.join(missing)}")

    return {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "mail_from": mail_from,
        "mail_to": mail_to,
        "use_tls": use_tls,
    }


def send_mail(subject: str, body: str) -> None:
    try:
        settings = _mail_settings()

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = settings["mail_from"]
        message["To"] = settings["mail_to"]
        message.set_content(body)

        with smtplib.SMTP(settings["host"], settings["port"], timeout=30) as smtp:
            smtp.ehlo()
            if settings["use_tls"]:
                smtp.starttls()
                smtp.ehlo()
            if smtp.has_extn("auth"):
                smtp.login(settings["username"], settings["password"])
            smtp.send_message(message)
    except Exception:
        logger.exception("Failed to send mail notification")
        raise


def notify_success(message: str, subject: str = "[Body Data Lab] ETL Success") -> None:
    send_mail(subject=subject, body=message)


def notify_error(error: str) -> None:
    send_mail(subject="[Body Data Lab] ETL Error", body=error)
