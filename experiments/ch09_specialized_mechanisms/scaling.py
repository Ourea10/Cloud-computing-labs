from experiments.ch08_infrastructure.models import (
    VirtualServer,
)

from experiments.ch09_specialized_mechanisms.models import (
    ScalingDirection,
    ScalingEvent,
    ScalingPolicy,
    utc_now,
)

from experiments.ch08_infrastructure.infrastructure import (
    CloudInfrastructure,
)

class AutomatedScalingListener:

    def __init__(
        self,
        policy: ScalingPolicy,
    ):
        self.policy = policy

        self.events: list[
            ScalingEvent
        ] = []

    def evaluate(
        self,
        resource_group: str,
        cpu_percent: float,
        current_count: int,
    ) -> ScalingEvent | None:

        if (
            cpu_percent
            > self.policy.scale_out_threshold
            and current_count
            < self.policy.max_instances
        ):

            new_count = current_count + 1

            event = ScalingEvent(
                timestamp=utc_now(),
                direction=ScalingDirection.SCALE_OUT,
                resource_group=resource_group,
                previous_count=current_count,
                new_count=new_count,
                reason=(
                    f"CPU {cpu_percent}% "
                    f"> threshold "
                    f"{self.policy.scale_out_threshold}%"
                ),
            )

            self.events.append(event)

            return event

        if (
            cpu_percent
            < self.policy.scale_in_threshold
            and current_count
            > self.policy.min_instances
        ):

            new_count = current_count - 1

            event = ScalingEvent(
                timestamp=utc_now(),
                direction=ScalingDirection.SCALE_IN,
                resource_group=resource_group,
                previous_count=current_count,
                new_count=new_count,
                reason=(
                    f"CPU {cpu_percent}% "
                    f"< threshold "
                    f"{self.policy.scale_in_threshold}%"
                ),
            )

            self.events.append(event)

            return event

        return None


class ScalingController:

    def __init__(
        self,
        listener: AutomatedScalingListener,
    ):
        self.listener = listener

    def reconcile(
        self,
        resource_group: str,
        servers: list[VirtualServer],
        cpu_percent: float,
    ) -> ScalingEvent | None:

        return self.listener.evaluate(
            resource_group=resource_group,
            cpu_percent=cpu_percent,
            current_count=len(servers),
        )
        
class InfrastructureScaler:

    def __init__(
        self,
        cloud: CloudInfrastructure,
        controller: ScalingController,
    ):
        self.cloud = cloud
        self.controller = controller

    def reconcile(
        self,
        resource_group: str,
        servers: list[VirtualServer],
        cpu_percent: float,
        tenant_id: str,
        image: str,
        cpu: int,
        memory_mb: int,
    ):

        event = self.controller.reconcile(
            resource_group=resource_group,
            servers=servers,
            cpu_percent=cpu_percent,
        )

        if event is None:
            return None

        if (
            event.direction
            == ScalingDirection.SCALE_OUT
        ):

            server_id = (
                f"{resource_group}-"
                f"{event.new_count}"
            )

            server = self.cloud.create_server(
                server_id=server_id,
                tenant_id=tenant_id,
                cpu=cpu,
                memory_mb=memory_mb,
                image=image,
            )

            return server

        return event