from app.routers.task_router import router as task_router
from app.routers.user_router import router as user_router

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
    }
]