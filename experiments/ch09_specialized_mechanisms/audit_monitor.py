import json
from pathlib import Path

from experiments.ch09_specialized_mechanisms.models import (
    AuditEvent,
    utc_now,
)


class AuditMonitor:

    def __init__(
        self,
        log_file: str = "audit.log",
    ):

        self.log_file = Path(
            log_file
        )

        self.events: list[
            AuditEvent
        ] = []

    def record(
        self,
        actor: str,
        tenant_id: str | None,
        action: str,
        resource_type: str,
        resource_id: str | None,
        success: bool,
        metadata: dict | None = None,
    ) -> AuditEvent:

        event = AuditEvent(
            timestamp=utc_now(),
            actor=actor,
            tenant_id=tenant_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            success=success,
            metadata=metadata or {},
        )

        self.events.append(event)

        self._append_to_file(event)

        return event

    def _append_to_file(
        self,
        event: AuditEvent,
    ) -> None:

        payload = {
            "timestamp": (
                event.timestamp.isoformat()
            ),
            "actor": event.actor,
            "tenant_id": event.tenant_id,
            "action": event.action,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "success": event.success,
            "metadata": event.metadata,
        }

        with self.log_file.open(
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                json.dumps(payload)
                + "\n"
            )

    def find_by_actor(
        self,
        actor: str,
    ) -> list[AuditEvent]:

        return [
            event
            for event in self.events
            if event.actor == actor
        ]

    def find_by_resource(
        self,
        resource_id: str,
    ) -> list[AuditEvent]:

        return [
            event
            for event in self.events
            if event.resource_id
            == resource_id
        ]