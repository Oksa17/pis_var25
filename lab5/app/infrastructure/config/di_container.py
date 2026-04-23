from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.infrastructure.repositories.recipe_repository import PostgresRecipeRepository
from app.infrastructure.adapters.out.email_notification_adapter import EmailNotificationAdapter
from app.application.service.recipe_application_service import RecipeApplicationService
from app.infrastructure.adapters.in.recipe_controller import setup_routes


def create_app() -> FastAPI:
    app = FastAPI(title="Recipe Generator", version="1.0.0")

    def get_service(db: Session = Depends(get_db)):
        recipe_repo = PostgresRecipeRepository(db)
        email_adapter = EmailNotificationAdapter()
        service = RecipeApplicationService(recipe_repo, email_adapter)
        return service

    setup_routes(app, get_service)

    return app


app = create_app()
