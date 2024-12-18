from fastapi.testclient import TestClient

from api import application
from api.routers import author_router
from . import TEST_URL

TEST_PREFIX = author_router.prefix
client = TestClient(application())


# def test_author_with_null_id():
#     response = client.get(f"{TEST_URL}{TEST_PREFIX}/0")
#     assert response.status_code == 200
#     assert response.json() == {"Hello": "World"}


def test_existent_author():
    response = client.get(f"{TEST_URL}{TEST_PREFIX}/1")
    assert response.status_code == 200
    assert response.json() == {
         'date_created': '2024-11-12T16:51:14.285878Z',
         'date_modified': None,
         'id': 1,
         'name_author': 'Булгаков М.А.',
         'row_version': 0,
         'user_created': 0,
         'user_modified': None
    }


# def test_non_existent_author():
#     response = client.get(f"{TEST_URL}{TEST_PREFIX}/999")
#     assert response.status_code == 200
#     assert response.json() == {"Hello": "World"}


