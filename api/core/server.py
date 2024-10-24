from fastapi import FastAPI
from api.core.routes import __routes__


class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)

    def get_app(self) -> FastAPI:
        return self.__app

    # статический метод не относится ни к атрибутам экземпляра, ни к атрибутам самого класса
    @staticmethod
    def __register_events(app):
        """Приватный статический метод регистрации событий"""
        # По аналогии с __register_routes(app) можно реализовать и этот метод
        # app.on_event('startup')()
        # из нужного модуля импортируем сюда ф-ю кот. будет выполнятся при запуске нашего fastapi-сервиса
        ...

    @staticmethod
    def __register_routes(app):
        """Приватный статический метод регистрации путей"""
        __routes__.register_routes(app)
