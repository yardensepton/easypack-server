from fastapi import FastAPI
from src.routers import user_route, item_route, trip_route, packing_list_route


def create_app() -> FastAPI:
    app: FastAPI = FastAPI()

    app.include_router(
        user_route.router
    )
    app.include_router(
        item_route.router
    )
    app.include_router(
        trip_route.router
    )
    app.include_router(
        packing_list_route.router
    )

    return app
