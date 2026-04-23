from src.application.command.rate_recipe_command import RateRecipeCommand


class RateRecipeHandler:
    """Обработчик команды оценки рецепта"""

    def __init__(self, recipe_repository, notification_service):
        self._recipe_repository = recipe_repository
        self._notification_service = notification_service

    def handle(self, command: RateRecipeCommand):
        # 1. Получить рецепт
        recipe = self._recipe_repository.find_by_id(command.recipe_id)
        if not recipe:
            raise ValueError(f"Рецепт {command.recipe_id} не найден")

        # 2. Валидация: оценка от 1 до 5
        if not 1 <= command.rating <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")

        # 3. Валидация: рецепт должен быть завершён
        if recipe.status.value != "завершён":
            raise ValueError(f"Нельзя оценить рецепт в статусе {recipe.status.value}")

        # 4. Добавить оценку
        recipe.add_rating(command.rating)

        # 5. Сохранить рецепт
        self._recipe_repository.save(recipe)

        # 6. Уведомление
        stars = "★" * command.rating + "☆" * (5 - command.rating)
        self._notification_service.notify(
            recipe.user_id,
            f"Рецепт '{recipe.name}' получил оценку {stars} ({command.rating}/5)"
        )

        return None  # события не генерируются
