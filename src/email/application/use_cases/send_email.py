import os
import smtplib
from src.email.domain.entities import Email
from src.email.domain.exceptions import EmailTransportException

class SendEmail:
    def __init__(self):
        self.host = os.getenv("MAILER_HOST")
        self.port = int(os.getenv("MAILER_PORT", 587))
        self.user = os.getenv("MAILER_USER")
        self.password = os.getenv("MAILER_PASSWORD")
        self.from_addr = os.getenv("MAILER_USER")


    def execute(
        self,
        email: Email
    ):
        msg = email.model_dump()
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
        except Exception:
            raise EmailTransportException()