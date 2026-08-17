from experiments.ch01_introduction.resource import ComputeResource
from experiments.ch01_introduction.resource_pool import ResourcePool

from .case_model import CloudCase


class CloudProvider:
    def __init__(self, name: str):
        self.name = name
        self.resource_pool = ResourcePool()

    def add_resource(
        self,
        resource: ComputeResource,
    ) -> None:
        self.resource_pool.add(resource)

    def provision_for_case(
        self,
        case: CloudCase,
    ) -> list[ComputeResource]:

        allocated = []

        for _ in range(case.desired_instances):
            resource = self.resource_pool.allocate(
                cpu=case.resource_requirements.cpu,
                memory=case.resource_requirements.memory,
            )

            allocated.append(resource)

        return allocated

    def release_resources(
        self,
        resources: list[ComputeResource],
    ) -> None:

        for resource in resources:
            self.resource_pool.release(
                resource.resource_id
            )

    def available_resources(self) -> list[ComputeResource]:
        return [
            resource
            for resource in self.resource_pool.resources
            if not resource.allocated
        ]
