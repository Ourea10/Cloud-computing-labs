from resource import ComputeResource


class ResourcePool:
    def __init__(self):
        self.resources: list[ComputeResource] = []

    def add(self, resource: ComputeResource):
        self.resources.append(resource)

    def allocate(
        self,
        cpu: int,
        memory: int,
    ) -> ComputeResource:

        for resource in self.resources:
            if (
                not resource.allocated
                and resource.cpu >= cpu
                and resource.memory >= memory
            ):
                resource.allocate()
                return resource

        raise RuntimeError(
            "No suitable resource is available"
        )

    def release(self, resource_id: str):
        for resource in self.resources:
            if resource.resource_id == resource_id:
                resource.release()
                return

        raise ValueError(
            f"Unknown resource: {resource_id}"
        )