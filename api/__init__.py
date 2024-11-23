from fastapi import FastAPI
from api.core.server import Server
import uvicorn
from api.core.logging import logger, LOG_CONFIG


def application() -> FastAPI:
    app = FastAPI()
    logger.info("==================== Start service =========================")
    return Server(app).get_app()


if __name__ == '__main__':
    uvicorn.run(application, log_level="trace", log_config=LOG_CONFIG)
    logger.info("==================== Stop service =========================")
