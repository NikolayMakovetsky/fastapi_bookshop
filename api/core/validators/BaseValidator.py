from typing import Callable


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

    def must(self, check_function):
        """3. Добавляется проверочная функция, которая должна вернуть: True или False
        Проверочных функций для одного свойства может быть несколько
        checking func should take 3 params:item(schema),value,session and return True(Success)/False)
        """
        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append({"check_function": check_function, "message": "Data validation failed", "when_function": None, "msg_params": {}})
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

    def when(self, when_function):
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

    def not_empty(self):

        async def check_function(item, value, session) -> bool:
            if value:
                return True
            return False

        current_rule = self.rules[-1]
        checklist = current_rule["checklist"]
        checklist.append({"check_function": check_function, "message": "The field must not be empty", "when_function": None, "msg_params": {}})
        return self

    def greater_than(self, comparison_value):

        async def check_function(item, value, session) -> bool:

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


# FLUENT VALIDATOR:
# https://docs.fluentvalidation.net/en/latest/built-in-validators.html


# DONE:
# + RuleFor(customer => customer.Surname).NotEmpty();
# + RuleFor(customer => customer.CreditLimit).GreaterThan(0);
# + RuleFor(customer => customer.Surname).Must(surname => surname == "Foo");

# IMPLEMENT:
# RuleFor(customer => customer.CreditLimit).LessThan(100);
# RuleFor(customer => customer.CreditLimit).LessThanOrEqualTo(100);
# RuleFor(customer => customer.CreditLimit).GreaterThanOrEqualTo(1);

# RuleFor(x => x.Surname).Empty();

# RuleFor(x => x.Surname).Null();
# RuleFor(customer => customer.Surname).NotNull();

# RuleFor(customer => customer.Surname).Equal("Foo"); (Any))
# RuleFor(customer => customer.Surname).NotEqual("Foo");

# RuleFor(customer => customer.Surname).MaximumLength(250); //must be 250 chars or fewer (len: str)
# RuleFor(customer => customer.Surname).MinimumLength(10); //must be 10 chars or more

# RuleFor(x => x.Id).ExclusiveBetween(1,10); (int, float)
# RuleFor(x => x.Id).InclusiveBetween(1,10);

# RuleFor(customer => customer.Surname).Length(1, 250); //must be between 1 and 250 chars (inclusive)  (str)


# RuleFor(x => x.Amount).PrecisionScale(4, 2, false);  (проверка float числа 4 знака всего, 2 после точки)
# RuleFor(x => x.ErrorLevel).IsInEnum();
# RuleFor(customer => customer.Surname).Matches("some regex here");



        # "EmailValidator" => "The value is not a valid email address",
        # "GreaterThanOrEqualValidator" => "The value must be greater than or equal to '{ComparisonValue}'",
        # "GreaterThanValidator" => "The value must be greater than '{ComparisonValue}'",
        # "LengthValidator" => "The value must be between {MinLength} and {MaxLength} characters. You entered {TotalLength} characters.",
        # "MinimumLengthValidator" => "The value must be at least {MinLength} characters. You entered {TotalLength} characters.",
        # "MaximumLengthValidator" => "The value must be {MaxLength} characters or fewer. You entered {TotalLength} characters.",
        # "LessThanOrEqualValidator" => "The value must be less than or equal to '{ComparisonValue}'",
        # "LessThanValidator" => "The value must be less than '{ComparisonValue}'",
        # "NotEmptyValidator" => "The field must not be empty",
        # "NotEqualValidator" => "The value must not be equal to '{ComparisonValue}'",
        # "NotNullValidator" => "The field must not be empty",
        # "PredicateValidator" => "The field contains an invalid value",
        # "AsyncPredicateValidator" => "The field contains an invalid value",
        # "RegularExpressionValidator" => "The value is not in the correct format",
        # "EqualValidator" => "The value must be equal to '{ComparisonValue}'",
        # "ExactLengthValidator" => "The value must be {MaxLength} characters in length. You entered {TotalLength} characters.",
        # "InclusiveBetweenValidator" => "The value must be between {From} and {To}. You entered {PropertyValue}.",
        # "ExclusiveBetweenValidator" => "The value must be between {From} and {To} (exclusive). You entered {PropertyValue}.",
        # "CreditCardValidator" => "The value is not a valid credit card number",
        # "ScalePrecisionValidator" => "The value must not be more than {ExpectedPrecision} digits in total, with allowance for {ExpectedScale} decimals. {Digits} digits and {ActualScale} decimals were found.",
        # "EmptyValidator" => "The field must be empty",
        # "NullValidator" => "The field must be empty",
        # "EnumValidator" => "The value is not in the specified range",
        # // Additional fallback messages used by clientside validation integration.
        # "Length_Simple" => "The value must be between {MinLength} and {MaxLength} characters",
        # "MinimumLength_Simple" => "The value must be at least {MinLength} characters",
        # "MaximumLength_Simple" => "The value must be {MaxLength} characters or fewer",
        # "ExactLength_Simple" => "The value must be {MaxLength} characters in length",
        # "InclusiveBetween_Simple" => "The value must be between {From} and {To}",

