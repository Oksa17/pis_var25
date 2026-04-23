class NotificationService:
    """Сервис отправки уведомлений (интерфейс для команды)"""

    def notify(self, user_id: str, message: str) -> None:
        # Реальная реализация может отправлять email/push/SMS
        print(f"📧 Уведомление для {user_id}: {message}")
