from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ..schemas import User
from .deps import get_current_active_ws_user
from .manager import WSConnectionManager

ws_router = APIRouter(prefix="", tags=["WebSockets"])
manager = WSConnectionManager()


@ws_router.websocket("/ws/events")
async def websocket_events(websocket: WebSocket, user: User = Depends(get_current_active_ws_user)):
    await manager.connect(user, websocket)
    await manager.send_all_without_user(user, f"User {user.email} join")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal(user, data)
            await manager.send_all_without_user(user, data)
    except WebSocketDisconnect:
        manager.disconnect(user)
        await manager.send_all(f"User {user.email} left")
