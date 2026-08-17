import ipaddress

from experiments.ch08_infrastructure.models import (
    ServerState,
    VirtualServer,
)


class VirtualServerManager:

    def __init__(
        self,
        network_prefix: str = "10.0.0.0/24",
    ):
        self.network = ipaddress.ip_network(
            network_prefix
        )

        self._allocated_ips: set[str] = set()

    def _allocate_ip(self) -> str:

        for ip in self.network.hosts():

            address = str(ip)

            if address not in self._allocated_ips:

                self._allocated_ips.add(
                    address
                )

                return address

        raise RuntimeError(
            "No private IP addresses available"
        )

    def create(
        self,
        server_id: str,
        tenant_id: str,
        cpu_cores: int,
        memory_mb: int,
        image: str,
    ) -> VirtualServer:

        server = VirtualServer(
            server_id=server_id,
            tenant_id=tenant_id,
            cpu_cores=cpu_cores,
            memory_mb=memory_mb,
            image=image,
            private_ip=self._allocate_ip(),
        )

        return server

    def start(
        self,
        server: VirtualServer,
    ) -> None:

        if server.state == ServerState.FAILED:
            raise RuntimeError(
                "Failed server cannot be started"
            )

        server.state = ServerState.RUNNING

    def stop(
        self,
        server: VirtualServer,
    ) -> None:

        server.state = ServerState.STOPPED