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
# app_test = application()
app_cooke = {'bookshop': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJleHAiOjE3MzQ4OTE5ODN9.sFSkQvrnS0wtWiZzy7oNs5nhMzLZhhgqXJpNquRXw2I'}


async def test_logout():

    headers = {
        "accept": "application/json",
        "accept-language": "ru-RU"
    }
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.post(f"{TEST_URL}/logout", json="", headers=headers)
    assert response.status_code in (204, 401)


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
    # app_cooke = dict(response.cookies)
    # assert app_cooke == {}
    assert response.status_code == 204


async def test_existent_book():
    headers = {
        "accept": "application/json",
        "accept-language": "ru-RU"
    }
    async with AsyncClient(
            transport=ASGITransport(app=application()), base_url=TEST_URL
    ) as ac:
        response = await ac.get("/books/1", headers=headers, cookies=app_cooke)
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Мастер и Маргарита'


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
