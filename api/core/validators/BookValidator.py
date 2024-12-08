from api.core.validators import BaseValidator
from api.core.validators.validate_funcs import check_genre_id, check_author_id
from api.core.localizators import get_localize_text as _
from api.schemas.BookSchema import BookValidateSchema


class BookValidator(BaseValidator):
    """Validation map for object BookValidateSchema

    All methods should be called strictly one by one!

    self.rule_for(attribute, func for calculating attribute value)
        .must(checking func. It'll take 3 params:item,value,session and return True(Success)/False)
        .message(func that adds text of our Custom error message for must() THAT DESCRIBED ABOVE)
                 if we'll use must() without message(), it'll use default error message
        .when(func that sets special conditions to run check function added to must() THAT DESCRIBED ABOVE)
              if we'll not use when() then must() will run in any case

        If we have some checking funcs in rule_for and one of them fails we go to next must()
    """

    def __init__(self, item: BookValidateSchema, session):
        super().__init__(item, session)
        self.rule_for("genre_id", lambda x: x.genre_id) \
            .greater_than(1) \
            .message(_("ERR_ValueGreaterThan")) \
            .must(check_genre_id)\
            .message(_("ERR_ValueNotFoundInList"))
        self.rule_for("author_id", lambda x: x.author_id) \
            .greater_than(2) \
            .message(_("ERR_ValueGreaterThan")) \
            .must(check_author_id)\
            .message(_("ERR_ValueNotFoundInList"))

