from fastapi import fastAPI, Websocket
from uuid import UUID


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: Websocket, user_id: UUID):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(websocket)

        print(f"User {user_id} connected")

    async def disconnect(self, websocket: Websocket, user_id: UUID):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: UUID):
        if user_id not in self.active_connections:
            return

        for connection in self.active_connections[user_id]:
            await connection.send_json(message)


manager = ConnectionManager()
