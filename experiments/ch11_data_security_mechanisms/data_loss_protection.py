from experiments.ch11_data_security_mechanisms.models import (
    DataLossEvent,
)


class DataLossProtectionMonitor:

    def __init__(
        self,
        threshold_bytes: int = 100_000_000,
    ):

        self.threshold = threshold_bytes

        self.events: list[
            DataLossEvent
        ] = []

    def analyze(
        self,
        event: DataLossEvent,
    ) -> bool:

        self.events.append(event)

        return (
            event.data_size
            >= self.threshold
        )

    def suspicious_events(
        self,
    ) -> list[DataLossEvent]:

        return [
            event
            for event in self.events
            if event.data_size
            >= self.threshold
        ]