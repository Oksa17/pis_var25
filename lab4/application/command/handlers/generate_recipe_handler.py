from src.domain.value_objects.ingredient import Ingredient
from src.domain.entities.user import User
from src.domain.aggregates.cooking_session import CookingSession
from src.application.command.generate_recipe_command import GenerateRecipeCommand
from src.application.service.notification_service import NotificationService


class GenerateRecipeHandler:
    """Обработчик команды генерации рецепта"""

    def __init__(self, user_repository, recipe_repository, notification_service):
        self._user_repository = user_repository
        self._recipe_repository = recipe_repository
        self._notification_service = notification_service

    def handle(self, command: GenerateRecipeCommand):
        # 1. Получить пользователя
        user = self._user_repository.find_by_id(command.user_id)
        if not user:
            raise ValueError(f"Пользователь {command.user_id} не найден")

        # 2. Валидация: не пустой список ингредиентов
        if not command.ingredient_names:
            raise ValueError("Нельзя генерировать рецепт без ингредиентов")

        # 3. Валидация: лимит запросов
        if not user.can_generate_recipe():
            raise ValueError(f"Превышен лимит запросов. Не более 10 в час")

        # 4. Создать Value Objects и проверить просрочку
        ingredients = [Ingredient(name=name) for name in command.ingredient_names]
        fresh_ingredients = [i for i in ingredients if i.is_available()]

        if not fresh_ingredients:
            raise ValueError("Все ингредиенты просрочены!")

        # 5. Создать агрегат и сгенерировать рецепт
        session = CookingSession()
        recipe = session.generate_recipe(user, fresh_ingredients)

        # 6. Сохранить рецепт
        self._recipe_repository.save(recipe)

        # 7. Отправить уведомление
        self._notification_service.notify(
            user.id,
            f"Рецепт '{recipe.name}' сгенерирован! Приятного аппетита!"
        )

        # 8. Вернуть события для публикации
        return session.get_events()
