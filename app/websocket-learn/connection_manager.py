from fastapi import WebSocket, WebSocketDisconnect, FastAPI

from fastapi import WebSocketDisconnect
import json

app = FastAPI()

# Lyfecycle
# connect
# → accept
# → add to list
# → receive/send loop
# → disconnect
# → remove from list


class ConnectionManager:

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        print(f"{user_id} connected")

        print(self.active_connections)

    def disconnect(self, user_id, websocket: WebSocket):

        if user_id in self.active_connections:
            connections = self.active_connections[user_id]
            if websocket in connections:
                connections.remove(websocket)

            if len(connections) == 0:
                del self.active_connections[user_id]

        print("Client disconnected")
        print(f"Total clients: {len(self.active_connections)}")

    async def send_personal_message(self, message: str, user_id: str):
        connections = self.active_connections.get(user_id)
        if not connections:
            return
        
        disconnected_connections = []

        for connection in connections:
            try:
                await connection.send_text(f"me: {message}")
            except Exception:
                disconnected_connections.append(connection)
        for connection in disconnected_connections:
            connections.remove(connection)

    async def send_to_user(
        self,
        from_user: str,
        to_user: str,
        message: str
    ):

        connections = self.active_connections.get(to_user)

        if not connections:

            print(f"{to_user} is offline")

            return

        disconnected_connections = []

        for connection in connections:
            try:
                await connection.send_text(
                    f"{from_user}: {message}"
                )

            except Exception:

                disconnected_connections.append(connection)

        for connection in disconnected_connections:

            connections.remove(connection)

    async def broadcast(self, message: str):

        disconnected_connections = []

        for connection in self.active_connections:

            try:
                await connection.send_text(message)

            except Exception as e:

                print("Broadcast error:", e)

                disconnected_connections.append(connection)

        for connection in disconnected_connections:
            self.disconnect(connection)


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):

    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()
            print('data', data)

            parsed_data = json.loads(data)

            to_user = parsed_data["to"]
            message = parsed_data["message"]

            print(f"{user_id} -> {to_user}: {message}")


            await manager.send_to_user(user_id, to_user, message)
            await manager.send_personal_message(f"{message}", user_id)
    except WebSocketDisconnect:

        print("disconnect socket:", websocket)

        manager.disconnect(user_id, websocket)
