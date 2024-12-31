from httpx import AsyncClient


# Independent tests
async def test_get_all_authors(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/authors/", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert len(res) > 0


async def test_get_existent_author(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/authors/1", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Булгаков М.А.'


async def test_get_nonexistent_author(client: AsyncClient, global_headers, cookie_value):
    response = await client.get('/authors/99', headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 404
    assert res == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_get_author_with_zero_id(client: AsyncClient, global_headers, cookie_value):
    response = await client.get('/authors/0', headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == ''


# Script 1 --->
TEST_VARS = {}

async def test_add_correct_author(client: AsyncClient, global_headers, cookie_value):
    global TEST_VARS
    user_data = {"name_author": "Petrov Petr"}
    response = await client.post('/authors/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    TEST_VARS['author_id'] = res['id']
    assert response.status_code == 201
    assert res['name_author'] == 'Petrov Petr'


async def test_add_duplicate_author(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_author": "Petrov Petr"}
    response = await client.post('/authors/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'name_author': ['Значение должно быть уникальным']},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_update_nonexistent_author(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_author": "Petrov Dmitry",
                 "row_version": 0}
    response = await client.put(f'/authors/99',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 404
    assert res == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_update1_added_author(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_author": "Petrov Dmitry",
                 "row_version": 0}
    response = await client.put(f'/authors/{TEST_VARS["author_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Petrov Dmitry'


async def test_update2_added_author(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_author": "Petrov Dmitry",
                 "row_version": 1}
    response = await client.put(f'/authors/{TEST_VARS["author_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['name_author'] == 'Petrov Dmitry'


async def test_update_added_author_with_old_row_version(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_author": "Petrov Ivan",
                 "row_version": 1}
    response = await client.put(f'/authors/{TEST_VARS["author_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 412
    assert res == {
        'errors': {},
        'status': 412,
        'title': 'Данные модифицированы другим пользователем'
    }


async def test_delete_nonexistent_author(client: AsyncClient, global_headers, cookie_value):
    response = await client.delete(f'/authors/99',
                                   headers=global_headers,
                                   cookies={'bookshop': cookie_value})
    assert response.status_code == 404
    assert response.json() == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_delete_added_author(client: AsyncClient, global_headers, cookie_value):
    response = await client.delete(f'/authors/{TEST_VARS["author_id"]}',
                                   headers=global_headers,
                                   cookies={'bookshop': cookie_value})
    assert response.status_code == 200
    assert response.json() == {}

# <---
