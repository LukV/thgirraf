import os
import smtplib
import logging
from pathlib import Path
from email.message import EmailMessage
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv()

SES_SMTP_SERVER = os.getenv("SES_SMTP_SERVER")
SES_SMTP_PORT = int(os.getenv("SES_SMTP_PORT", "587"))
SES_SMTP_USERNAME = os.getenv("SES_SMTP_USERNAME")
SES_SMTP_PASSWORD = os.getenv("SES_SMTP_PASSWORD")
RESET_PASSWORD_URL = os.getenv("RESET_PASSWORD_URL")

def send_reset_email(email: str, token: str):
    """Sends a password reset email to the specified recipient."""
    reset_link = f"{RESET_PASSWORD_URL}?token={token}"

    msg = EmailMessage()
    msg["Subject"] = "Password Reset Request"
    msg["From"] = "dataframe.one@gmail.com"
    msg["To"] = email
    msg.set_content(f"Click the following link to reset your password: {reset_link}")

    try:
        with smtplib.SMTP(SES_SMTP_SERVER, SES_SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SES_SMTP_USERNAME, SES_SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("Password reset email sent successfully.")
    except smtplib.SMTPException as smtp_error:
        logger.error("SMTP error occurred while sending email to %s: %s", 
                     email, smtp_error)
        raise  # Re-raise the exception for further handling
    except Exception as general_error:
        logger.error("Unexpected error occurred while sending email to %s: %s", 
                     email, general_error)
        raise
