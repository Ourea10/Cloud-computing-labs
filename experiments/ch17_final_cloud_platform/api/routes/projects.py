from fastapi import APIRouter

from ...schemas import ProjectCreate

from ...services.project_service import (
    ProjectService,
)

from ..dependencies import (
    project_repository,
)


router = APIRouter()

service = ProjectService(
    project_repository
)


@router.post("/")
def create_project(
    owner_id: str,
    request: ProjectCreate,
):

    project = service.create(
        owner_id=owner_id,
        name=request.name,
        description=request.description,
    )

    return project


@router.get("/")
def list_projects(
    owner_id: str,
):

    return service.list_projects(
        owner_id
    )