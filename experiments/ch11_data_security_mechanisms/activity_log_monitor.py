from experiments.ch11_data_security_mechanisms.models import (
    ActivityEvent,
)


class ActivityLogMonitor:

    def __init__(self):

        self.events: list[
            ActivityEvent
        ] = []

    def record(
        self,
        event: ActivityEvent,
    ) -> None:

        self.events.append(event)

    def find_by_user(
        self,
        user_id: str,
    ) -> list[ActivityEvent]:

        return [
            event
            for event in self.events
            if event.user_id == user_id
        ]

    def find_by_resource(
        self,
        resource_id: str,
    ) -> list[ActivityEvent]:

        return [
            event
            for event in self.events
            if event.resource_id
            == resource_id
        ]

    def count_action(
        self,
        action: str,
    ) -> int:

        return sum(
            event.action == action
            for event in self.events
        )