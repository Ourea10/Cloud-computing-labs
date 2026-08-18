from .alert_engine import (
    AlertEngine,
)

from .health_checker import (
    HealthChecker,
)

from .metric_collector import (
    MetricCollector,
)

from .metric_store import (
    MetricStore,
)


class MonitoringService:

    def __init__(self):

        self.collector = (
            MetricCollector()
        )

        self.store = (
            MetricStore()
        )

        self.health_checker = (
            HealthChecker()
        )

        self.alert_engine = (
            AlertEngine()
        )

    def collect(
        self,
        resource_id: str,
    ):

        metrics = (
            self.collector.collect(
                resource_id
            )
        )

        self.store.save_many(
            metrics
        )

        alerts = []

        for metric in metrics:

            alerts.extend(
                self.alert_engine.evaluate(
                    metric
                )
            )

        return metrics, alerts

    def health(
        self,
        resource_id: str,
    ):

        metrics = (
            self.store.get_resource_metrics(
                resource_id
            )
        )

        return (
            self.health_checker.check(
                resource_id,
                metrics,
            )
        )

    def latest(
        self,
        resource_id: str,
    ):

        metrics = (
            self.store.get_resource_metrics(
                resource_id
            )
        )

        return metrics