from fastapi import FastAPI
from api.core.server import Server
import uvicorn


def application() -> FastAPI:
    app = FastAPI()
    return Server(app).get_app()


if __name__ == '__main__':
    uvicorn.run(application)
