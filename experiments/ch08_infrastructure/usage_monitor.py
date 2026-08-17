from dataclasses import dataclass
from datetime import datetime, timezone

from experiments.ch08_infrastructure.models import (
    ResourceUsage,
)


@dataclass(frozen=True)
class UsageRecord:

    timestamp: datetime

    usage: ResourceUsage


class CloudUsageMonitor:

    def __init__(self):

        self.records: list[
            UsageRecord
        ] = []

    def record(
        self,
        usage: ResourceUsage,
    ) -> UsageRecord:

        record = UsageRecord(
            timestamp=datetime.now(
                timezone.utc
            ),
            usage=usage,
        )

        self.records.append(record)

        return record

    def get_resource_usage(
        self,
        resource_id: str,
    ) -> list[UsageRecord]:

        return [
            record
            for record in self.records
            if record.usage.resource_id
            == resource_id
        ]

    def latest(
        self,
        resource_id: str,
    ) -> UsageRecord | None:

        records = self.get_resource_usage(
            resource_id
        )

        if not records:
            return None

        return records[-1]