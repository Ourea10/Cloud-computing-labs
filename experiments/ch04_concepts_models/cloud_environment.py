from experiments.ch01_introduction.resource import (
    ComputeResource,
)
from experiments.ch01_introduction.resource_pool import (
    ResourcePool,
)

from tenant import Tenant


class CloudEnvironment:
    def __init__(self):
        self.resource_pool = ResourcePool()

        self.tenants: dict[str, Tenant] = {}

        self.tenant_resources: dict[
            str,
            list[ComputeResource],
        ] = {}

    def register_tenant(
        self,
        tenant: Tenant,
    ):
        if tenant.tenant_id in self.tenants:
            raise ValueError(
                "Tenant already exists"
            )

        self.tenants[tenant.tenant_id] = tenant
        self.tenant_resources[
            tenant.tenant_id
        ] = []

    def add_resource(
        self,
        resource: ComputeResource,
    ):
        self.resource_pool.add(resource)

    def allocate(
        self,
        tenant_id: str,
        cpu: int,
        memory: int,
    ) -> ComputeResource:

        if tenant_id not in self.tenants:
            raise ValueError(
                "Unknown tenant"
            )

        resource = self.resource_pool.allocate(
            cpu=cpu,
            memory=memory,
        )

        self.tenant_resources[
            tenant_id
        ].append(resource)

        return resource

    def release(
        self,
        tenant_id: str,
        resource_id: str,
    ):

        if tenant_id not in self.tenants:
            raise ValueError(
                "Unknown tenant"
            )

        resources = self.tenant_resources[
            tenant_id
        ]

        for resource in resources:
            if resource.resource_id == resource_id:
                self.resource_pool.release(
                    resource_id
                )

                resources.remove(resource)

                return

        raise ValueError(
            "Resource does not belong to tenant"
        )

    def resources_for_tenant(
        self,
        tenant_id: str,
    ) -> list[ComputeResource]:

        if tenant_id not in self.tenants:
            raise ValueError(
                "Unknown tenant"
            )

        return list(
            self.tenant_resources[tenant_id]
        )