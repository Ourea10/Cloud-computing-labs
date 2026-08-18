from datetime import datetime, timezone

from .models import (
    HealthStatus,
    MetricType,
    ResourceHealth,
)


class HealthChecker:

    CPU_WARNING = 80
    CPU_CRITICAL = 95

    MEMORY_WARNING = 80
    MEMORY_CRITICAL = 95

    def check(
        self,
        resource_id: str,
        metrics: list,
    ) -> HealthStatus:

        latest = {
            metric.metric_type: metric
            for metric in metrics
            if metric.resource_id
            == resource_id
        }

        cpu = latest.get(
            MetricType.CPU
        )

        memory = latest.get(
            MetricType.MEMORY
        )

        checks = {
            "cpu": (
                cpu is not None
            ),
            "memory": (
                memory is not None
            ),
        }

        if not cpu or not memory:

            status = (
                ResourceHealth.UNKNOWN
            )

        elif (
            cpu.value
            >= self.CPU_CRITICAL
            or memory.value
            >= self.MEMORY_CRITICAL
        ):

            status = (
                ResourceHealth.CRITICAL
            )

        elif (
            cpu.value
            >= self.CPU_WARNING
            or memory.value
            >= self.MEMORY_WARNING
        ):

            status = (
                ResourceHealth.WARNING
            )

        else:

            status = (
                ResourceHealth.HEALTHY
            )

        return HealthStatus(
            resource_id=resource_id,
            status=status,
            checks=checks,
            timestamp=datetime.now(
                timezone.utc
            ),
        )