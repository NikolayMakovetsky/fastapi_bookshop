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


USERNAME = "nik@ya.ru"
PASSWORD = "nik"

async def test_login():

    body_str = f'grant_type=password&username={USERNAME}&password={PASSWORD}&scope=&client_id=string&client_secret=string'

    headers = {
        "accept": "application/json",
        "accept-language": "ru-RU",
        "Content-Type": "application/x-www-form-urlencoded"
   }
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.post(f"{TEST_URL}/login", json=body_str, headers=headers)
    assert response.status_code == 204



# @pytest.mark.asyncio(forbid_global_loop=True)
async def test_existent_author3():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.get("/authors/1")
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Булгаков М.А.'


# @pytest.mark.asyncio(forbid_global_loop=True)
async def test_existent_genre():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.get("/genres/1")
    res = response.json()
    assert response.status_code == 200
    assert res['name_genre'] == 'Роман'


async def test_anonymous():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL + TEST_PREFIX
    ) as ac:
        response = await ac.get("/anonymous")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, Anonymous!'}

# @pytest.mark.asyncio(forbid_global_loop=True)
async def test_anonymous1():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL + TEST_PREFIX
    ) as ac:
        response = await ac.get("/anonymous")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, Anonymous!'}


# @pytest.mark.asyncio(forbid_global_loop=True)
async def test_existent_author2():
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.get("/authors/1")
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Булгаков М.А.'
