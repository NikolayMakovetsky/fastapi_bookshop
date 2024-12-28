import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


async def test_get_anonymous(client: AsyncClient):
    response = await client.get("/anonymous")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, Anonymous!'}


async def test_get_some_user(client: AsyncClient, kuki_value):
    response = await client.get("/some_user", cookies={'bookshop': kuki_value})
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, User!'}


async def test_get_current_user(client: AsyncClient, kuki_value):
    response = await client.get("/current_user", cookies={'bookshop': kuki_value})
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, Nikolay!'}
