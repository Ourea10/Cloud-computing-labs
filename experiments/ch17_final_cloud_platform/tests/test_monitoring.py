from ..repositories.metric_repository import (
    MetricRepository,
)

from ..services.monitoring_service import (
    MonitoringService,
)


def test_record_metric():

    repository = MetricRepository()

    service = MonitoringService(
        repository
    )

    metric = service.record(
        resource_id="resource-1",
        cpu_usage=80,
        memory_usage=60,
    )

    assert metric.cpu_usage == 80

    metrics = service.get_metrics(
        "resource-1"
    )

    assert len(metrics) == 1