from api.core.routes.routes import Routes
from api.routers import genre_router, auth_router, register_router, hello_router, author_router, book_router

__routes__ = Routes(routers=(
    auth_router,
    register_router,
    genre_router,
    hello_router,
    author_router,
    book_router
))
