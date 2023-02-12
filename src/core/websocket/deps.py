from typing import Optional

from fastapi import Cookie, Depends, Query, status
from starlette.websockets import WebSocket

from core import schemas
from core.api.deps import (
    get_current_active_superuser,
    get_current_active_user,
    get_current_user,
)


async def get_token(
    websocket: WebSocket,
    session: Optional[str] = Cookie(None),
    token: Optional[str] = Query(None),
) -> str:
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


async def get_current_ws_user(token: str = Depends(get_token)) -> schemas.User:
    return await get_current_user(token)


def get_current_active_ws_user(current_user: schemas.User = Depends(get_current_ws_user)) -> schemas.User:
    return get_current_active_user(current_user)


def get_current_active_ws_superuser(current_user: schemas.User = Depends(get_current_ws_user)):
    return get_current_active_superuser(current_user)
