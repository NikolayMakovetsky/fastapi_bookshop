from httpx import AsyncClient


# Independent tests
async def test_get_all_books(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/books/", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert len(res) > 0


async def test_existent_book(client: AsyncClient, global_headers, cookie_value):
    response = await client.get("/books/1", headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Мастер и Маргарита'


async def test_get_nonexistent_book(client: AsyncClient, global_headers, cookie_value):
    response = await client.get('/books/99', headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 404
    assert res == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_get_book_with_zero_id(client: AsyncClient, global_headers, cookie_value):
    response = await client.get('/books/0', headers=global_headers, cookies={'bookshop': cookie_value})
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == ''


# Script 1 --->
TEST_VARS = {}


async def test_add1_incorrect_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 999,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20
    }
    response = await client.post('/books/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'author_id': ['Значение не найдено в справочнике']},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_add2_incorrect_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 999,
        'price': 150.0,
        'qty': 20
    }
    response = await client.post('/books/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'genre_id': ['Значение не найдено в справочнике']},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_add3_incorrect_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 1,
        'price': -200,
        'qty': 20
    }
    response = await client.post('/books/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'price': ["Значение должно быть больше или равно '0'"]},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_add4_incorrect_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.945,
        'qty': 20
    }
    response = await client.post('/books/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'price': ['Значение должно содержать не более 10 цифр, включая 2 '
                             'цифры после запятой. Вами введено целое число: 150 и '
                             'десятичная часть: 945']},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_add_correct_book(client: AsyncClient, global_headers, cookie_value):
    global TEST_VARS
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20
    }
    response = await client.post('/books/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    TEST_VARS['book_id'] = res['id']
    TEST_VARS['author_id'] = res['author_id']
    TEST_VARS['genre_id'] = res['genre_id']
    assert response.status_code == 201
    assert res['title'] == 'Собачье сердце'


async def test_add_duplicate_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20
    }
    response = await client.post('/books/',
                                 headers=global_headers,
                                 cookies={'bookshop': cookie_value},
                                 json=user_data)
    res = response.json()
    assert response.status_code == 422
    assert res == {
        'errors': {'title': ['Значение должно быть уникальным']},
        'status': 422,
        'title': 'Ошибка проверки данных'
    }


async def test_update_nonexistent_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20
    }
    response = await client.put(f'/books/99',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 404
    assert res == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_update1_added_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Собачье сердце',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20,
        "row_version": 0
    }
    response = await client.put(f'/books/{TEST_VARS["book_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Собачье сердце'


async def test_update2_added_book(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Дни Турбиных',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20,
        "row_version": 1
    }
    response = await client.put(f'/books/{TEST_VARS["book_id"]}',
                                headers=global_headers,
                                cookies={'bookshop': cookie_value},
                                json=user_data)
    res = response.json()
    assert response.status_code == 200
    assert res['title'] == 'Дни Турбиных'


async def test_update_added_genre_with_old_row_version(client: AsyncClient, global_headers, cookie_value):
    user_data = {
        'title': 'Зойкина квартира',
        'author_id': 1,
        'genre_id': 1,
        'price': 150.0,
        'qty': 20,
        "row_version": 1
    }
    response = await client.put(f'/books/{TEST_VARS["book_id"]}',
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


async def test_delete_nonexistent_book(client: AsyncClient, global_headers, cookie_value):
    response = await client.delete(f'/books/99',
                                   headers=global_headers,
                                   cookies={'bookshop': cookie_value})
    assert response.status_code == 404
    assert response.json() == {'errors': {}, 'status': 404, 'title': 'Данные не найдены'}


async def test_delete_added_book(client: AsyncClient, global_headers, cookie_value):
    response = await client.delete(f'/books/{TEST_VARS["book_id"]}',
                                   headers=global_headers,
                                   cookies={'bookshop': cookie_value})
    assert response.status_code == 200
    assert response.json() == {}

# <---
