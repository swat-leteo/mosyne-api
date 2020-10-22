"""
Functions to manage the email sends.
"""

# Built in
import os
from pathlib import Path

# Settings
from config import settings

# Email sender
from .sender import email_sender

###################
# Email Functions #
###################

templates_dir = Path(f"{os.getcwd()}/services/mails/templates")


def send_verification_email(recipient_name: str, email: str, token: str) -> None:
    """Send a welcome/verification email.

    Params:
    -------
    - recipient_name: str - The name of the new user.
    - email: str - The target email.
    """
    with open(f"{templates_dir}/welcome.html") as f:
        template_str = f.read()

    link = f"{settings.WEB_HOST}/verification?token={token}"
    email_content = template_str.format(recipient_name=recipient_name, link=link)

    email = email_sender.create_email(
        to_list=[email],
        subject="Mosyne - Verification email",
        html_content=email_content,
    )
    email_sender.send_email(email=email)


def send_recovery_password_email(email: str, token: str) -> None:
    """Send a email with a link with the token to reset the password.

    Params:
    -------
    - email: str - The user email
    - token: str - The encoded JWT for recovery password
    """
    with open(f"{templates_dir}/recovery_password.html") as f:
        template_str = f.read()

    link = f"{settings.WEB_HOST}/recovery-password?token={token}"
    email_content = template_str.format(link=link)

    email = email_sender.create_email(
        to_list=[email],
        subject="Mosyne - Recovery password",
        html_content=email_content,
    )
    email_sender.send_email(email=email)


def send_angel_advise(
    email: str, angel_name: str, lat: str = None, lon: str = None
) -> None:
    """Send email to guardian when an angel profile is visited.

    Params:
    -------
    - email: str - The guardian email
    - angel_name: str - The name of the angel.
    - lat: str - The latitude of the profile visitant
    - lon: str - The longitude of the profile visitant
    """
    with open(f"{templates_dir}/angel_advise.html") as f:
        template_str = f.read()

    if lat and lon:
        location = f"Lat: {lat}, Lon: {lon}"
    else:
        location = "Desconocida."

    email_content = template_str.format(angel_name=angel_name, location=location)

    email = email_sender.create_email(
        to_list=[email],
        subject="Mosyne - Aviso Importante.",
        html_content=email_content,
    )
    email_sender.send_email(email=email)
