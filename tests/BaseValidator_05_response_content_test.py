import pytest
from pydantic import BaseModel

from api.core.validators import BaseValidator


class TestSchema(BaseModel):
    id: int = 5
    name: str = "Igor"


session = "async_session"
item = TestSchema()

base_valid = BaseValidator(item, session)


def test_response_content_is_valid_true():
    assert base_valid.response_content() is None


def test_response_content_is_valid_false():
    base_valid.is_valid = False
    assert base_valid.response_content() == {
        "title": "Data validation error",
        "status": 422,
        "errors": base_valid.errors
    }


if __name__ == '__main__':
    pytest.main()
