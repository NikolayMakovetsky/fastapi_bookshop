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
async def test_user_data(client: AsyncClient, base_url):
    data = {
        "email": "test@ya.ru",
        "password": "test_password",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "TestUserName"
    }

    response = await client.post(f"{base_url}/register", json=data)
    if response.status_code == 201:
        print('TestUser registered')
    elif response.status_code == 400 and response.json() == {"detail": "REGISTER_USER_ALREADY_EXISTS"}:
        print('TestUser already exists')
    else:
        print('Error: TestUser not received')

    return data


@pytest.fixture(scope="module")
async def login_completed(client: AsyncClient, base_url, test_user_data):
    username = test_user_data['email']
    password = test_user_data['password']
    body_str = f'grant_type=password&username={username}&password={password}&scope=&client_id=string&client_secret=string'
    headers = {
            "accept": "application/json",
            "accept-language": "ru-RU",
            "Content-Type": "application/x-www-form-urlencoded"
    }
    print('Test logout is completed')
    await client.post(f"{base_url}/logout", json="", headers=headers)
    print(f'Test login for {username=}, {password=} is completed')
    await client.post(f"{base_url}/login", json=body_str, headers=headers)


@pytest.fixture(scope="module")
async def cookie_value(client: AsyncClient, login_completed):
    cookie_bookshop = client.cookies.get('bookshop')
    print('Test cookie name: bookshop')
    print('Test cookie value:', cookie_bookshop)
    yield cookie_bookshop


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"
