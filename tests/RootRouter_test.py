from httpx import AsyncClient


async def test_get_hello_world(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, world!'}


async def test_get_anonymous(client: AsyncClient):
    response = await client.get("/anonymous")
    assert response.status_code == 200
    assert response.json() == {'result': 'Hello, Anonymous!'}
