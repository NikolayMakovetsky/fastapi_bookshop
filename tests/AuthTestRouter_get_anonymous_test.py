import pytest
from httpx import ASGITransport, AsyncClient

from api import application
from api.routers import auth_test_router
from . import TEST_URL

TEST_PREFIX = auth_test_router.prefix

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return 'asyncio'  # 'trio'


async def test_anonymous():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL + TEST_PREFIX
    ) as ac:
        response = await ac.get("/anonymous")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, Anonymous!'}
