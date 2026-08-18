from uuid import uuid4

from .exceptions import (
    ResourceNotFoundError,
    ResourceQuotaExceededError,
)

from .models import (
    Resource,
    ResourceQuota,
    ResourceStatus,
    ResourceType,
    ResourceUsage,
)


class ResourceManagementSystem:

    def __init__(self):

        self.resources: dict[
            str,
            Resource,
        ] = {}

        self.quotas: dict[
            str,
            ResourceQuota,
        ] = {}

    def set_quota(
        self,
        quota: ResourceQuota,
    ) -> None:

        self.quotas[
            quota.owner_id
        ] = quota

    def get_usage(
        self,
        owner_id: str,
    ) -> ResourceUsage:

        owner_resources = [
            resource
            for resource in self.resources.values()
            if resource.owner_id == owner_id
            and resource.status
            != ResourceStatus.TERMINATED
        ]

        return ResourceUsage(
            owner_id=owner_id,
            cpu=sum(
                resource.cpu
                for resource in owner_resources
            ),
            memory_gb=sum(
                resource.memory_gb
                for resource in owner_resources
            ),
            storage_gb=sum(
                resource.storage_gb
                for resource in owner_resources
            ),
        )

    def _check_quota(
        self,
        owner_id: str,
        cpu: int,
        memory_gb: int,
        storage_gb: int,
    ) -> None:

        quota = self.quotas.get(
            owner_id
        )

        if quota is None:

            raise ResourceQuotaExceededError(
                f"No quota configured "
                f"for {owner_id}"
            )

        usage = self.get_usage(
            owner_id
        )

        if (
            usage.cpu + cpu
            > quota.max_cpu
        ):

            raise ResourceQuotaExceededError(
                "CPU quota exceeded"
            )

        if (
            usage.memory_gb + memory_gb
            > quota.max_memory_gb
        ):

            raise ResourceQuotaExceededError(
                "Memory quota exceeded"
            )

        if (
            usage.storage_gb + storage_gb
            > quota.max_storage_gb
        ):

            raise ResourceQuotaExceededError(
                "Storage quota exceeded"
            )

    def create_resource(
        self,
        owner_id: str,
        resource_type: ResourceType,
        name: str,
        cpu: int = 0,
        memory_gb: int = 0,
        storage_gb: int = 0,
        region: str = "local",
    ) -> Resource:

        self._check_quota(
            owner_id=owner_id,
            cpu=cpu,
            memory_gb=memory_gb,
            storage_gb=storage_gb,
        )

        resource = Resource(
            resource_id=str(uuid4()),
            owner_id=owner_id,
            resource_type=resource_type,
            name=name,
            status=ResourceStatus.PROVISIONING,
            cpu=cpu,
            memory_gb=memory_gb,
            storage_gb=storage_gb,
            region=region,
        )

        self.resources[
            resource.resource_id
        ] = resource

        return resource

    def delete_resource(
        self,
        resource_id: str,
    ) -> None:

        resource = self.resources.get(
            resource_id
        )

        if resource is None:

            raise ResourceNotFoundError(
                f"Resource {resource_id} "
                "not found"
            )

        resource.status = (
            ResourceStatus.TERMINATED
        )

    def list_resources(
        self,
        owner_id: str | None = None,
    ) -> list[Resource]:

        resources = list(
            self.resources.values()
        )

        if owner_id is None:
            return resources

        return [
            resource
            for resource in resources
            if resource.owner_id == owner_id
        ]