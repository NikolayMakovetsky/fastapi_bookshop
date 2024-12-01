import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.core.localizators import load_localize_data
from api.core.server import Server
from api.core.logging import logger, LOG_CONFIG


def application() -> FastAPI:
    app = FastAPI()

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
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": modified_details}),
        )

    logger.info("Localization data loading...")
    load_localize_data()
    logger.info("Localization data loaded. Success.")
    logger.info("==================== Start service =========================")
    return Server(app).get_app()


if __name__ == '__main__':
    uvicorn.run(application, log_level="trace", log_config=LOG_CONFIG)
    logger.info("==================== Stop service =========================")
