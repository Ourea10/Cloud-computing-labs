from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkEndpoint:
    host: str
    port: int


@dataclass
class NetworkRequest:
    source: NetworkEndpoint
    destination: NetworkEndpoint
    payload_size_bytes: int


class NetworkPath:
    def __init__(
        self,
        latency_ms: float,
        bandwidth_mbps: float,
    ):
        self.latency_ms = latency_ms
        self.bandwidth_mbps = bandwidth_mbps

    def transfer_time_ms(
        self,
        payload_size_bytes: int,
    ) -> float:

        payload_bits = (
            payload_size_bytes * 8
        )

        bandwidth_bits_per_ms = (
            self.bandwidth_mbps * 1_000_000
        ) / 1_000

        transmission_time = (
            payload_bits
            / bandwidth_bits_per_ms
        )

        return (
            self.latency_ms
            + transmission_time
        )