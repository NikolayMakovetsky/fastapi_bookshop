from fastapi import APIRouter, Depends

from api.models import Userlist
from auth.user import current_user

router = APIRouter(
    prefix="/hello",
    tags=["The Hello Auth Test"],
)


@router.get("/current_user")
async def get_hello_for_current_user(user: Userlist = Depends(current_user)):
    return {'result': f'Hello, {user.username}!'}


@router.get("/some_user", dependencies=[Depends(current_user)])
async def get_hello_for_some_user():
    return {'result': f'Hello, User!'}


@router.get("/anonymous")
async def get_hello_for_anonymous():
    return {'result': 'Hello, Anonymous!'}
