from api.core.validators import BaseValidator
from api.core.validators.validate_funcs import is_unique_name_genre
from api.core.localizators import get_localize_text as _
from api.schemas import GenreValidateSchema


class GenreValidator(BaseValidator):
    def __init__(self, item: GenreValidateSchema, session):
        super().__init__(item, session)
        self.rule_for("name_genre", lambda x: x.name_genre) \
            .must(is_unique_name_genre) \
            .message(_("ERR_UniqueValue"))

