import secrets
from dataclasses import dataclass


@dataclass
class VPNTunnel:
    tunnel_id: str
    client_id: str
    gateway: str
    active: bool = True


class VPNService:

    def __init__(
        self,
        gateway: str,
    ):

        self.gateway = gateway

        self.tunnels: dict[
            str,
            VPNTunnel,
        ] = {}

    def connect(
        self,
        client_id: str,
    ) -> VPNTunnel:

        tunnel = VPNTunnel(
            tunnel_id=secrets.token_hex(16),
            client_id=client_id,
            gateway=self.gateway,
        )

        self.tunnels[
            tunnel.tunnel_id
        ] = tunnel

        return tunnel

    def disconnect(
        self,
        tunnel_id: str,
    ) -> None:

        tunnel = self.tunnels[tunnel_id]

        tunnel.active = False