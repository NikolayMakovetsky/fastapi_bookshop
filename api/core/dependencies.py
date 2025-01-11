from typing_extensions import Annotated
from fastapi import Header, Depends

from api.core.localizators.localizator import default_language, supported_langs
from api.core.logging import logger
from api.models import User
from auth.user import current_active_user


async def get_current_language(accept_language: Annotated[str, Header()] = None):
    current_language = default_language
    if accept_language:
        current_language = accept_language[:2]
        if current_language not in supported_langs:
            current_language = default_language
    return current_language


async def get_user_settings(current_language: str = Depends(get_current_language),
                            user: User = Depends(current_active_user)):
    logger.info(f'User settings -> Username: {user.username}, Current language: {current_language}')
    return {"current_language": current_language, "user": user}
