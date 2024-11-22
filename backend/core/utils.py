# utils.py
import os
from pathlib import Path
from email.message import EmailMessage
import smtplib
import logging
import requests
import ulid
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
path = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=path / ".env")

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
        raise
    except Exception as general_error:
        logger.error("Unexpected error occurred while sending email to %s: %s",
                     email, general_error)
        raise

def download_user_icon(url: str, user_id: str) -> str:
    """
    Downloads a user icon from the specified URL and saves it locally with a unique filename.

    Args:
        url (str): The URL of the user icon to download.
        user_id (str): The unique identifier of the user, used in the generated filename.

    Returns:
        str: The filename of the saved icon.
    """
    try:
        response = requests.get(url, stream=True, timeout=None)
        response.raise_for_status()

        # Get the content type from the response headers
        content_type = response.headers.get('Content-Type', '')

        # Map common MIME types to file extensions
        mime_to_extension = {
            "image/jpeg": "jpg",
            "image/png": "png",
            "image/gif": "gif",
            "image/webp": "webp",
        }
        file_extension = mime_to_extension.get(content_type, "png")  # Default to 'png' if unknown

        # Define file name based on user ID and ULID
        icon_filename = f"{user_id}I{str(ulid.new())}.{file_extension}"
        icon_path = Path(path / f"static/icons/{icon_filename}")

        # Ensure the directory exists
        icon_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the image to the file
        with open(icon_path, "wb") as icon_file:
            for chunk in response.iter_content(1024):
                icon_file.write(chunk)

        # Return only the filename
        return icon_filename

    except requests.RequestException as exc:
        return exc
