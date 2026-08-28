from unittest.mock import patch

from backend.agents.notification_agent import NotificationAgent


def test_notification_agent():

    agent = NotificationAgent()

    with patch(
        "backend.agents.notification_agent.EmailService.send_email"
    ) as mock_send:

        agent.notify(
            receiver_email="test@example.com",
            report_path="backend/reports/abc123.pdf",
        )

        mock_send.assert_called_once_with(
            receiver_email="test@example.com",
            subject="AI Code Review Report",
            body="Please find the attached AI Code Review Report.",
            attachment_path="backend/reports/abc123.pdf",
        )