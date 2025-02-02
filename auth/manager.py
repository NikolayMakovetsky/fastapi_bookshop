from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from api.core.database import get_user_db
from api.models import User

# from .db import User, get_user_db

SECRET = "SECRET"  # Еще один секретный ключ для сброса пароля и для верификации


# Класс, который управляет созданием пользователей
class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
