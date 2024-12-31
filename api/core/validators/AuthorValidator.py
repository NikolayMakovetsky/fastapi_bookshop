from api.core.validators import BaseValidator
from api.core.validators.validate_funcs import is_unique_name_author
from api.core.localizators import get_localize_text as _
from api.schemas import AuthorValidateSchema


class AuthorValidator(BaseValidator):
    def __init__(self, item: AuthorValidateSchema, session, lang: str):
        super().__init__(item, session)
        self.rule_for("name_author", lambda x: x.name_author) \
            .must(is_unique_name_author) \
            .message(_(lang, "ERR_UniqueValue"))

