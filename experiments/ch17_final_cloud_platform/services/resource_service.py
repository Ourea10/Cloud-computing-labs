import uuid

from ..models import Resource
from ..repositories.resource_repository import (
    ResourceRepository,
)


class ResourceService:

    def __init__(
        self,
        repository: ResourceRepository,
    ):

        self.repository = repository

    def create(
        self,
        project_id,
        name,
        resource_type,
    ):

        resource = Resource(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=name,
            resource_type=resource_type,
            status="creating",
        )

        return self.repository.create(
            resource
        )

    def get(
        self,
        resource_id,
    ):

        return self.repository.get(
            resource_id
        )

    def update_status(
        self,
        resource_id,
        status,
    ):

        return self.repository.update_status(
            resource_id,
            status,
        )