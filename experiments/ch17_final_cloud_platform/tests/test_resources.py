from ..repositories.resource_repository import (
    ResourceRepository,
)

from ..services.resource_service import (
    ResourceService,
)


def test_create_resource():

    repository = ResourceRepository()

    service = ResourceService(
        repository
    )

    resource = service.create(
        project_id="project-1",
        name="api-server",
        resource_type="compute",
    )

    assert resource.status == (
        "creating"
    )

    service.update_status(
        resource.id,
        "running",
    )

    result = service.get(
        resource.id
    )

    assert result.status == "running"