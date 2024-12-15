import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api.core.localizators import load_localize_data
from api.core.server import Server
from api.core.logging import logger, LOG_CONFIG


def application() -> FastAPI:

    app = FastAPI(redoc_url=None)


    # tags_metadata = [
    #     {
    #         "name": "fusers", # Genres
    #         "description": "This is **user** route"
    #     },
    #     {
    #         "name": "trades", # Books
    #         "description": "This is _**trades**_ route"  #
    #     },
    # ]
    #
    # app = FastAPI(
    #     openapi_tags=tags_metadata,
     # )

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

    # --> fastapi.openapi settings (add header parameter "accept-language" to all OPENAPI-routers)
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
    app_structure = app.openapi()

    OPENAPI_ACCEPT_LANGUAGE_PARAM = {
        "name": "accept-language",
        "in": "header",
        "description": "pass the locale here: examples like => ru,en,ru_RU,en-US,ja-JP",
        "style": "simple",
        "schema": {
            "type": "String"
        }
    }

    #  previous app_structure init
    for k_path, path in app_structure['paths'].items():
        for k_http, method in path.items():
            if 'parameters' not in method:
                method['parameters'] = []
            method['parameters'].append(OPENAPI_ACCEPT_LANGUAGE_PARAM)
    # <--

    return server_app


if __name__ == '__main__':
    uvicorn.run(application, factory=True, log_level="trace", log_config=LOG_CONFIG)
    logger.info("==================== Stop service =========================")
