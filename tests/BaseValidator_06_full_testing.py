import pytest
from pydantic import BaseModel

from api.core.validators import BaseValidator
from api.database import new_session
from api.core.localizators import get_localize_text as _


class TestSchema(BaseModel):
    id: int = 1
    name: str = "Igor"


test = TestSchema()


class TestValidator(BaseValidator):
    def __init__(self, item: TestSchema, session):
        super().__init__(item, session)
        self.rule_for("id", lambda x: x.id) \
            .greater_than(3) \
            .message(_("ERR_ValueGreaterThan")) \


async def test_greater_than():
    async with new_session() as session:
        validator = TestValidator(test, session)
        await validator.validate()
    assert validator.rules[-1]["checklist"][-1]["message"] == "The value must be greater than '3'"


if __name__ == '__main__':
    pytest.main()
