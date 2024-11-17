from pprint import pprint
from typing import Callable

from pydantic import BaseModel, ConfigDict


class BaseValidator:

    def __init__(self, x, session):
        self.x = x  # экземпляр валидационного класса
        self.rules = []  # rule содержит набор check-ов (функция, имя проверяемого поля, значение)
        self.errors = []
        self.is_valid = bool
        self.session = session


    def rule_for(self, property_name: str, property_name_func: Callable):
        """Создание правила для валидации:
        1. Добавление имени свойства
        2. Добавление значения этого свойства, которое требует валидации"""
        self.rules.append({"property_name": property_name, "property_value": property_name_func(self.x), "property_name_func": property_name_func, "checklist": []})
        return self

    def must(self, check_function):
        """3. Добавляется проверочная функция, которая должна вернуть: True или False
        Проверочных функций для одного свойства может быть несколько"""
        current_rules = self.rules[-1]
        checklist = current_rules["checklist"]
        checklist.append( {"check_function": check_function, "message": "Проверка не выполнена", "when_function": None})
        return self

    def message(self, message_name):
        """Работает в связке с must
        Сначала .must указываем, а эатем .message (чтобы задать выдаваемое сообщение при возникновении ошибки)"""
        current_rules = self.rules[-1]
        checklist = current_rules["checklist"]
        checklist[-1]["message"] = message_name
        return self

    def when(self, when_function):
        """Работает в связке с must
        При валидации добавляет условие при срабатывании которого нужно запускать проверку"""
        current_rules = self.rules[-1]
        checklist = current_rules["checklist"]
        checklist[-1]["when_function"] = when_function
        return self

    async def validate(self):
        """check_function должна принимать 3 параметра:
        x (schema)
        v (value) - значение которое будем валидировать
        s (session)"""
        # pprint(self.rules)

        for rule in self.rules:
            for check in rule["checklist"]:
                valid = await check["check_function"](rule["property_value"], self.session)
                if not valid:
                    self.errors.append({rule["property_name"]: check["message"]})
                    break
        # print(self.errors)

# class QSchema(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     title: str = ""
#     genre_id: int = 0
#     author_id: int = 0


if __name__ == '__main__':
    pass
        # book_validate_schema = QSchema()
        # book_validate_schema.title = "test"
        # book_validate_schema.genre_id = 3
        # book_validate_schema.author_id = 5
        # valid = BookValidator(book_validate_schema)
        # valid.validate()

