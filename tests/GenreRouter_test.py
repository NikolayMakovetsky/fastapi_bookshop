from httpx import AsyncClient


async def test_get_existent_genre(client: AsyncClient, cookie_value):
    response = await client.get("/genres/1", cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_genre'] == 'Роман'

