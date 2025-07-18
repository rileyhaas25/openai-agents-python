from pydantic import BaseModel
from agents import Agent, function_tool
from __future__ import annotations
import os
from pathlib import Path
import smtplib
from email.message import EmailMessage


def _load_env_file(path: str = ".env") -> None:
    """Load environment variables from ``path`` if it exists."""
    try:
        for line in Path(path).read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, sep, value = line.partition("=")
            if sep:
                os.environ.setdefault(key, value)
    except FileNotFoundError:
        return


_load_env_file()

class EmailParams(BaseModel):
    recipient: str
    subject: str
    body: str

@function_tool
async def send_email(recipent: str, subject: str, body: str) -> str:
    """Send an email using SMTP.

    Args:
        recipent: The email address to send the message to.
        subject: The subject line of the email.
        body: The content of the email body.
    """
    host = os.getenv("SMTP_HOST", "localhost")
    port = int(os.getenv("SMTP_PORT", "25"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")

    message = EmailMessage()
    message["From"] = username or "no-reply@example.com"
    message["To"] = recipent
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(host=host, port=port) as smtp:
        if username and password:
            smtp.login(username, password)
        smtp.send_message(message)

    return "Email sent successfully."

send_email_agent = Agent(
    name="EmailSenderAgent",
    instructions="Send the provided report via email using the send_email tool.",
    tools=[send_email]
)



