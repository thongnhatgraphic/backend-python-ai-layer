from fastapi import FastAPI
from prometheus_client import make_asgi_app

from app.router_registry import all_router

app = FastAPI()

for router in all_router:
    app.include_router(
        router["router"],
        prefix=router["prefix"],
        tags=router["tags"],
    )

metrics_app = make_asgi_app()

app.mount(
    "/metrics",
    metrics_app,
)
