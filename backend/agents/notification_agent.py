from backend.services.email_services import EmailService


class NotificationAgent:
    """
    Sends AI review reports to developers.
    """

    def __init__(self):
        self.email_service = EmailService()

    def notify(
        self,
        receiver_email: str,
        report_path: str,
    ):
        """
        Send notification email.
        """

        self.email_service.send_email(
            receiver_email=receiver_email,
            subject="AI Code Review Report",
            body="Please find the attached AI Code Review Report.",
            attachment_path=report_path,
        )