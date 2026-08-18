from datetime import datetime, timezone
from uuid import uuid4

from .models import (
    AuditAction,
    AuditEvent,
)


class AuditLogger:

    def __init__(self):

        self.events: list[
            AuditEvent
        ] = []

    def log(
        self,
        user_id: str | None,
        action: AuditAction,
        resource: str | None,
        success: bool,
        message: str = "",
    ) -> AuditEvent:

        event = AuditEvent(
            event_id=str(uuid4()),
            user_id=user_id,
            action=action,
            resource=resource,
            timestamp=datetime.now(
                timezone.utc
            ),
            success=success,
            message=message,
        )

        self.events.append(event)

        return event

    def get_events_for_user(
        self,
        user_id: str,
    ) -> list[AuditEvent]:

        return [
            event
            for event in self.events
            if event.user_id == user_id
        ]

    def get_failed_events(
        self,
    ) -> list[AuditEvent]:

        return [
            event
            for event in self.events
            if not event.success
        ]