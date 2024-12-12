import pytest
from pydantic import BaseModel

from api.core.validators import BaseValidator


class TestSchema(BaseModel):
    id: int = 5
    name: str = "Igor"


session = "async_session"
item = TestSchema()

base_valid = BaseValidator(item, session)


def test_property_name():
    base_valid.rule_for("id", lambda x: x.id)
    assert base_valid.rules[-1]["property_name"] == "id"


def test_property_value_int():
    base_valid.rule_for("id", lambda x: x.id)
    assert base_valid.rules[-1]["property_value"] == 5


def test_property_value_str():
    base_valid.rule_for("name", lambda x: x.name)
    assert base_valid.rules[-1]["property_value"] == "Igor"


if __name__ == '__main__':
    pytest.main()
