import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


async def test_existent_book(client: AsyncClient, kuki_value):
    headers = {
        "accept": "application/json",
        "accept-language": "ru-RU"
    }
    response = await client.get("/books/1", headers=headers, cookies={'bookshop': kuki_value})
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Мастер и Маргарита'


