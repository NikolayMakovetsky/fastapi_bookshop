## Работа с ORM
Pydantic поддерживает интеграцию с ORM (например, SQLAlchemy) для валидации и трансформации данных, полученных из базы данных.

Чтобы настроить модель для работы с ORM, используйте параметр ConfigDict с флагом from_attributes=True.

Пример:
```
from datetime import date
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    id: int
    name: str = 'John Doe'
    birthday_date: date

    config = ConfigDict(from_attributes=True)
```

## Работа с alembic (Миграции)

1. Устанавливаем alembic в окружение
```poetry add alembic```
2. Запускаем команду ```alimbic init migrations```
3. Изменяем файл alembic.ini 
```
# sqlalchemy.url = driver://user:pass@localhost/dbname
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s
```
4. Создаем файл с переменными окружения .env
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bookshop_db
DB_USER=postgres
DB_PASS=postgres
```
5. Создаем сonfig.py
```
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
```
6. Устанавливаем dotenv в окружение
```poetry add python-dotenv```
7. Работа с файлом migtations/env.py
```
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Устанавливаем правила передачи данных в файл alembic.ini
# Дописываем:
section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASS", DB_PASS)
...
# указываем ссылку на метаданные, которые "зашиты" в классе Base
target_metadata = Base.metadata
# target_metadata = None

```
8. Порядок передачи данных о переменных окружения ```.env -> config.py -> env.py -> alembic.ini```
9. Устанавливаем psycopg2 в окружение (Видимо миграции на нём работают)
```poetry add psycopg2```
10. Создаем бд bookshop_db2, используя pgAdmin
11. Создание первой миграции (получение скрипта на питоне)
```alembic revision --autogenerate -m "db creation"```
флаг --autogenerate позволит alembic-у сравнить текущее состояние базы данных и тех моделей,
которые у нас подклеены к metadata
Получаем в папке versions скрипт: 4adc220eddd8_db_creation.py
12. Проверка сгенерированного скрипта (добавляем создание и удаление схемы books)
```
def upgrade() -> None:
op.execute("create schema books")  # ADDED MANUALLY!
...

def downgrade() -> None:
...
op.execute("drop schema books")  # ADDED MANUALLY!
```
13. Проверяем, есть ли миграции привязанные к нашей БД, используя pgAdmin
```
bookshop_db2 -> Schemas -> public -> Tables -> alembic_version

Запускаем скрипт:
SELECT * FROM alembic_version; -> Total rows: 0 of 0 (Миграций пока не было)
```
13. Запуск скрипта
```
alembic upgrade <указание той ревизии, до которой мы хотим обновиться (номер хеша или head)>
alembic upgrade 4adc220eddd8
```
14. Смотрим результат в pgAdmin =)


##  FastapiUsers
1. Обновляем .toml файл (удаляем лишнее, устанавливаем fastapi users)
```poetry add fastapi-users[sqlalchemy]```
2. Запускаем тесты (или тестируем вручную)
Необходимо убидеться, что после обновления установленных библиотек проект остался в рабочем состоянии
3. Выбираем транспорт для нашего приложения (JWT)

[read about JSON Web Token here](https://jwt.io/introduction)

4. Добавляем и кастомизируем код из документации по FastapiUsers
