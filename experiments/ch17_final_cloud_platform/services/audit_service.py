from datetime import datetime


class AuditService:

    def __init__(self):

        self.events = []

    def record(
        self,
        actor_id,
        action,
        resource_id=None,
    ):

        event = {
            "actor_id": actor_id,
            "action": action,
            "resource_id": resource_id,
            "timestamp": datetime.utcnow()
            .isoformat(),
        }

        self.events.append(
            event
        )

        return event

    def list_events(self):

        return self.events