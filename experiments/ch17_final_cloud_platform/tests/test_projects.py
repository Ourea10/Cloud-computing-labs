from ..repositories.project_repository import (
    ProjectRepository,
)

from ..services.project_service import (
    ProjectService,
)


def test_create_project():

    repository = ProjectRepository()

    service = ProjectService(
        repository
    )

    project = service.create(
        owner_id="user-1",
        name="Ecommerce",
        description="Test project",
    )

    assert project.name == "Ecommerce"

    projects = service.list_projects(
        "user-1"
    )

    assert len(projects) == 1