
from fastapi import FastAPI
from src.infrastructure.config.dependency_injection import setup_dependencies
from src.infrastructure.adapter.in.recipe_controller import setup_routes


def create_app() -> FastAPI:
    # Собираем зависимости
    deps = setup_dependencies()
    
    # Создаём приложение
    app = FastAPI(title="Recipe Generator", version="1.0.0")
    
    # Подключаем маршруты
    setup_routes(app, deps["generate_use_case"], deps["history_use_case"])
    
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
