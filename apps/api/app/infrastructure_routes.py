from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.security import (
    get_current_user,
)

from app.security_store import User

from app.infrastructure import (
    cloud_infrastructure,
)


router = APIRouter(
    prefix="/infrastructure",
    tags=["infrastructure"],
)


@router.post("/servers")
def create_server(
    server_id: str,
    cpu: int,
    memory_mb: int,
    image: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    try:

        server = (
            cloud_infrastructure
            .create_server(
                server_id=server_id,
                tenant_id=current_user.tenant_id,
                cpu=cpu,
                memory_mb=memory_mb,
                image=image,
            )
        )

    except RuntimeError as error:

        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error

    return {
        "server_id": server.server_id,
        "tenant_id": server.tenant_id,
        "cpu": server.cpu_cores,
        "memory_mb": server.memory_mb,
        "state": server.state,
        "private_ip": server.private_ip,
    }


@router.post("/storage")
def create_storage(
    volume_id: str,
    size_gb: int,
    current_user: User = Depends(
        get_current_user
    ),
):

    try:

        volume = (
            cloud_infrastructure
            .create_storage(
                volume_id=volume_id,
                tenant_id=current_user.tenant_id,
                size_gb=size_gb,
            )
        )

    except (
        ValueError,
        RuntimeError,
    ) as error:

        raise HTTPException(
            status_code=409,
            detail=str(error),
        ) from error

    return {
        "volume_id": volume.volume_id,
        "tenant_id": volume.tenant_id,
        "size_gb": volume.size_gb,
        "storage_type": (
            volume.storage_type
        ),
    }