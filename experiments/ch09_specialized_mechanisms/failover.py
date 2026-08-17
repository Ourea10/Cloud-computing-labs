from dataclasses import dataclass

from experiments.ch09_specialized_mechanisms.models import (
    FailoverMode,
    FailoverResource,
    ResourceState,
)


@dataclass
class FailoverGroup:

    group_id: str
    mode: FailoverMode
    resources: list[FailoverResource]


class FailoverSystem:

    def __init__(self):

        self.groups: dict[
            str,
            FailoverGroup,
        ] = {}

    def create_group(
        self,
        group_id: str,
        mode: FailoverMode,
        resources: list[FailoverResource],
    ) -> FailoverGroup:

        group = FailoverGroup(
            group_id=group_id,
            mode=mode,
            resources=resources,
        )

        self.groups[group_id] = group

        return group

    def fail(
        self,
        group_id: str,
        resource_id: str,
    ) -> None:

        group = self.groups[
            group_id
        ]

        failed = next(
            resource
            for resource in group.resources
            if resource.resource_id
            == resource_id
        )

        failed.state = ResourceState.FAILED

    def recover(
        self,
        group_id: str,
    ) -> FailoverResource:

        group = self.groups[group_id]

        active = [
            resource
            for resource in group.resources
            if resource.state
            == ResourceState.ACTIVE
        ]

        if group.mode == FailoverMode.ACTIVE_ACTIVE:

            if not active:
                raise RuntimeError(
                    "No active resource available"
                )

            return active[0]

        if active:

            return active[0]

        for resource in group.resources:

            if resource.state == ResourceState.INACTIVE:

                resource.state = (
                    ResourceState.ACTIVE
                )

                return resource

        raise RuntimeError(
            "No passive resource available"
        )