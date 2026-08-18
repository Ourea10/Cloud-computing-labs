from experiments.ch10_security_mechanisms.models import (
    NetworkEvent,
)


class NetworkIntrusionMonitor:

    def __init__(self):

        self.events: list[
            NetworkEvent
        ] = []

    def record(
        self,
        event: NetworkEvent,
    ) -> None:

        self.events.append(event)

    def blocked_events(
        self,
    ) -> list[NetworkEvent]:

        return [
            event
            for event in self.events
            if event.blocked
        ]