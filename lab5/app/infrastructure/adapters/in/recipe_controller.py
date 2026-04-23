from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional

from app.application.service.recipe_application_service import RecipeApplicationService


class GenerateRecipeRequest(BaseModel):
    ingredient_names: List[str] = Field(..., min_length=1, max_length=20)

class StartCookingRequest(BaseModel):
    estimated_minutes: int = Field(..., gt=0, le=1440)

class RateRecipeRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)


def setup_routes(app: FastAPI, service: RecipeApplicationService):
    @app.post("/api/recipes/generate")
    async def generate_recipe(request: GenerateRecipeRequest, user_id: str = "user-123"):
        try:
            events = service.generate_recipe(user_id, request.ingredient_names)
            return {"message": "Рецепт сгенерирован", "events": [type(e).__name__ for e in events]}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/recipes/{recipe_id}/start")
    async def start_cooking(recipe_id: str, request: StartCookingRequest, user_id: str = "user-123"):
        try:
            events = service.start_cooking(recipe_id, user_id, request.estimated_minutes)
            return {"message": "Готовка начата", "events": [type(e).__name__ for e in events]}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/sessions/{session_id}/step/{step_number}")
    async def complete_step(session_id: str, step_number: int):
        try:
            events = service.complete_step(session_id, step_number)
            return {"message": f"Шаг {step_number} завершён", "events": [type(e).__name__ for e in events]}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/api/recipes/{recipe_id}/rate")
    async def rate_recipe(recipe_id: str, request: RateRecipeRequest, user_id: str = "user-123"):
        try:
            service.rate_recipe(recipe_id, user_id, request.rating)
            return {"message": f"Рецепт оценён на {request.rating}★"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/api/recipes/{recipe_id}")
    async def get_recipe(recipe_id: str):
        recipe = service.get_recipe_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Рецепт не найден")
        return recipe

    @app.get("/api/users/{user_id}/history")
    async def get_user_history(user_id: str, limit: int = 10, offset: int = 0):
        history = service.get_user_history(user_id, limit=limit, offset=offset)
        return history
