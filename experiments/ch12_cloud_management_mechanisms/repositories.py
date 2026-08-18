from .models import Resource


class ResourceRepository:

    def __init__(self):

        self._resources: dict[
            str,
            Resource,
        ] = {}

    def save(
        self,
        resource: Resource,
    ) -> Resource:

        self._resources[
            resource.resource_id
        ] = resource

        return resource

    def get(
        self,
        resource_id: str,
    ) -> Resource | None:

        return self._resources.get(
            resource_id
        )

    def delete(
        self,
        resource_id: str,
    ) -> None:

        self._resources.pop(
            resource_id,
            None,
        )

    def list_all(
        self,
    ) -> list[Resource]:

        return list(
            self._resources.values()
        )