from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import user_route, item_route, trip_route, packing_list_route, city_route, weather_route, \
    exchange_rate_route


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
        exchange_rate_route.router
    )
    app.include_router(
        weather_route.router
    )

    # Configure CORS
    origins = [
        "http://localhost",
        "http://localhost:54689",
        "http://192.168.1.197:8000",
        "http://192.168.1.197",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
