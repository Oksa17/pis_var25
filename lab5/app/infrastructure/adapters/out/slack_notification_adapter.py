import os
import requests

from app.application.port.out.notification_port import NotificationPort


class SlackNotificationAdapter(NotificationPort):
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def notify(self, user_id: str, message: str) -> None:
        if not self.webhook_url:
            print("⚠️ Slack webhook не настроен")
            return

        try:
            response = requests.post(
                self.webhook_url,
                json={"text": f"👨‍🍳 Пользователь {user_id}: {message}"}
            )
            if response.status_code == 200:
                print(f"📢 Slack уведомление отправлено пользователю {user_id}")
            else:
                print(f"❌ Ошибка Slack: {response.status_code}")
        except Exception as e:
            print(f"❌ Ошибка отправки в Slack: {e}")
