import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def anyio_backend():
    return "asyncio"


async def test_get_existent_author(client: AsyncClient, kuki_value):
    response = await client.get("/authors/1", cookies={'bookshop': kuki_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Булгаков М.А.'


async def test_get_nonexistent_author(client: AsyncClient, kuki_value):
    response = await client.get('/authors/99', cookies={'bookshop': kuki_value})
    res = response.json()
    assert response.status_code == 404


async def test_get_author_with_zero_id(client: AsyncClient, kuki_value):
    response = await client.get('/authors/0', cookies={'bookshop': kuki_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == ''


# Petrov Petr --->
PETROV = {}


async def test_add_correct_author(client: AsyncClient, kuki_value):
    global PETROV
    user_data = {"name_author": "Petrov Petr"}
    response = await client.post('/authors/',
                                 cookies={'bookshop': kuki_value},
                                 json=user_data)
    res = response.json()
    PETROV = res
    assert response.status_code == 201
    assert res['name_author'] == 'Petrov Petr'


async def test_update_added_author(client: AsyncClient, kuki_value):
    user_data = {"name_author": "Petrov Petr123",
                 "row_version": 0}
    response = await client.put(f'/authors/{PETROV["id"]}',
                                cookies={'bookshop': kuki_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Petrov Petr123'

# async def test_delete_added_author(client: AsyncClient, kuki_value):
#     user_data = {"row_version": 1}
#     response = await client.delete(f'/authors/{PETROV["id"]}',
#                                    cookies={'bookshop': kuki_value},
#                                    json=user_data)
#     assert response.status_code == 200
#     assert response.json() == {}

# <--- Petrov Petr
