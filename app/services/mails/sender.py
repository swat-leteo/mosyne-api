"""
Emails sender class - Sendgrid implementation.
"""

# Built in
from typing import List, Type

# Sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers import mail

# Settings
from config import settings


class EmailSender:
    """Email sender abstraction.
    Perform operations to create and send emails.
    """

    def __init__(self):
        self.sendgrid = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.EMAIL_SENDER

    def create_email(
        self,
        to_list: List[str],
        subject: str,
        html_content: str,
    ) -> Type[mail.Mail]:
        """Create a new email entitie of sendgrid.

        Params:
        -------
        - to_list: List[str] - Email address list of recipients.
        - subject: str - Email subject
        - html_content: - The email content in html format

        Return:
        -------
        - email: Mail - The sendgrid emai entitie with passed data.
        """
        email: mail.Mail = mail.Mail()
        email.from_email = mail.From(self.from_email)
        email.subject = mail.Subject(subject)

        for recipient in to_list:
            email.add_to(recipient)

        email.content = mail.Content(mail.MimeType.html, html_content)
        return email

    def send_email(self, email: mail.Mail) -> None:
        """Send a email to all recipients.

        Params:
        -------
        - email: Mail - The sendgrid email object to send.
        """
        self.sendgrid.send(email)


email_sender = EmailSender()
