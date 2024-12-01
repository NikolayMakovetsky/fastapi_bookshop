from http import HTTPStatus

from starlette.responses import JSONResponse

from api.core.localizators import translations


def validation_problem(status: int, content: dict | None = None):

    match status:
        case HTTPStatus.BAD_REQUEST:
            msg_key = "400BadRequest"
            msg_str = HTTPStatus(HTTPStatus.BAD_REQUEST).phrase
        case HTTPStatus.NOT_FOUND:
            msg_key = "404NotFound"
            msg_str = HTTPStatus(HTTPStatus.NOT_FOUND).phrase
        case HTTPStatus.CONFLICT:
            msg_key = "409Conflict"
            msg_str = HTTPStatus(HTTPStatus.CONFLICT).phrase
        case HTTPStatus.PRECONDITION_FAILED:
            msg_key = "412PreconditionFailed"
            msg_str = HTTPStatus(HTTPStatus.PRECONDITION_FAILED).phrase
        case HTTPStatus.UNPROCESSABLE_ENTITY:
            msg_key = "422UnprocessableEntity"
            msg_str = HTTPStatus(HTTPStatus.UNPROCESSABLE_ENTITY).phrase
        case _:
            msg_key = ""
            msg_str = ""

    msg_str = translations.get(('ru', msg_key), msg_str)
    cnt = {"title": "", "status": status, "errors": {}}
    if content:
        cnt = content
    cnt["title"] = msg_str

    return JSONResponse(status_code=status, content=cnt)

