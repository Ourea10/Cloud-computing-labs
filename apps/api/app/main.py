from fastapi import FastAPI

from app.routers.health import router as health_router

from app.security_routes import router as security_router

app = FastAPI(
    title="Cloud Computing Lab API",
    version="0.1.0",
)

app.include_router(health_router)

app.include_router(
    security_router
)