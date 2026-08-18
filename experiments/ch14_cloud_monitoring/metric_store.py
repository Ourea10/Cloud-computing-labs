from datetime import datetime

from .models import Metric


class MetricStore:

    def __init__(self):

        self.metrics: list[Metric] = []

    def save(
        self,
        metric: Metric,
    ) -> None:

        self.metrics.append(
            metric
        )

    def save_many(
        self,
        metrics: list[Metric],
    ) -> None:

        self.metrics.extend(
            metrics
        )

    def get_resource_metrics(
        self,
        resource_id: str,
    ) -> list[Metric]:

        return [
            metric
            for metric in self.metrics
            if metric.resource_id
            == resource_id
        ]

    def get_latest(
        self,
        resource_id: str,
        metric_type,
    ) -> Metric | None:

        matching = [
            metric
            for metric in self.metrics
            if (
                metric.resource_id
                == resource_id
                and metric.metric_type
                == metric_type
            )
        ]

        if not matching:
            return None

        return max(
            matching,
            key=lambda metric:
            metric.timestamp,
        )

    def get_between(
        self,
        resource_id: str,
        start: datetime,
        end: datetime,
    ) -> list[Metric]:

        return [
            metric
            for metric in self.metrics
            if (
                metric.resource_id
                == resource_id
                and start
                <= metric.timestamp
                <= end
            )
        ]