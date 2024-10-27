from auth.auth import auth_backend

from api.schemas import UserRead, UserCreate
from auth.user import fastapi_users

router1 = fastapi_users.get_auth_router(auth_backend)
router1.prefix = "/auth/jwt"
router1.tags = ["Auth"]

router2 = fastapi_users.get_register_router(UserRead, UserCreate)
router2.prefix = "/auth"
router2.tags = ["Auth"]
