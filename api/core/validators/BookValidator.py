from api.core.validators import BaseValidator
from api.core.validators.validate_funcs import check_val_gt_zero, check_genre_id, check_author_id
from api.core.localizators import get_localize_text as _


class BookValidator(BaseValidator):
    def __init__(self, item, session):
        super().__init__(item, session)
        self.rule_for("genre_id", lambda x: x.genre_id) \
            .must(check_val_gt_zero)\
            .message(_("ERR_ValueNotGreaterZero"))\
            .must(check_genre_id)\
            .message(_("ERR_ValueNotFoundInList"))
        self.rule_for("author_id", lambda x: x.author_id) \
            .must(check_val_gt_zero)\
            .message(_("ERR_ValueNotGreaterZero"))\
            .must(check_author_id)\
            .message(_("ERR_ValueNotFoundInList"))

