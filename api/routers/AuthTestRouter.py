from fastapi import APIRouter, Depends

from api.core.dependencies import get_user_settings
from api.models import User
from auth.user import current_user


router = APIRouter(
    prefix="",
    tags=["AuthTest"],
    dependencies=[Depends(get_user_settings)]
)


@router.get("/current_user")
async def get_current_user(user: User = Depends(current_user)):
    return {'result': f'Hello, {user.username}!'}


@router.get("/some_user")
async def get_some_user(current_user_settings = Depends(get_user_settings)):
    return {'result': f'Hello, {current_user_settings["user"].username}!'}

