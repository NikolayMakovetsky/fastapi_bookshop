from fastapi import APIRouter, Depends

from api.models import User
from auth.user import current_user

router = APIRouter(
    prefix="",
    tags=["AuthTest"],
)


@router.get("/current_user")
async def get_current_user(user: User = Depends(current_user)):
    return {'result': f'Hello, {user.username}!'}


@router.get("/some_user", dependencies=[Depends(current_user)])
async def get_some_user():
    return {'result': f'Hello, User!'}


@router.get("/anonymous")
async def get_anonymous():
    return {'result': 'Hello, Anonymous!'}
