from fastapi.testclient import TestClient
from app.infrastructure.config.di_container import app

client = TestClient(app)


def test_generate_recipe():
    response = client.post(
        "/api/recipes/generate",
        json={"ingredient_names": ["хлеб", "яйца", "молоко"]},
        params={"user_id": "user-1"}
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_recipe_not_found():
    response = client.get("/api/recipes/non-existent-id")
    assert response.status_code == 404
