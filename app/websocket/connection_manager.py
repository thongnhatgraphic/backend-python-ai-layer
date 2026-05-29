from fastapi import FastAPI, WebSocket
from uuid import UUID


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID):
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)

        print(f"User {user_id} connected")
        print(f"User connect current", self.active_connections)

    def disconnect(self, websocket: WebSocket, user_id: UUID):
        if user_id not in self.active_connections:
            return 
        
        connections = self.active_connections[user_id]

        if websocket in connections:
            connections.remove(websocket)

        if len(connections) == 0:
            del self.active_connections[user_id]
        
        print("Client disconnected")

        print(f"User {user_id} disconnected")

    async def send_to_user(self, message: dict, to_user_id: UUID):
        key = str(to_user_id)
        if key not in self.active_connections:
            return
        
        dead_connections = []

        for connection in self.active_connections[key]:
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.append(connection)

        for connection in dead_connections:
            self.active_connections[key].remove(connection)

        print(f"Message to user {to_user_id}: {message}")


    async def send_personal_message(self, message: dict, user_id: UUID):
        print(f"Message to user {user_id}: {message}")


manager = ConnectionManager()
