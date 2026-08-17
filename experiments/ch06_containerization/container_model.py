from dataclasses import dataclass


@dataclass
class Container:
    container_id: str
    image: str
    cpu_limit: float
    memory_limit_mb: int
    running: bool = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


@dataclass
class ContainerHost:
    host_id: str
    cpu: float
    memory_mb: int

    containers: list[Container] | None = None

    def __post_init__(self):
        if self.containers is None:
            self.containers = []

    @property
    def used_cpu(self):
        return sum(
            container.cpu_limit
            for container in self.containers
            if container.running
        )

    @property
    def used_memory(self):
        return sum(
            container.memory_limit_mb
            for container in self.containers
            if container.running
        )

    def run_container(
        self,
        container: Container,
    ):
        if (
            self.used_cpu
            + container.cpu_limit
            > self.cpu
        ):
            raise RuntimeError(
                "Insufficient CPU"
            )

        if (
            self.used_memory
            + container.memory_limit_mb
            > self.memory_mb
        ):
            raise RuntimeError(
                "Insufficient memory"
            )

        container.start()

        self.containers.append(
            container
        )