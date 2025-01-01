from httpx import AsyncClient


# Independent tests
async def test_get_all_genres(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/genres/", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert len(res) > 0


async def test_get_existent_genre(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/genres/1", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_genre'] == 'Роман'


async def test_get_nonexistent_genre(client: AsyncClient, global_headers, cookie_value):
    response = await client.get('/genres/99', headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 404
    assert res == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_get_genre_with_zero_id(client: AsyncClient, global_headers, cookie_value):
    response = await client.get('/genres/0', headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['name_genre'] == ''


# Script 1 --->
TEST_VARS = {}

async def test_add_correct_genre(client: AsyncClient, global_headers, cookie_value):
    global TEST_VARS
    user_data = {"name_genre": "Fantasy"}
    response = await client.post('/genres/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    TEST_VARS['genre_id'] = res['id']
    assert response.status_code == 201
    assert res['name_genre'] == 'Fantasy'


async def test_add_duplicate_genre(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_genre": "Fantasy"}
    response = await client.post('/genres/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'name_genre': ['Значение должно быть уникальным']},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_update_nonexistent_genre(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_genre": "Fantasy",
                 "row_version": 0}
    response = await client.put(f'/genres/99',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 404
    assert res == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_update1_added_genre(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_genre": "Fantasy",
                 "row_version": 0}
    response = await client.put(f'/genres/{TEST_VARS["genre_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['name_genre'] == 'Fantasy'


async def test_update2_added_genre(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_genre": "Fantastic",
                 "row_version": 1}
    response = await client.put(f'/genres/{TEST_VARS["genre_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['name_genre'] == 'Fantastic'


async def test_update_added_genre_with_old_row_version(client: AsyncClient, global_headers, cookie_value):
    user_data = {"name_author": "Fairy tale",
                 "row_version": 1}
    response = await client.put(f'/genres/{TEST_VARS["genre_id"]}',
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


async def test_delete_nonexistent_genre(client: AsyncClient, global_headers, cookie_value):
    response = await client.delete(f'/genres/99',
                                   headers=global_headers,
                                   cookies={'bookshop': cookie_value})
    assert response.status_code == 404
    assert response.json() == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_delete_added_genre(client: AsyncClient, global_headers, cookie_value):
    response = await client.delete(f'/genres/{TEST_VARS["genre_id"]}',
                                   headers=global_headers,
                                   cookies={'bookshop': cookie_value})
    assert response.status_code == 200
    assert response.json() == {}

# <---
