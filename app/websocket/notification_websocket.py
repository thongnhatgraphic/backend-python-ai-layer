import json
import asyncio
from uuid import UUID

from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.core.redis import redis_client
from app.websocket.connection_manager import manager

router = APIRouter()

async def receive_loop(websocket: WebSocket):
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: UUID
):
    
    await manager.connect(
        websocket,
        user_id
    )

    print(
        f"[CONNECT] user={user_id}"
    )
    print(
        f"[ACTIVE SOCKETS] {len(manager.active_connections[user_id])}"
    )

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("WebSocket disconnected")
        await manager.disconnect(
            websocket,
            user_id
        )