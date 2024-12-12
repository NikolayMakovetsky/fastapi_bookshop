import pytest
from pydantic import BaseModel

from api.core.validators import BaseValidator


class TestSchema(BaseModel):
    id: int = 5
    name: str = "Igor"


session = "async_session"
item = TestSchema()

base_valid = BaseValidator(item, session)


async def check_id(item, v: int, session) -> bool:
    if v > 0:
        return True
    return False


def test_message_by_default():
    base_valid.rule_for("id", lambda x: x.id)
    base_valid.must(check_id)
    base_valid.message("New error message")
    assert base_valid.rules[-1]["checklist"][-1]["message"] == "New error message"


def test_message_with_params():
    base_valid.rule_for("id", lambda x: x.id)
    base_valid.greater_than(5)  # "msg_params": {"comparison_value": comparison_value}
    assert base_valid.rules[-1]["checklist"][-1]["message"] == "The value must be greater than '5'"


if __name__ == '__main__':
    pytest.main()
