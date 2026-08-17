from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    event_type: str
    actor: str
    resource: str
    action: str
    outcome: str
    details: str = ""


class AuditLogger:
    def __init__(self):
        self.events: list[AuditEvent] = []

    def record(
        self,
        event_type: str,
        actor: str,
        resource: str,
        action: str,
        outcome: str,
        details: str = "",
    ) -> AuditEvent:

        event = AuditEvent(
            timestamp=datetime.now(timezone.utc),
            event_type=event_type,
            actor=actor,
            resource=resource,
            action=action,
            outcome=outcome,
            details=details,
        )

        self.events.append(event)

        return event

    def failed_events(self) -> list[AuditEvent]:
        return [
            event
            for event in self.events
            if event.outcome == "denied"
        ]