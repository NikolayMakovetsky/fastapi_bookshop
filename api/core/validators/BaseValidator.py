import re
from typing import Callable, Any


class BaseValidator:

    def __init__(self, item, session):
        self.item = item  # экземпляр валидационного класса
        self.rules = []  # rule содержит набор check-ов (функция, имя проверяемого поля, значение)
        self.errors = {}
        self.is_valid = True
        self.session = session

    def rule_for(self, property_name: str, property_name_func: Callable):
        """Создание правила для валидации:
        1. Добавление имени свойства
        2. Добавление значения этого свойства, которое требует валидации"""
        self.rules.append({"property_name": property_name, "property_value": property_name_func(self.item),
                           "property_name_func": property_name_func, "checklist": []})
        return self

    def must(self, check_function: Callable):
        """3. Добавляется проверочная функция, которая должна вернуть: True или False
        Проверочных функций для одного свойства может быть несколько
        checking func should take 3 params:item(schema),value,session and return True(Success)/False)
        """
        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append({"check_function": check_function, "message": "Data validation failed", "when_function": None,
                          "msg_params": {}})
        return self

    def message(self, message_name: str):
        """Работает в связке с must
        Сначала .must указываем, а эатем .message (чтобы задать выдаваемое сообщение при возникновении ошибки)"""

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        msg_params = checklist[-1]["msg_params"]

        for k, v in msg_params.items():
            key_in_brackets = "{" + k + "}"
            if key_in_brackets in message_name:
                message_name = message_name.replace(key_in_brackets, f"{v}")

        checklist[-1]["message"] = message_name
        return self

    def when(self, when_function: Callable):
        """Работает в связке с must
        При валидации добавляет условие при срабатывании которого нужно запускать проверку"""
        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist[-1]["when_function"] = when_function
        return self

    def response_content(self):
        if self.is_valid:
            return None
        return {
            "title": "Data validation error",
            "status": 422,
            "errors": self.errors
        }

    def is_empty(self):

        async def check_function(item, value: Any, session) -> bool:
            if not value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {"check_function": check_function,
             "message": "The field must be empty",
             "when_function": None,
             "msg_params": {}})
        return self

    def is_not_empty(self):

        async def check_function(item, value: Any, session) -> bool:
            if value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {"check_function": check_function,
             "message": "The field must not be empty",
             "when_function": None,
             "msg_params": {}})
        return self

    def is_null(self):

        async def check_function(item, value: Any, session) -> bool:
            if value is None:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {"check_function": check_function,
             "message": "The value must be null",
             "when_function": None,
             "msg_params": {}})
        return self

    def is_not_null(self):

        async def check_function(item, value: Any, session) -> bool:
            if value is not None:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {"check_function": check_function,
             "message": "The value must not be null",
             "when_function": None,
             "msg_params": {}})
        return self

    def equal(self, comparison_value: Any):

        async def check_function(item, value: Any, session) -> bool:
            if value == comparison_value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be equal to '{comparison_value}'",
                "when_function": None,
                "msg_params": {"comparison_value": comparison_value}
            }
        )
        return self

    def not_equal(self, comparison_value: Any):

        async def check_function(item, value: Any, session) -> bool:
            if value != comparison_value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must not be equal to '{comparison_value}'",
                "when_function": None,
                "msg_params": {"comparison_value": comparison_value}
            }
        )
        return self

    def greater_than(self, comparison_value: int | float):

        async def check_function(item, value: int | float, session) -> bool:

            if not isinstance(value, (int, float)):
                return True

            if value > comparison_value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be greater than '{comparison_value}'",
                "when_function": None,
                "msg_params": {"comparison_value": comparison_value}
            }
        )
        return self

    def greater_than_or_equal(self, comparison_value: int | float):

        async def check_function(item, value: int | float, session) -> bool:

            if not isinstance(value, (int, float)):
                return True

            if value >= comparison_value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be greater than or equal to '{comparison_value}'",
                "when_function": None,
                "msg_params": {"comparison_value": comparison_value}
            }
        )
        return self

    def less_than(self, comparison_value: int | float):

        async def check_function(item, value: int | float, session) -> bool:

            if not isinstance(value, (int, float)):
                return True

            if value < comparison_value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be less than '{comparison_value}'",
                "when_function": None,
                "msg_params": {"comparison_value": comparison_value}
            }
        )
        return self

    def less_than_or_equal(self, comparison_value: int | float):

        async def check_function(item, value: int | float, session) -> bool:

            if not isinstance(value, (int, float)):
                return True

            if value <= comparison_value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be less than or equal to '{comparison_value}'",
                "when_function": None,
                "msg_params": {"comparison_value": comparison_value}
            }
        )
        return self

    def maximum_length(self, max_length: int):
        total_length = 0
        if isinstance(self.rules[-1]["property_value"], str):
            total_length = len(self.rules[-1]["property_value"])

        async def check_function(item, value: str, session) -> bool:
            if not isinstance(value, str):
                return True
            if len(value) < max_length:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be {max_length} characters or fewer. You entered {total_length} characters.",
                "when_function": None,
                "msg_params": {"max_length": max_length, "total_length": total_length}
            }
        )
        return self

    def minimum_length(self, min_length: int):
        total_length = 0
        if isinstance(self.rules[-1]["property_value"], str):
            total_length = len(self.rules[-1]["property_value"])

        async def check_function(item, value: str, session) -> bool:
            if not isinstance(value, str):
                return True
            if len(value) >= min_length:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be at least {min_length} characters. You entered {total_length} characters.",
                "when_function": None,
                "msg_params": {"min_length": min_length, "total_length": total_length}
            }
        )
        return self

    def exclusive_between(self, min_val: int | float, max_val: int | float):
        property_value = self.rules[-1]["property_value"]

        async def check_function(item, value: int | float, session) -> bool:

            if not isinstance(value, (int, float)):
                return True
            if min_val < value < max_val:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be between {min_val} and {max_val} (exclusive). You entered {property_value}",
                "when_function": None,
                "msg_params": {"min_val": min_val, "max_val": max_val, "property_value": property_value}
            }
        )
        return self

    def inclusive_between(self, min_val: int | float, max_val: int | float):
        property_value = self.rules[-1]["property_value"]

        async def check_function(item, value: int | float, session) -> bool:

            if not isinstance(value, (int, float)):
                return True
            if min_val <= value <= max_val:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be between {min_val} and {max_val} (inclusive). You entered {property_value}",
                "when_function": None,
                "msg_params": {"min_val": min_val, "max_val": max_val, "property_value": property_value}
            }
        )
        return self

    def length(self, min_len: int, max_len: int):

        async def check_function(item, value: str, session) -> bool:

            if not isinstance(value, str):
                return True
            if min_len <= len(value) <= max_len:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must be between {min_len} and {max_len} characters",
                "when_function": None,
                "msg_params": {"min_len": min_len, "max_len": max_len}
            }
        )
        return self

    def precision_scale(self, expected_precision: int, expected_scale: int):
        """function checks if float value could be correctly insert into database field with type 'decimal' e.g.
        Example for precision_scale(6, 2):
            1234.56 -> OK
            34.56 -> OK
            123.456789 -> FAIL
            123.46 -> OK
            123.4 -> OK
            123.0 -> OK
            """
        digits, actual_scale = "", ""
        if isinstance(self.rules[-1]["property_value"], float):
            property_value = str(self.rules[-1]["property_value"])
            digits, actual_scale = property_value.split(".")
            if len(actual_scale) < expected_scale:
                actual_scale = (actual_scale + ('0' * expected_scale))[:expected_scale]

        async def check_function(item, value: float, session) -> bool:
            if not isinstance(value, float):
                return True
            if len(digits + actual_scale) <= expected_precision and len(actual_scale) == expected_scale:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value must not be more than {expected_precision} digits in total, "
                           f"with allowance for {expected_scale} decimals. "
                           f"{digits} digits and {actual_scale} decimals were found.",
                "when_function": None,
                "msg_params": {"expected_precision": expected_precision,
                               "expected_scale": expected_scale,
                               "digits": digits,
                               "actual_scale": actual_scale}
            }
        )
        return self

    def is_in_enum(self, enum: list | tuple):

        async def check_function(item, value: Any, session) -> bool:
            if value in enum:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value is not in the specified range",
                "when_function": None,
                "msg_params": {}
            }
        )
        return self

    def matches(self, regex: str):  # 8\(\d{3}\)\d{3}-\d{2}-\d{2}  ->  8(495)111-22-33

        async def check_function(item, value: str, session) -> bool:
            if not isinstance(value, str):
                return True

            res = re.match(regex, value)
            if res:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append(
            {
                "check_function": check_function,
                "message": f"The value is not in the correct format",
                "when_function": None,
                "msg_params": {}
            }
        )
        return self

    async def validate(self):
        """Method that runs validation process"""
        for rule in self.rules:
            for check in rule["checklist"]:
                when_res = True
                if check["when_function"]:
                    when_res = await check["when_function"](self.item, rule["property_value"], self.session)
                if when_res:
                    valid = await check["check_function"](self.item, rule["property_value"], self.session)
                    if not valid:
                        msg_errors_array = self.errors.get(rule["property_name"], [])
                        if msg_errors_array:
                            msg_errors_array.append(check["message"])
                        else:
                            self.errors[rule["property_name"]] = [check["message"]]

                        self.is_valid = False
                        break

