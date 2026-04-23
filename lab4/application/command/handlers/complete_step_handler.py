from src.application.command.complete_step_command import CompleteStepCommand


class CompleteStepHandler:
    """Обработчик команды завершения шага"""

    def __init__(self, session_repository, notification_service):
        self._session_repository = session_repository
        self._notification_service = notification_service

    def handle(self, command: CompleteStepCommand):
        # 1. Получить сессию
        session = self._session_repository.find_by_id(command.session_id)
        if not session:
            raise ValueError(f"Сессия {command.session_id} не найдена")

        # 2. Завершить шаг (внутри проверяются инварианты)
        session.complete_step(command.step_number)

        # 3. Сохранить обновлённую сессию
        self._session_repository.save(session)

        # 4. Уведомление о завершении шага
        step_description = ""
        if session.recipe and command.step_number <= len(session.recipe.steps):
            step_description = session.recipe.steps[command.step_number - 1].description

        self._notification_service.notify(
            session.user.id if session.user else "unknown",
            f"✅ Шаг {command.step_number} завершён: {step_description}"
        )

        # 5. Если все шаги завершены — дополнительное уведомление
        if session.completed_steps and session.recipe:
            if len(session.completed_steps) == len(session.recipe.steps):
                self._notification_service.notify(
                    session.user.id if session.user else "unknown",
                    f"🎉 Поздравляем! Блюдо '{session.recipe.name}' готово!"
                )

        return session.get_events()
