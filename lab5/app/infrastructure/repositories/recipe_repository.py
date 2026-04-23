from sqlalchemy.orm import Session
from typing import List, Optional
import json

from app.domain.models.recipe import Recipe
from app.domain.value_objects.ingredient import Ingredient
from app.domain.value_objects.cooking_step import CookingStep
from app.infrastructure.db.models import RecipeModel
from app.application.port.out.recipe_repository import RecipeRepository


class PostgresRecipeRepository(RecipeRepository):
    def __init__(self, db_session: Session):
        self._db = db_session

    def save(self, recipe: Recipe) -> Recipe:
        model = self._db.query(RecipeModel).filter(RecipeModel.id == recipe.id).first()

        if model:
            model.name = recipe.name
            model.ingredients = [{"name": i.name, "expiry_date": str(i.expiry_date) if i.expiry_date else None} for i in recipe.ingredients]
            model.steps = [{"order": s.order, "description": s.description, "duration_minutes": s.duration_minutes} for s in recipe.steps]
            model.status = recipe.status.value
            model.source = recipe.source
            model.rating = recipe.rating
            model.updated_at = recipe.created_at
        else:
            model = RecipeModel(
                id=recipe.id,
                user_id=recipe.user_id,
                name=recipe.name,
                ingredients=[{"name": i.name, "expiry_date": str(i.expiry_date) if i.expiry_date else None} for i in recipe.ingredients],
                steps=[{"order": s.order, "description": s.description, "duration_minutes": s.duration_minutes} for s in recipe.steps],
                status=recipe.status.value,
                source=recipe.source,
                rating=recipe.rating
            )
            self._db.add(model)

        self._db.commit()
        self._db.refresh(model)
        return recipe

    def find_by_id(self, recipe_id: str) -> Optional[Recipe]:
        model = self._db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
        if not model:
            return None

        from app.domain.models.recipe import Recipe
        from app.domain.value_objects.ingredient import Ingredient
        from app.domain.value_objects.cooking_step import CookingStep
        from app.domain.value_objects.recipe_status import RecipeStatus

        ingredients = [Ingredient(
            name=i["name"],
            expiry_date=None  # упрощённо
        ) for i in model.ingredients]

        steps = [CookingStep(
            order=s["order"],
            description=s["description"],
            duration_minutes=s.get("duration_minutes")
        ) for s in model.steps]

        recipe = Recipe(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            ingredients=ingredients,
            steps=steps,
            source=model.source
        )
        recipe.status = RecipeStatus(model.status)
        recipe.rating = model.rating
        recipe.created_at = model.created_at
        return recipe

    def find_by_user_id(self, user_id: str) -> List[Recipe]:
        models = self._db.query(RecipeModel).filter(RecipeModel.user_id == user_id).all()
        return [self.find_by_id(m.id) for m in models if self.find_by_id(m.id)]
