from datetime import datetime, timezone
from uuid import uuid4

from .exceptions import (
    InvalidResourceOperationError,
    ResourceNotFoundError,
)

from .models import (
    OperationStatus,
    Resource,
    ResourceOperation,
    ResourceStatus,
)


class RemoteAdministrationSystem:

    def __init__(
        self,
        resources: dict[str, Resource],
    ):

        self.resources = resources

        self.operations: list[
            ResourceOperation
        ] = []

    def _get_resource(
        self,
        resource_id: str,
    ) -> Resource:

        resource = self.resources.get(
            resource_id
        )

        if resource is None:

            raise ResourceNotFoundError(
                f"Resource {resource_id} "
                "does not exist"
            )

        return resource

    def _record_operation(
        self,
        resource_id: str,
        operation: str,
        status: OperationStatus,
        message: str = "",
    ) -> ResourceOperation:

        result = ResourceOperation(
            operation_id=str(uuid4()),
            resource_id=resource_id,
            operation=operation,
            status=status,
            created_at=datetime.now(
                timezone.utc
            ),
            message=message,
        )

        self.operations.append(result)

        return result

    def start(
        self,
        resource_id: str,
    ) -> ResourceOperation:

        resource = self._get_resource(
            resource_id
        )

        if resource.status not in (
            ResourceStatus.STOPPED,
            ResourceStatus.PROVISIONING,
        ):

            return self._record_operation(
                resource_id,
                "start",
                OperationStatus.FAILED,
                (
                    f"Cannot start resource "
                    f"in state {resource.status}"
                ),
            )

        resource.status = (
            ResourceStatus.RUNNING
        )

        return self._record_operation(
            resource_id,
            "start",
            OperationStatus.SUCCESS,
            "Resource started",
        )

    def stop(
        self,
        resource_id: str,
    ) -> ResourceOperation:

        resource = self._get_resource(
            resource_id
        )

        if resource.status != (
            ResourceStatus.RUNNING
        ):

            return self._record_operation(
                resource_id,
                "stop",
                OperationStatus.FAILED,
                (
                    "Only running resources "
                    "can be stopped"
                ),
            )

        resource.status = (
            ResourceStatus.STOPPED
        )

        return self._record_operation(
            resource_id,
            "stop",
            OperationStatus.SUCCESS,
            "Resource stopped",
        )

    def restart(
        self,
        resource_id: str,
    ) -> ResourceOperation:

        resource = self._get_resource(
            resource_id
        )

        if resource.status != (
            ResourceStatus.RUNNING
        ):

            return self._record_operation(
                resource_id,
                "restart",
                OperationStatus.FAILED,
                (
                    "Only running resources "
                    "can be restarted"
                ),
            )

        resource.status = (
            ResourceStatus.STOPPED
        )

        resource.status = (
            ResourceStatus.RUNNING
        )

        return self._record_operation(
            resource_id,
            "restart",
            OperationStatus.SUCCESS,
            "Resource restarted",
        )

    def terminate(
        self,
        resource_id: str,
    ) -> ResourceOperation:

        resource = self._get_resource(
            resource_id
        )

        if resource.status == (
            ResourceStatus.TERMINATED
        ):

            raise InvalidResourceOperationError(
                "Resource already terminated"
            )

        resource.status = (
            ResourceStatus.TERMINATED
        )

        return self._record_operation(
            resource_id,
            "terminate",
            OperationStatus.SUCCESS,
            "Resource terminated",
        )

    def inspect(
        self,
        resource_id: str,
    ) -> Resource:

        return self._get_resource(
            resource_id
        )