from experiments.ch11_data_security_mechanisms.models import (
    TrafficEvent,
)


class TrafficMonitor:

    def __init__(self):

        self.events: list[
            TrafficEvent
        ] = []

    def record(
        self,
        event: TrafficEvent,
    ) -> None:

        self.events.append(event)

    def total_bytes(
        self,
    ) -> int:

        return sum(
            event.bytes_transferred
            for event in self.events
        )

    def bytes_from(
        self,
        source_ip: str,
    ) -> int:

        return sum(
            event.bytes_transferred
            for event in self.events
            if event.source_ip
            == source_ip
        )

    def top_destination(
        self,
    ) -> str | None:

        if not self.events:
            return None

        totals: dict[str, int] = {}

        for event in self.events:

            totals[event.destination_ip] = (
                totals.get(
                    event.destination_ip,
                    0,
                )
                + event.bytes_transferred
            )

        return max(
            totals,
            key=totals.get,
        )