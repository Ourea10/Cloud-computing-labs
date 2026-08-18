from experiments.ch10_security_mechanisms.vpn import (
    VPNService,
)


class VPNMonitor:

    def __init__(
        self,
        vpn: VPNService,
    ):

        self.vpn = vpn

    def active_tunnels(self) -> int:

        return sum(
            tunnel.active
            for tunnel in self.vpn.tunnels.values()
        )

    def disconnected_tunnels(self) -> int:

        return sum(
            not tunnel.active
            for tunnel in self.vpn.tunnels.values()
        )