from pprint import pprint
from typing import Callable

from pydantic import BaseModel, ConfigDict


class BaseValidator:

    def __init__(self, x, session):
        self.x = x  # экземпляр валидационного класса
        self.rules = []  # rule содержит набор check-ов (функция, имя проверяемого поля, значение)
        self.errors = {}
        self.is_valid = True
        self.session = session

    def rule_for(self, property_name: str, property_name_func: Callable):
        """Создание правила для валидации:
        1. Добавление имени свойства
        2. Добавление значения этого свойства, которое требует валидации"""
        self.rules.append({"property_name": property_name, "property_value": property_name_func(self.x),
                           "property_name_func": property_name_func, "checklist": []})
        return self

    def must(self, check_function):
        """3. Добавляется проверочная функция, которая должна вернуть: True или False
        Проверочных функций для одного свойства может быть несколько"""
        current_rules = self.rules[-1]
        checklist = current_rules["checklist"]
        checklist.append({"check_function": check_function, "message": "Проверка не выполнена", "when_function": None})
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

    def response_content(self):
        if self.is_valid:
            return None
        return {
            "title": "Ошибка проверки данных",
            "status": 422,
            "errors": self.errors
        }

    async def validate(self):
        """check_function должна принимать 3 параметра:
        x (schema)
        v (value) - значение которое будем валидировать
        s (session)"""

        for rule in self.rules:
            for check in rule["checklist"]:
                valid = await check["check_function"](rule["property_value"], self.session)
                if not valid:
                    msg_errors_array = self.errors.get(rule["property_name"], [])
                    if msg_errors_array:
                        msg_errors_array.append(check["message"])
                    else:
                        self.errors[rule["property_name"]] = [check["message"]]

                    self.is_valid = False
                    break


if __name__ == '__main__':
    pass
