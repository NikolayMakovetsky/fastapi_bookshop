from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.auth import auth_backend

from api.models import Userlist

fastapi_users = FastAPIUsers[Userlist, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
