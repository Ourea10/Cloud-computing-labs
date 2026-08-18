from datetime import datetime
from uuid import uuid4

from .exceptions import SLANotFoundError

from .models import (
    SLAEvent,
    SLAPolicy,
)


class SLAManagementSystem:

    def __init__(self):

        self.policies: dict[
            str,
            SLAPolicy,
        ] = {}

        self.events: list[
            SLAEvent
        ] = []

    def create_policy(
        self,
        policy: SLAPolicy,
    ) -> SLAPolicy:

        self.policies[
            policy.sla_id
        ] = policy

        return policy

    def get_policy(
        self,
        sla_id: str,
    ) -> SLAPolicy:

        policy = self.policies.get(
            sla_id
        )

        if policy is None:

            raise SLANotFoundError(
                f"SLA {sla_id} not found"
            )

        return policy

    def record_measurement(
        self,
        sla_id: str,
        availability: float,
        response_time_ms: int,
        timestamp: datetime,
    ) -> SLAEvent:

        policy = self.get_policy(
            sla_id
        )

        violations = []

        if (
            availability
            < policy.availability_target
        ):

            violations.append(
                (
                    "availability below "
                    "target"
                )
            )

        if (
            response_time_ms
            > policy.response_time_target_ms
        ):

            violations.append(
                (
                    "response time above "
                    "target"
                )
            )

        event = SLAEvent(
            event_id=str(uuid4()),
            sla_id=sla_id,
            timestamp=timestamp,
            availability=availability,
            response_time_ms=response_time_ms,
            violated=bool(violations),
            reason="; ".join(violations),
        )

        self.events.append(event)

        return event

    def get_violations(
        self,
        sla_id: str,
    ) -> list[SLAEvent]:

        return [
            event
            for event in self.events
            if event.sla_id == sla_id
            and event.violated
        ]