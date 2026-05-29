from app.routers.task_router import router as task_router
from app.routers.user_router import router as user_router
from app.routers.notification_router import router as notification_router

from app.websocket.notification_websocket import router as ws_notification_router

all_routers = [
    {
        "router": task_router,
        "prefix": "/tasks",
        "tags": ["Tasks"]
    },
    {
        "router": user_router,
        "prefix": "/users",
        "tags": ["Users"]
    },
    {
        "router": notification_router,
        "prefix": "/notifications",
        "tags": ["Notification"]
    },
    {
        "router": ws_notification_router,
        "prefix": "/notification",
        "tags": ["Notification"]
    }
]