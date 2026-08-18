import uuid

from ..models import Project
from ..repositories.project_repository import (
    ProjectRepository,
)


class ProjectService:

    def __init__(
        self,
        repository: ProjectRepository,
    ):

        self.repository = repository

    def create(
        self,
        owner_id: str,
        name: str,
        description: str,
    ):

        project = Project(
            id=str(uuid.uuid4()),
            owner_id=owner_id,
            name=name,
            description=description,
        )

        return self.repository.create(
            project
        )

    def list_projects(
        self,
        owner_id,
    ):

        return self.repository.list_by_owner(
            owner_id
        )