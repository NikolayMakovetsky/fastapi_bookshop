from dataclasses import dataclass
from fastapi import FastAPI


# создаем именно dataclass т.к. он будет принимать и хранить в атрибутах определенные пути,
# которые мы будем затем регистрировать


@dataclass(frozen=True)  # frozen class неизменяемый
class Routes:
    routers: tuple

    def register_routes(self, app: FastAPI):
        """Функция регистрирующая роутер в наше приложение"""

        for router in self.routers:
            app.include_router(router, tags=router.tags)  # prefix=router.prefix
