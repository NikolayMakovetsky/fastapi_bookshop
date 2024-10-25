from fastapi_users import schemas
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    user_id: int
    username: str
    email: str
    # password: str
    # hashed_password: str  ПАРОЛЬ ЗДЕСЬ ВЫВОДИТЬ НЕЛЬЗЯ
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(schemas.BaseUserCreate):
    user_id: int
    username: str
    email: str
    # password: str
    hashed_password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass