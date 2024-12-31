from httpx import AsyncClient


async def test_get_some_user(client: AsyncClient, cookie_value, test_user_data):
    response = await client.get("/some_user", cookies={'bookshop': cookie_value})
    assert response.status_code == 200
    assert response.json() == {'result': f'Hello, {test_user_data["username"]}!'}


async def test_get_current_user(client: AsyncClient, cookie_value, test_user_data):
    response = await client.get("/current_user", cookies={'bookshop': cookie_value})
    assert response.status_code == 200
    assert response.json() == {'result': f'Hello, {test_user_data["username"]}!'}
