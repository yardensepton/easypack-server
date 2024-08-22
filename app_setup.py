from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import user_route, item_route, trip_route, packing_list_route, city_route, weather_route


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
    app.include_router(
        city_route.router
    )

    app.include_router(
        weather_route.router
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
