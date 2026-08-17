from collections import deque

from experiments.ch09_specialized_mechanisms.models import (
    BackendTarget,
    HealthStatus,
)


class LoadBalancer:

    def __init__(self):

        self.targets: dict[
            str,
            BackendTarget,
        ] = {}

        self._rotation = deque()

    def register(
        self,
        target: BackendTarget,
    ) -> None:

        self.targets[
            target.resource_id
        ] = target

        self._rotation.append(
            target.resource_id
        )

    def deregister(
        self,
        resource_id: str,
    ) -> None:

        self.targets.pop(
            resource_id,
            None,
        )

        try:
            self._rotation.remove(
                resource_id
            )
        except ValueError:
            pass

    def mark_healthy(
        self,
        resource_id: str,
    ) -> None:

        self.targets[
            resource_id
        ].health = HealthStatus.HEALTHY

    def mark_unhealthy(
        self,
        resource_id: str,
    ) -> None:

        self.targets[
            resource_id
        ].health = HealthStatus.UNHEALTHY

    def healthy_targets(
        self,
    ) -> list[BackendTarget]:

        return [
            target
            for target in self.targets.values()
            if target.health
            == HealthStatus.HEALTHY
        ]

    def select_target(
        self,
    ) -> BackendTarget:

        for _ in range(
            len(self._rotation)
        ):

            resource_id = (
                self._rotation.popleft()
            )

            self._rotation.append(
                resource_id
            )

            target = self.targets[
                resource_id
            ]

            if (
                target.health
                == HealthStatus.HEALTHY
            ):

                target.active_connections += 1

                return target

        raise RuntimeError(
            "No healthy backend available"
        )

    def release_connection(
        self,
        resource_id: str,
    ) -> None:

        target = self.targets[
            resource_id
        ]

        if target.active_connections > 0:
            target.active_connections -= 1
            
class HealthChecker:

    def check(
        self,
        target: BackendTarget,
        healthy_resource_ids: set[str],
    ) -> HealthStatus:

        if (
            target.resource_id
            in healthy_resource_ids
        ):
            return HealthStatus.HEALTHY

        return HealthStatus.UNHEALTHY