import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


async def test_get_hello_world(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, world!'}
