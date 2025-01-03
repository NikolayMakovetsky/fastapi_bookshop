from api.core.routes.routes import Routes
from api.routers import (genre_router,
                         auth_router,
                         register_router,
                         auth_test_router,
                         author_router,
                         book_router,
                         root_router)

from reports import (rep_books_that_was_not_sold_router, rep_qty_balance_router)

__routes__ = Routes(routers=(
    root_router,
    auth_router,
    register_router,
    auth_test_router,
    genre_router,
    author_router,
    book_router,
    rep_books_that_was_not_sold_router,
    rep_qty_balance_router
))
