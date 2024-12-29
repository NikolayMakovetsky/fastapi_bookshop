import time

import pytest
from httpx import AsyncClient

from api import application


@pytest.fixture(scope='session')
def app():
    yield application()


@pytest.fixture(scope='session')
def base_url():
    return 'http://127.0.0.1:8000'


@pytest.fixture(scope="module")
async def client(app, base_url):
    async with AsyncClient(app=app, base_url=base_url) as client:
        print("Test Client is ready")
        time.sleep(1)  # corresponds with engine parameter: pool_recycle=1 (database.py)
        yield client


@pytest.fixture(scope="module")
async def login_completed(client: AsyncClient, base_url):
    username = "nik@ya.ru"
    password = "nik"
    body_str = f'grant_type=password&username={username}&password={password}&scope=&client_id=string&client_secret=string'
    headers = {
            "accept": "application/json",
            "accept-language": "ru-RU",
            "Content-Type": "application/x-www-form-urlencoded"
    }
    print('Test logout is completed')
    response = await client.post(f"{base_url}/logout", json="", headers=headers)
    print(f'Test login for {username=}, {password=} is completed')
    response = await client.post(f"{base_url}/login", json=body_str, headers=headers)


@pytest.fixture(scope="module")
async def cookie_value(client: AsyncClient, login_completed):
    cookie_bookshop = client.cookies.get('bookshop')
    print('Test cookie name: bookshop')
    print('Test cookie value:', cookie_bookshop)
    yield cookie_bookshop


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
