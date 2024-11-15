from fastapi.testclient import TestClient

from api.core.routes import genre_router

client =  TestClient(genre_router)

def test_get_genre_by_id_1():
    response = client.get("/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name_genre": "Роман",
        "user_created": 0,
        "date_created": "2024-10-29T19:30:25.771789Z",
        "row_version": 0
    }
