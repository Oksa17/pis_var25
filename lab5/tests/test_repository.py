import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.infrastructure.db.database import Base
from app.infrastructure.repositories.recipe_repository import PostgresRecipeRepository
from app.domain.models.recipe import Recipe
from app.domain.value_objects.ingredient import Ingredient
from app.domain.value_objects.cooking_step import CookingStep


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    yield Session()
    Base.metadata.drop_all(engine)


def test_save_and_find_recipe(db_session):
    repo = PostgresRecipeRepository(db_session)

    ingredients = [Ingredient(name="хлеб"), Ingredient(name="яйца")]
    steps = [CookingStep(order=1, description="Порезать хлеб")]

    recipe = Recipe(
        user_id="user-1",
        name="Гренки",
        ingredients=ingredients,
        steps=steps
    )

    repo.save(recipe)
    found = repo.find_by_id(recipe.id)

    assert found is not None
    assert found.name == "Гренки"
    assert len(found.ingredients) == 2
