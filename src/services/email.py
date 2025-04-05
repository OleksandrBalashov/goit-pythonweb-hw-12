from pathlib import Path
import os
from dotenv import load_dotenv

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.services.auth import create_email_token

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    Send a verification email to the user.
    Parameters:
    - email (EmailStr): The email address of the user.
    - username (str): The username of the user.
    - host (str): The host URL for the email verification link.
    """
    try:
        token_verification = create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionErrors as err:
        print(err)


async def send_reset_password_email(
    to_email: EmailStr, username: str, host: str, reset_token: str
) -> None:
    """
    Send a password reset email to the user.
    Parameters:
    - to_email (EmailStr): The email address of the user.
    - username (str): The username of the user.
    - host (str): The host URL for the password reset link.
    - reset_token (str): The token for password reset.
    Raises:
    - ConnectionErrors: If there is an error in sending the email.
    - HTTPException: If the email is not sent successfully.
    - Exception: If there is any other error in sending the email.
    """
    try:
        reset_link = f"{host}api/auth/confirm_reset_password/{reset_token}"

        message = MessageSchema(
            subject="Important: Update your account information",
            recipients=[to_email],
            template_body={"reset_link": reset_link, "username": username},
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password.html")
    except ConnectionErrors as err:
        print(err)
