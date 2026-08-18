from fastapi import FastAPI

from .routes.auth import router as auth_router
from .routes.projects import router as project_router
from .routes.resources import router as resource_router
from .routes.monitoring import router as monitoring_router
from .routes.alerts import router as alert_router


app = FastAPI(
    title="Cloud Asset Management Platform",
    version="1.0.0",
)


app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["auth"],
)

app.include_router(
    project_router,
    prefix="/api/v1/projects",
    tags=["projects"],
)

app.include_router(
    resource_router,
    prefix="/api/v1/resources",
    tags=["resources"],
)

app.include_router(
    monitoring_router,
    prefix="/api/v1/monitoring",
    tags=["monitoring"],
)

app.include_router(
    alert_router,
    prefix="/api/v1/alerts",
    tags=["alerts"],
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }