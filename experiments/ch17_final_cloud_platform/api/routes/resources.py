from fastapi import APIRouter

from ...schemas import ResourceCreate

from ...services.resource_service import (
    ResourceService,
)

from ..dependencies import (
    resource_repository,
)


router = APIRouter()

service = ResourceService(
    resource_repository
)


@router.post("/")
def create_resource(
    project_id: str,
    request: ResourceCreate,
):

    return service.create(
        project_id=project_id,
        name=request.name,
        resource_type=request.resource_type,
    )


@router.get("/{resource_id}")
def get_resource(
    resource_id: str,
):

    return service.get(
        resource_id
    )