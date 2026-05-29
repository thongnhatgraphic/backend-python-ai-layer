import json
from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.connection_manager import manager

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: UUID):
    user_id = str(user_id)
    
    await manager.connect(websocket, user_id)

    try:
        while True:
            data = await websocket.receive_text()

            print('data', data)

            parsed_data = json.loads(data)

            print(f"{user_id}", parsed_data)

    except WebSocketDisconnect:
        manager.disconnect(
            websocket,
            user_id
        )

        print(
            f"User {user_id} disconnected"
        )