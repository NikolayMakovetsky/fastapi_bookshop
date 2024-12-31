import uvicorn
from fastapi import FastAPI, Request, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api.core.localizators import load_localize_data
from api.core.server import Server
from api.core.logging import logger, LOG_CONFIG
from api.dependencies import get_current_language
from api.models import User


def application() -> FastAPI:

    app = FastAPI(redoc_url=None, dependencies=[Depends(get_current_language)])

    logger.info("Localization data loading...")
    load_localize_data()
    logger.info("Localization data successfully loaded.")

    logger.info("==================== Start service =========================")
    server_app = Server(app).get_app()

    # --> fastapi.exceptions settings (set status_code=400 instead of 422 if fastapi raises RequestValidationError)
    # status_code=422 we will use for custom validator
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Get the original 'detail' list of errors
        details = exc.errors()
        modified_details = []
        # Replace 'msg' with 'message' for each error
        for error in details:
            modified_details.append(
                {
                    "loc": error["loc"],
                    "message": error["msg"],
                    "type": error["type"],
                }
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,  # 400 instead of 422
            content=jsonable_encoder({"detail": modified_details}),
        )
    # <--

    # --> fastapi.openapi settings
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="BookShopAPI",
            version="1.0.0",
            license_info={"name": "MIT Licence"},
            summary="«Магазин книг»",
            description="_**Формирование, комплектация и отслеживание заказов на реализацию**_", # ** bold, _ cursive
            routes=app.routes
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    # <--

    return server_app


if __name__ == '__main__':
    uvicorn.run(application, factory=True, log_level="trace", log_config=LOG_CONFIG)
    logger.info("==================== Stop service =========================")
