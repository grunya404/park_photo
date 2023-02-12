from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyQuery, APIKeyHeader
from jose import jwt
from pydantic import ValidationError
from starlette.status import HTTP_403_FORBIDDEN

from config import settings
from core import crud, schemas
from redis.utils import get_object_from_redis, set_object_to_redis
from security import ALGORITHM

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/api/v1/login/access-token")

api_key_query = APIKeyQuery(name=settings.API_KEY, auto_error=False)
api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER_NAME, auto_error=False)


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
):
    if api_key_query == settings.API_KEY:
        return api_key_query
    elif api_key_header == settings.API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


def get_token_data(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


async def get_current_user(token: str = Depends(reusable_oauth2)) -> schemas.User:
    token_data = get_token_data(token)
    user = await get_object_from_redis(f"user:{token_data.sub}", schemas.User)
    if not user:
        user = await crud.user.get(token_data.sub)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user = schemas.User.parse_obj(user)
        await set_object_to_redis(f"user:{token_data.sub}", user)
    return user


def check_token_access(
        current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_user(
        current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
        current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="The user doesn't have enough privileges")
    return current_user
