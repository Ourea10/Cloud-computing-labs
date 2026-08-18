from fastapi import APIRouter, Depends

from .dependencies import (
    require_permission,
)

from .schemas import (
    DirectIORequest,
    EdgeProcessRequest,
    MultipathRequest,
)

from ..specialized_cloud_service import (
    SpecializedCloudService,
)


router = APIRouter()

service = (
    SpecializedCloudService()
)


@router.post(
    "/storage/{storage_id}/allocate"
)
def allocate_storage(
    storage_id: str,
    amount_gb: int,
    user=Depends(
        require_permission(
            "resource:manage"
        )
    ),
):

    service.storage.allocate(
        storage_id,
        amount_gb,
    )

    storage = service.storage.get(
        storage_id
    )

    return {
        "storage_id": storage.storage_id,
        "capacity_gb": storage.capacity_gb,
        "used_gb": storage.used_gb,
        "available_gb": (
            service.storage
            .available_capacity(
                storage_id
            )
        ),
    }


@router.post(
    "/direct-io"
)
def grant_direct_io(
    request: DirectIORequest,
    user=Depends(
        require_permission(
            "resource:manage"
        )
    ),
):

    access = (
        service.direct_io
        .grant_access(
            resource_id=(
                request.resource_id
            ),
            lun_id=request.lun_id,
            client_id=request.client_id,
        )
    )

    return {
        "resource_id": access.resource_id,
        "lun_id": access.lun_id,
        "client_id": access.client_id,
        "enabled": access.enabled,
    }


@router.get(
    "/multipath"
)
def get_multipath(
    request: MultipathRequest,
    user=Depends(
        require_permission(
            "resource:read"
        )
    ),
):

    paths = (
        service.multipath
        .available_paths(
            request.source_id,
            request.target_id,
        )
    )

    return [
        {
            "path_id": path.path_id,
            "status": path.status.value,
            "connection_type": (
                path.connection_type.value
            ),
        }
        for path in paths
    ]


@router.post(
    "/edge/process"
)
def process_edge_data(
    request: EdgeProcessRequest,
    user=Depends(
        require_permission(
            "resource:manage"
        )
    ),
):

    return service.edge.process(
        request.node_id,
        request.data,
    )