from experiments.ch09_specialized_mechanisms.models import (
    ClusterMember,
    ResourceState,
)


class ResourceCluster:

    def __init__(
        self,
        cluster_id: str,
    ):

        self.cluster_id = cluster_id

        self.members: dict[
            str,
            ClusterMember,
        ] = {}

    def add(
        self,
        resource_id: str,
    ) -> ClusterMember:

        member = ClusterMember(
            resource_id=resource_id
        )

        self.members[
            resource_id
        ] = member

        return member

    def remove(
        self,
        resource_id: str,
    ) -> None:

        self.members.pop(
            resource_id,
            None,
        )

    def mark_failed(
        self,
        resource_id: str,
    ) -> None:

        self.members[
            resource_id
        ].state = ResourceState.FAILED

    def active_members(
        self,
    ) -> list[ClusterMember]:

        return [
            member
            for member in self.members.values()
            if member.state
            == ResourceState.ACTIVE
        ]

    def health_ratio(self) -> float:

        if not self.members:
            return 0.0

        active = len(
            self.active_members()
        )

        return active / len(
            self.members
        )

    def is_healthy(
        self,
        minimum_ratio: float = 0.5,
    ) -> bool:

        return (
            self.health_ratio()
            >= minimum_ratio
        )