from datetime import datetime

from ..models import Metric
from ..repositories.metric_repository import (
    MetricRepository,
)


class MonitoringService:

    def __init__(
        self,
        repository: MetricRepository,
    ):

        self.repository = repository

    def record(
        self,
        resource_id,
        cpu_usage,
        memory_usage,
    ):

        metric = Metric(
            resource_id=resource_id,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            timestamp=datetime.utcnow(),
        )

        self.repository.save(
            metric
        )

        return metric

    def get_metrics(
        self,
        resource_id,
    ):

        return (
            self.repository
            .list_by_resource(
                resource_id
            )
        )