from api.core.routes.routes import Routes
from api.routers import genre_router, auth_router, register_router, hello_router


__routes__ = Routes(routers=(
    genre_router,
    auth_router,
    register_router,
    hello_router
))
