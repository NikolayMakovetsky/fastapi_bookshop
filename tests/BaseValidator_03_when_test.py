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


async def when_check_id(item, v: int, session) -> bool:
    if v > 3:
        return True
    return False


def test_when():
    base_valid.rule_for("id", lambda x: x.id)
    base_valid.must(check_id)
    base_valid.when(when_check_id)
    assert base_valid.rules[-1]["checklist"][-1]["when_function"] == when_check_id


if __name__ == '__main__':
    pytest.main()
