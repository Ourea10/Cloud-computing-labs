from fastapi import APIRouter

from ...schemas import MetricCreate

from ...services.monitoring_service import (
    MonitoringService,
)

from ..dependencies import (
    metric_repository,
)


router = APIRouter()

service = MonitoringService(
    metric_repository
)


@router.post(
    "/{resource_id}/metrics"
)
def record_metric(
    resource_id: str,
    request: MetricCreate,
):

    return service.record(
        resource_id=resource_id,
        cpu_usage=request.cpu_usage,
        memory_usage=request.memory_usage,
    )


@router.get(
    "/{resource_id}/metrics"
)
def metrics(
    resource_id: str,
):

    return service.get_metrics(
        resource_id
    )