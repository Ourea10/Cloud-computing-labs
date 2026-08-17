from dataclasses import dataclass

from experiments.ch08_infrastructure.models import (
    ServerState,
    VirtualServer,
)


@dataclass
class PhysicalHost:

    host_id: str

    total_cpu: int
    total_memory_mb: int

    used_cpu: int = 0
    used_memory_mb: int = 0

    def available_cpu(self) -> int:
        return self.total_cpu - self.used_cpu

    def available_memory(self) -> int:
        return (
            self.total_memory_mb
            - self.used_memory_mb
        )


class Hypervisor:

    def __init__(
        self,
        host: PhysicalHost,
    ):
        self.host = host

        self.virtual_servers: dict[
            str,
            VirtualServer,
        ] = {}

    def can_allocate(
        self,
        cpu: int,
        memory_mb: int,
    ) -> bool:

        return (
            self.host.available_cpu()
            >= cpu
            and
            self.host.available_memory()
            >= memory_mb
        )

    def create_vm(
        self,
        server: VirtualServer,
    ) -> VirtualServer:

        if not self.can_allocate(
            server.cpu_cores,
            server.memory_mb,
        ):
            raise RuntimeError(
                "Insufficient physical resources"
            )

        self.host.used_cpu += (
            server.cpu_cores
        )

        self.host.used_memory_mb += (
            server.memory_mb
        )

        self.virtual_servers[
            server.server_id
        ] = server

        server.state = ServerState.RUNNING

        return server

    def destroy_vm(
        self,
        server_id: str,
    ) -> None:

        server = self.virtual_servers.pop(
            server_id
        )

        self.host.used_cpu -= (
            server.cpu_cores
        )

        self.host.used_memory_mb -= (
            server.memory_mb
        )

        server.state = ServerState.STOPPED