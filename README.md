
https://luciopaiva.com/markdown-toc/

# BookShopAPI v.1.0 «Магазин книг»

## Общая информация
API-интерфейс интернет-магазина книг, реализованный в соответствии с принципами REST.

Приложение разработано на FastApi с использованием базы данных PostgreSQL и
ORM SQLAlchemy в асинхронной реализации. 
Простая удобная структура проекта позволит легко масштабировать его, в случае необходимости.
Аутентификация реализована на базе библиотеки FastApiUsers, с использованием
Cookie и JWT-токена.

Для создания структуры таблиц и загрузки данных использвется библиотека alembic.

В проекте разработан универсальный механизм проверки данных, который позволяет
создавать "карту валидации" любой сложности для заданной Pydantic-схемы и выполнять проверку.
Все сообщения сервера, включая валидационные, выдаются
с учетом языка локализации (ru, en).

Тестирование роутеров реализовано с использованием библиотеки pytest.
Каждый роутер проверяется набором асинхронных тестовых функций.

## Оглавление:


- [Tech stack](#tech-stack)
- [Run the app using Terminal](#run-the-app-using-terminal)
- [Project structure](#project-structure)
- [class Server for FastApi app](#class-server-for-fastapi-app)
- [Work with PostgreSQL database](#work-with-postgresql-database)
  - [Database schema](#database-schema)
  - [Database creation](#database-creation)
  - [Migrations start - filling in the database](#migrations-start---filling-in-the-database)
- [Authentication](#authentication)
- [Server messages localization](#server-messages-localization)
- [Validation](#validation)
  - [How to create validation map for instance](#how-to-create-validation-map-for-instance)
- [Reports](#reports)
- [References](#references)


## Tech stack

- Python, Poetry, PostgreSQL, FastApi, Alembic, SQLAlchemy, Pydantic, FastApiUsers

## Run the app using Terminal
1. Установите Питон 3.11 командой
2. Установите Poetry командой ```poetry install```

Подготовка тестовой БД
1. Создайте базу данных
2. Настройте файл .env, 
2. Проведите миграции


1. Создайте папку
2. Скачайте проект на свой ПК
2. создать виртуальное poetry окружение
3. Установите необходимые библиотеки в ВО командой
4. Запустите файл ```api/__init__.py```


## Project structure

Структура проекта представляет собой набор пакетов,
ключевые файлы которого вынесены в папку ```api/core```:
```
api/core
├── localizators
├── logging
├── resources
├── routes
├── validators
└── server.py
```

## class Server for FastApi app
Для удобной работы с приложением FastAPI, а также
для создания единой точки регистрации роутеров,
используется класс Server.
```
api/core/server.py

class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)
```

## Work with PostgreSQL database

### Database schema

![shopdb](img/shopdb.jpg)

### Database creation
1. Установите СУБД PostrgreSQL (Postrges PRO)

[Загрузить Postgres PRO](https://postgrespro.ru/products/download)

2. Установите pgAdmin — платформу для администрирования и настройки СУБД PostgreSQL

[Загрузить pgAdmin](https://www.pgadmin.org/download/)

3. Подготовка pgAdmin к работе
- Создайте сервер, например ```Postgres Pro 14 (64bit)```

![servers](img/pgadmin_servers.jpg)

- Задайте имя пользователя, например ```postgres```
- Задайте пароль, например ```postgres```
- Подключитесь к серверу

![connection](img/connect_to_server.jpg)

- Создайте базу данных, например ```bookshop_db2```

![create_db](img/create_database.jpg)



### Migrations start - filling in the database
1. Общая информация

Миграционные файлы с необходимыми для библиотеки alembic
инструкциями по добавлению схем, а также
созданию и заполнению таблиц, находятся в папке:
```./migrations/versions```

![migrations](img/migrations.jpg)

Каждая таблица создается и инициализируется отдельным
миграционным файлом, что позволяет
при необходимости удобно вносить изменения.


К важным миграционным файлам также относятся:
- .env (ключевой файл, из которого извлекается информация
о базе данных, как для проведения миграций,
так и для подключения к ней при запуске приложения)

![env](img/env.jpg)
- config.py
- alembic.ini

2. Перед запуском миграций, необходимо:
- Убедиться, что создана пустая база данных PostgreSQL
- Убедиться, что создано и инициализировано виртуальное
окружение проекта (в том числе установлена библиотека
alembic)
- Убедиться, что в файле ```.env``` указана верная информация
о базе данных

3. Запуск миграций

Для запуска необходимо в терминале перейти в папку проекта
и выполнить команду ```alembic upgrade head```

![alembic_upgrade](img/alembic_upgrade.jpg)

После успешного завершения процесса необходимо открыть
pgAdmin и убедиться, что в базу данных успешно добавлены
схемы, таблицы и данные, согласно миграционным файлам.

![bookshopdb2](img/pgadmin_bookshopdb2.jpg)

Чтобы увидеть созданные таблицы, перейдите в схему,
например ```books```, и выберите ```Tables```

Чтобы увидеть данные таблиц, щелкните правой кнопкой мыши
по названию базы данных ```bookshop_db2``` и выберите пункт
```Query Tool```. В открывшемся окне ```Query``` напишите
любой запрос на выборку данных, например ```select * from books.book```
и нажмите кнопку ```Execute script (F5)```

![select_from_db](img/select_from_db.jpg)

После завершения инициализации базы данных
приложение готово к работе.

## Authentication
```./auth```

Аутентификация пользователей
реализована при помощи FastApiUsers.
- Database adapter: SQLAlchemy
- Transport: Cookie
- Strategy: JWT


## Logging
```api/core/logging```

Для корректной работы логирования необходимо добавить в корень проекта папку ```.log```

Настройка параметров логирования осуществляется в специальном конфигурационном файле.
```
api/core/logging/log_config

'formatters'    - форматы логирования
'handlers'      - настройки обработчиков потоков логирования
'loggers'       - настройки отслеживаемых логгеров
```

## Server messages localization
```api/core/localizators```
### Server errors localization
```
api/core/localizators

Функция validation_problem
при передаче ей двух параметров: (lang: str, status: int) 

```
### Validation errors localization
```
api/core/localizators/localizator.py

def get_localize_text - возвращает
```

## Dependency injection
для добавления accept-language во все роутеры 


## Testing
```./tests```

Тестирование роутеров осуществляется
при помощи библиотеки ```pytest```

Фикстуры, запускаемые перед началом процесса
тестирования, описаны в файле ```tests/conftest.py```

```
@pytest.fixtures:

anyio_backend       - осуществляет настройку библиотеки pytest
app                 - возвращает ссылку на приложение
base_url            - возвращает базовый url на котором запускается приложение
client              - возвращает асинхронного тестового клиента
test_user_data      - регистрирует тестового клиента и возвращает его описание
global_headers      - возвращает заголовки для роутеров
login_completed     - осуществляет вход (login) для тестового клиента
cookie_value        - возвращает значение cookie, необходимое для запуска роутеров
```


## Validation
class BaseValidator - это универсальный класс, который позволяет создавать карты валидации
(наборы правил проверки) для различных экземпляров pydantic-моделей, а также осуществлять
валидацию в соответствии с этими картами валидации.
```
BaseValidator.py

class BaseValidator:
    def __init__(self, item, session):
        self.item = item            - объект pydantic-модели
        self.rules = []             - список правил проверки для полей объекта item
        self.errors = {}            - список ошибок, выявленных в процессе валидации
        self.is_valid = True        - флаг, отражающий общий результат проверки
        self.session = session      - текущая сессия (необходима для запуска 
                                                      условных и проверочных функций)

-------------------------------------------------------
Структура self.rules:
[
    {
        "property_name": property_name_1,
        "property_value": property_name_func(self.item),
        "property_name_func": property_name_func,
        "checklist":
         [
            {
            "check_function": check_function_1,
            "message": "Data validation failed",
            "when_function": None,
            "msg_params": {}
            }
            {
            "check_function": check_function_2,
            "message": "Data validation failed",
            "when_function": None,
            "msg_params": {}
            }
            ...            
        ]
    },
    {
        "property_name": property_name_2
        ...
    }
    ...
]
-------------------------------------------------------

    def rule_for            - добавляет в self.rules валидационное правило для поля объекта self.item
    
    def must                - добавляет в self.rules проверочную функцию ("check_function")
                              для валидационного правила
                              Для каждого правила можно добавлять любое к-во проверочных функций.
                              В качестве проверочных функций могут выступать как специфические
                              пользовательские функции, так и типовые методы класса BaseValidator:
                              is_empty, is_not_empty...is_in_enum, matches (см.ниже)
                              
    def message             - добавляет в self.rules
                              для конкретной проверочной функции ("check_function")
                              сообщение ("message") об ошибке валидации (опционально)
                              Если данную функцию не использовать, то в случае возникновения
                              ошибки валидации будет выведено сообщение по умолчанию
                              
    def when                - добавляет в self.rules
                              для конкретной проверочной функции ("check_function")
                              условную функцию ("when_function") (опционально)
                              Если результат выполнения условной функции True - проверочная 
                              функция будет выполнена, в противном случае проверочная функция
                              будет игнорироваться
                              
    def response_content    - формирует структуру ошибки валидации для её последующего
                              добавления в self.errors
                              {
                                  "title": "Data validation error",
                                  "status": 422,
                                  "errors": self.errors
                              }
    
    async def validate      - асинхронный метод, запускающий процесс валидации
                              в соответствии со сформированной картой валидации
    
    Типовые проверочные методы (для передачи в def must):
    
    def is_empty
    def is_not_empty
    def is_null
    def is_not_null
    def equal
    def not_equal
    def greater_than
    def greater_than_or_equal
    def less_than
    def less_than_or_equal
    def maximum_length
    def minimum_length
    def exclusive_between
    def inclusive_between
    def length
    def precision_scale
    def is_in_enum
    def matches

```
### How to create validation map for instance

Пример создания карты валидации для конкретного объекта

class AuthorValidator(BaseValidator) - это класс, создающий карту валидации
(набор правил проверки) для конкретной pydantic-модели (Author)
```
AuthorValidator.py

class AuthorValidator(BaseValidator):
    def __init__(self, item: AuthorValidateSchema, session, lang: str):
        super().__init__(item, session)
        self.rule_for("name_author", lambda x: x.name_author) \
            .must(is_unique_name_author) \
            .message(_(lang, "ERR_UniqueValue"))
```

Обратите внимание, что методы rule_for, must, message, when возвращают self,
благодаря чему мы можем записывать их друг за другом через точку,
формируя таким образом нашу карту валидации.

```
Примеры использования:

self.rule_for().must()
self.rule_for().must().message()
self.rule_for().must().message().when()
self.rule_for().must().message().must().message()
self.rule_for().must().message().when().must().message().when()
```

На первом месте всегда стоит rule_for. Он определяет поле объекта, которое мы будем валидировать.
На втором месте всегда стоит must. Он задает проверочную функцию для поля нашего объекта.
Метод message добавляется опционально (рекомендуется)
если мы хотим кастомизировать текст сообщения об ошибке.
Метод when добавляется опционально если мы хотим добавить условие запуска проверочной функции.

Важно!
Количество функций must может быть любым. Таким образом, мы можем задавать любое число проверок
для поля нашего объекта.

```
Пример:

self.rule_for().must().must().must()
```
В этом случае, при запуске валидации, мы для поля ХХ выполним 3 различные проверки.
При этом будут использоваться сообщения об ошибках по умолчанию.

Рекомендуется после каждой функции must вызывать функцию message.
Это позволит получать точную информацию о возникшей ошибке валидации.
```
Пример:

self.rule_for().must().message().must().message().must().message()
```

Для того, чтобы в роутере осуществить валидационную проверку нашего объекта
достаточно создать экземпляр класса AuthorValidator и вызвать
асинхронный метод validate()
```
AuthorRouter.py

            validator = AuthorValidator(author, session, lang)
            await validator.validate()
```


## Reports

## References
- https://www.python.org/doc/
- https://python-poetry.org/docs/
- https://fastapi.tiangolo.com
- https://fastapi.qubitpi.org/tutorial/
- https://docs.sqlalchemy.org/en/20/
- https://postgrespro.ru/
- https://www.pgadmin.org
- https://alembic.sqlalchemy.org/en/latest/index.html
- https://docs.pydantic.dev/latest/
- https://fastapi-users.github.io/fastapi-users/latest/

