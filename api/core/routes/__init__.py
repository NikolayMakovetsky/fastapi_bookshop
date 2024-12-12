from api.core.routes.routes import Routes
from api.routers import (genre_router,
                         auth_router,
                         register_router,
                         auth_test_router,
                         author_router,
                         book_router,
                         root_router)

__routes__ = Routes(routers=(
    root_router,
    auth_router,
    register_router,
    auth_test_router,
    genre_router,
    author_router,
    book_router
))
