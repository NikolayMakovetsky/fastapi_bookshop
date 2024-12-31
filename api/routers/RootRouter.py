from fastapi import APIRouter


router = APIRouter(
    prefix="",
    tags=["Root"],
)


@router.get("/")
async def get_hello_world():
    return {'result': f'Hello, world!'}


@router.get("/anonymous")
async def get_anonymous():
    return {'result': 'Hello, Anonymous!'}
