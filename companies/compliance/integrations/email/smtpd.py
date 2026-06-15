"""
smtp.py
Deterministic SMTP helper for BaseLayerOS.

This is intentionally minimal:
- no global state
- no implicit retries
- no background threads
- no hidden TLS negotiation
"""

from dataclasses import dataclass
import smtplib
from email.message import EmailMessage
from typing import Optional


@dataclass
class SMTPConfig:
    host: str
    port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True


class SMTPClient:
    """
    Deterministic SMTP client wrapper.
    """

    def __init__(self, config: SMTPConfig) -> None:
        self.config = config

    def send(
        self,
        to: str,
        subject: str,
        body: str,
        sender: Optional[str] = None,
    ) -> None:
        """
        Send a simple text email deterministically.
        """

        msg = EmailMessage()
        msg["To"] = to
        msg["From"] = sender or self.config.username or "no-reply@example.com"
        msg["Subject"] = subject
        msg.set_content(body)

        # Connect
        with smtplib.SMTP(self.config.host, self.config.port) as server:
            if self.config.use_tls:
                server.starttls()

            if self.config.username and self.config.password:
                server.login(self.config.username, self.config.password)

            server.send_message(msg)
