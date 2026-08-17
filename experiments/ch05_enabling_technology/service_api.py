from dataclasses import dataclass


@dataclass
class ServiceResponse:
    status_code: int
    body: dict


class CloudResourceService:
    def __init__(self):
        self.resources: dict[str, dict] = {}

    def create_resource(
        self,
        resource_id: str,
        cpu: int,
        memory: int,
    ) -> ServiceResponse:

        self.resources[resource_id] = {
            "id": resource_id,
            "cpu": cpu,
            "memory": memory,
        }

        return ServiceResponse(
            status_code=201,
            body=self.resources[resource_id],
        )

    def get_resource(
        self,
        resource_id: str,
    ) -> ServiceResponse:

        resource = self.resources.get(
            resource_id
        )

        if resource is None:
            return ServiceResponse(
                status_code=404,
                body={
                    "error": "resource_not_found"
                },
            )

        return ServiceResponse(
            status_code=200,
            body=resource,
        )