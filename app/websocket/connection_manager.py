from fastapi import FastAPI, WebSocket
from uuid import UUID
import json
from app.core.redis import redis_client
from datetime import datetime, timezone
from app.constant.user_status import USER_STATUS


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[UUID, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: UUID):
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        redis_client.incr(f"online:user:{user_id}")

        redis_client.publish(
            "presence",
            json.dumps({
                "type": USER_STATUS["online"],
                "data": {
                    "user_id": str(user_id)
                }
            })
        )

        print(
            {
                user: len(sockets) for user, sockets in manager.active_connections.items()
            }
        )

    async def disconnect(self, websocket: WebSocket, user_id: UUID):
        if user_id not in self.active_connections:
            return
        
        if websocket in self.active_connections[user_id]:
            self.active_connections[user_id].remove(websocket)
            

        if not self.active_connections[user_id]:
            del self.active_connections[user_id]
        
        remaining = redis_client.decr(
                f"online:user:{user_id}"
            )
        if remaining <= 0:
            redis_client.delete(f"online:user:{user_id}")
            redis_client.set(
                f"last_seen:user:{user_id}",
                datetime.now(timezone.utc).isoformat()                
            )

            redis_client.publish(
                "presence",
                json.dumps({
                    "type": USER_STATUS["offline"],
                    "data": {
                        "user_id": str(user_id)
                    }
                })
            )
            
        total = sum(
            len(v)
            for v in self.active_connections.values()
        )

        print(f"[DISCONNECT] user={user_id}")
        print(f"[ACTIVE SOCKETS] {total}")

    async def send_to_user(
        self,
        message: dict,
        to_user_id: str
    ):
        user_id = UUID(to_user_id)
        
        if user_id not in self.active_connections:
            return

        dead_connections = []
        print("\n\n\n\n here \n\n\n\n", message)
        for websocket in self.active_connections[user_id]:

            try:
                print('message', message)
                await websocket.send_json(message)

            except Exception:
                dead_connections.append(
                    websocket
                )

        for websocket in dead_connections:
            self.active_connections[user_id].remove(
                websocket
            )


    async def send_personal_message(self, message: dict, user_id: UUID):
        print(f"Message to user {user_id}: {message}")

    async def broadcast(self, message: dict, user_id: UUID):
        print(f"Broadcast: {message}")

        for socket in self.active_connections[user_id]:
            await socket.send_json(message)


manager = ConnectionManager()
