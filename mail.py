"""Optional SMTP notifications for the admissions chatbot."""

import os
import smtplib
import ssl
from email.message import EmailMessage


def send_notification(recipient, subject, body):
    """Send an email when notifications are enabled in the environment."""
    if os.getenv("ENABLE_EMAIL_NOTIFICATIONS", "false").strip().lower() != "true":
        return False

    host = os.getenv("SMTP_HOST")
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    sender = os.getenv("SMTP_FROM") or username
    if not all((host, username, password, sender)):
        raise ValueError("Configure SMTP_HOST, SMTP_USERNAME and SMTP_PASSWORD to send notifications.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    port = int(os.getenv("SMTP_PORT") or "587")
    tls_context = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(host, port, context=tls_context, timeout=15) as smtp:
            smtp.login(username, password)
            smtp.send_message(message)
    else:
        with smtplib.SMTP(host, port, timeout=15) as smtp:
            smtp.starttls(context=tls_context)
            smtp.login(username, password)
            smtp.send_message(message)
    return True
