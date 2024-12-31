from httpx import AsyncClient


async def test_existent_book(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/books/1", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Мастер и Маргарита'


