import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


async def test_get_existent_author(client: AsyncClient, kuki_value):
    response = await client.get("/authors/1", cookies={'bookshop': kuki_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Булгаков М.А.'

