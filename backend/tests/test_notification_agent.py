from backend.agents.notification_agent import NotificationAgent

agent = NotificationAgent()

agent.notify(
    receiver_email="ayush.srinivasan09@gmail.com",
    report_path="backend/reports/abc123.pdf",
)

print("Notification sent.")