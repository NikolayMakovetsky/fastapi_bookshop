from httpx import AsyncClient


async def test_existent_book(client: AsyncClient, cookie_value):
    response = await client.get("/books/1", cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Мастер и Маргарита'


