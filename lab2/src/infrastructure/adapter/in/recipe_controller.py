from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


class GenerateRecipeRequest(BaseModel):
    ingredient_names: List[str]


def setup_routes(app: FastAPI, repository, ai_service):
    @app.post("/api/recipes/generate")
    async def generate_recipe(request: GenerateRecipeRequest, user_id: str = "user-123"):
        try:
            # TODO: вызвать use case
            return {"id": "123", "name": "Гренки", "steps": ["1. Порежь", "2. Обжарь"]}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
