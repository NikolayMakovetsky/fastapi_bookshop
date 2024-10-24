from api.core.routes.routes import Routes
from api.routers import genre_router


__routes__ = Routes(routers=(
    genre_router,
))
