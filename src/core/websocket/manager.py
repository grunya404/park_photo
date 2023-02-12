from typing import Dict

from starlette.websockets import WebSocket

from core.schemas.user import User


class WSConnectionManager:
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(WSConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user: User, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user.id] = websocket

    def disconnect(self, user: User):
        del self.active_connections[user.id]

    async def send_personal(self, user: User, message: str):
        websocket = self.active_connections.get(user.id)
        if websocket:
            await websocket.send_text(message)

    async def send_all(self, message: str):
        for conn in self.active_connections.values():
            await conn.send_text(message)

    async def send_all_without_user(self, user: User, message: str):
        for user_id, conn in self.active_connections.items():
            if user.id != user_id:
                await conn.send_text(message)
