import os
import smtplib

from email.message import EmailMessage

from backend.config import settings
from backend.utils.logger import logger


class EmailService:
    """
    Handles email notifications.
    """

    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.email = settings.smtp_email
        self.password = settings.smtp_password

    def send_email(
        self,
        receiver_email: str,
        subject: str,
        body: str,
        attachment_path: str,
    ):
        """
        Send email with PDF attachment.
        """

        try:

            message = EmailMessage()

            message["Subject"] = subject
            message["From"] = self.email
            message["To"] = receiver_email

            message.set_content(body)

            with open(attachment_path, "rb") as file:
                message.add_attachment(
                    file.read(),
                    maintype="application",
                    subtype="pdf",
                    filename=os.path.basename(attachment_path),
                )

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:

                smtp.starttls()

                smtp.login(self.email, self.password)

                smtp.send_message(message)

            logger.info("Email sent successfully.")

        except Exception as e:
            logger.exception(e)
            raise