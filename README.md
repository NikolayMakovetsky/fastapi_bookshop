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

