from experiments.ch08_infrastructure.models import (
    ContainerInstance,
)


class ContainerManager:

    def __init__(self):

        self.containers: dict[
            str,
            ContainerInstance,
        ] = {}

    def create(
        self,
        container_id: str,
        tenant_id: str,
        image: str,
        cpu_limit: float,
        memory_limit_mb: int,
        server_id: str,
    ) -> ContainerInstance:

        if container_id in self.containers:
            raise ValueError(
                "Container already exists"
            )

        if cpu_limit <= 0:
            raise ValueError(
                "CPU limit must be positive"
            )

        if memory_limit_mb <= 0:
            raise ValueError(
                "Memory limit must be positive"
            )

        container = ContainerInstance(
            container_id=container_id,
            tenant_id=tenant_id,
            image=image,
            cpu_limit=cpu_limit,
            memory_limit_mb=memory_limit_mb,
            server_id=server_id,
        )

        self.containers[
            container_id
        ] = container

        return container

    def start(
        self,
        container_id: str,
    ) -> None:

        container = self.containers[
            container_id
        ]

        container.running = True

    def stop(
        self,
        container_id: str,
    ) -> None:

        container = self.containers[
            container_id
        ]

        container.running = False