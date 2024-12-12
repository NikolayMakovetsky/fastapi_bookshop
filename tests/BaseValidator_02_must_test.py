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


def test_append_check_function():
    base_valid.rule_for("id", lambda x: x.id)
    base_valid.must(check_id)
    assert base_valid.rules[-1]["checklist"][-1]["check_function"] == check_id


def test_append_message():
    base_valid.rule_for("id", lambda x: x.id)
    base_valid.must(check_id)
    assert base_valid.rules[-1]["checklist"][-1]["message"] == "Data validation failed"


if __name__ == '__main__':
    pytest.main()
