import smtplib
from email.mime.text import MIMEText
import os

from app.application.port.out.notification_port import NotificationPort


class EmailNotificationAdapter(NotificationPort):
    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "smtp.mailtrap.io")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "2525"))
        self.smtp_user = os.getenv("EMAIL_USER")
        self.smtp_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = "noreply@recipe-generator.com"

    def notify(self, user_id: str, message: str) -> None:
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)

                msg = MIMEText(message)
                msg["Subject"] = "Рецепто-генератор"
                msg["From"] = self.from_email
                msg["To"] = f"user-{user_id}@example.com"

                server.send_message(msg)
                print(f"✉️ Email уведомление отправлено пользователю {user_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки email: {e}")
