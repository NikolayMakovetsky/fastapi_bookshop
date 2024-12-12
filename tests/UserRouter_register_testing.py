import pytest
from fastapi import status
from httpx import AsyncClient

# https://github.com/fastapi-users/fastapi-users/blob/master/tests/conftest.py

from api import application
from . import TEST_URL


@pytest_asyncio.fixture
async def test_app_client(
        get_user_manager, get_test_client
) -> AsyncGenerator[httpx.AsyncClient, None]:
    register_router = get_register_router(
        get_user_manager,
        User,
        UserCreate,
    )


@pytest.mark.router
@pytest.mark.asyncio
class TestRegister:
    async def test_empty_body(self, test_app_client: AsyncClient):
        response = await test_app_client.post("/register", json={})
        assert response.status_code == status.HTTP_100_CONTINUE
