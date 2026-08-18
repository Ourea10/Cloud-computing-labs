from experiments.ch10_security_mechanisms.models import (
    AuthenticationEvent,
)


class AuthenticationLogMonitor:

    def __init__(self):

        self.events: list[
            AuthenticationEvent
        ] = []

    def record(
        self,
        event: AuthenticationEvent,
    ) -> None:

        self.events.append(event)

    def failed_attempts(
        self,
        user_id: str | None = None,
    ) -> int:

        events = self.events

        if user_id is not None:

            events = [
                event
                for event in events
                if event.user_id == user_id
            ]

        return sum(
            not event.success
            for event in events
        )