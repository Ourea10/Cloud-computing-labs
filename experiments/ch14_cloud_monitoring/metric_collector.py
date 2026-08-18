import random
from datetime import datetime, timezone

from .models import Metric, MetricType


class MetricCollector:

    def collect(
        self,
        resource_id: str,
    ) -> list[Metric]:

        now = datetime.now(
            timezone.utc
        )

        return [
            Metric(
                metric_id=(
                    f"{resource_id}-cpu-{now.timestamp()}"
                ),
                resource_id=resource_id,
                metric_type=MetricType.CPU,
                value=round(
                    random.uniform(
                        10,
                        95,
                    ),
                    2,
                ),
                unit="percent",
                timestamp=now,
            ),
            Metric(
                metric_id=(
                    f"{resource_id}-memory-{now.timestamp()}"
                ),
                resource_id=resource_id,
                metric_type=MetricType.MEMORY,
                value=round(
                    random.uniform(
                        20,
                        95,
                    ),
                    2,
                ),
                unit="percent",
                timestamp=now,
            ),
            Metric(
                metric_id=(
                    f"{resource_id}-network-in-{now.timestamp()}"
                ),
                resource_id=resource_id,
                metric_type=MetricType.NETWORK_IN,
                value=round(
                    random.uniform(
                        10,
                        500,
                    ),
                    2,
                ),
                unit="MB/s",
                timestamp=now,
            ),
            Metric(
                metric_id=(
                    f"{resource_id}-network-out-{now.timestamp()}"
                ),
                resource_id=resource_id,
                metric_type=MetricType.NETWORK_OUT,
                value=round(
                    random.uniform(
                        10,
                        500,
                    ),
                    2,
                ),
                unit="MB/s",
                timestamp=now,
            ),
        ]