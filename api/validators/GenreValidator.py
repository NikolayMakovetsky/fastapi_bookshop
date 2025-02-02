from api.validators import BaseValidator
from api.validators.validate_funcs import is_unique_name_genre
from api.core.localizators import get_localize_text as _
from api.schemas import GenreValidateSchema


class GenreValidator(BaseValidator):
    def __init__(self, item: GenreValidateSchema, session, lang: str):
        super().__init__(item, session)
        self.rule_for("name_genre", lambda x: x.name_genre) \
            .must(is_unique_name_genre) \
            .message(_(lang, "ERR_UniqueValue"))

