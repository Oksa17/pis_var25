from src.domain.aggregates.cooking_session import CookingSession
from src.application.command.start_cooking_command import StartCookingCommand


class StartCookingHandler:
    """Обработчик команды начала готовки"""

    def __init__(self, recipe_repository, session_repository, notification_service):
        self._recipe_repository = recipe_repository
        self._session_repository = session_repository
        self._notification_service = notification_service

    def handle(self, command: StartCookingCommand):
        # 1. Получить рецепт
        recipe = self._recipe_repository.find_by_id(command.recipe_id)
        if not recipe:
            raise ValueError(f"Рецепт {command.recipe_id} не найден")

        # 2. Валидация: рецепт принадлежит пользователю
        if recipe.user_id != command.user_id:
            raise ValueError("Нельзя начать готовку чужого рецепта")

        # 3. Валидация: длительность положительная
        if command.estimated_minutes <= 0:
            raise ValueError("Длительность приготовления должна быть положительной")

        # 4. Создать сессию и начать готовку
        session = CookingSession()
        session.start_cooking(recipe, command.estimated_minutes)

        # 5. Сохранить сессию
        self._session_repository.save(session)

        # 6. Отправить уведомление
        self._notification_service.notify(
            command.user_id,
            f"Начинаем готовить '{recipe.name}'! ⏰ {command.estimated_minutes} минут"
        )

        return session.get_events()
