import pytest
from httpx import ASGITransport, AsyncClient

from api import application
from . import TEST_URL

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return 'asyncio'  # 'trio'


async def test_get_hello_world():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, world!'}
