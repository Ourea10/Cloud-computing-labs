class ResourceRepository:

    def __init__(self):

        self.resources = {}

    def create(self, resource):

        self.resources[
            resource.id
        ] = resource

        return resource

    def get(self, resource_id):

        return self.resources.get(
            resource_id
        )

    def list_by_project(
        self,
        project_id,
    ):

        return [
            resource
            for resource
            in self.resources.values()
            if resource.project_id
            == project_id
        ]

    def update_status(
        self,
        resource_id,
        status,
    ):

        resource = self.resources[
            resource_id
        ]

        resource.status = status

        return resource