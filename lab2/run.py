
from fastapi import FastAPI
from src.infrastructure.config.dependency_injection import setup_dependencies
from src.infrastructure.adapter.in.recipe_controller import setup_routes


def create_app() -> FastAPI:
    repository, ai_service = setup_dependencies()
    app = FastAPI(title="Recipe Generator", version="1.0.0")
    setup_routes(app, repository, ai_service)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
