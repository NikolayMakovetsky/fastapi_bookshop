from auth.auth import auth_backend

from api.schemas import UserRead, UserCreate
from auth.user import fastapi_users

router1 = fastapi_users.get_auth_router(auth_backend)
# prefix = "/auth/jwt",
# tags = ["auth"],

router2 = fastapi_users.get_register_router(UserRead, UserCreate)
# prefix = "/auth",
# tags = ["auth"],
