from fastapi import APIRouter, Depends

from .dependencies import (
    require_permission,
)

from .schemas import (
    AlertResponse,
    HealthResponse,
    MetricResponse,
)

from ..monitoring_service import (
    MonitoringService,
)


router = APIRouter()

monitoring = (
    MonitoringService()
)


@router.post(
    "/resources/{resource_id}/metrics",
)
def collect_metrics(
    resource_id: str,
    user=Depends(
        require_permission(
            "monitoring:manage"
        )
    ),
):

    metrics, alerts = (
        monitoring.collect(
            resource_id
        )
    )

    return {
        "resource_id": resource_id,
        "metrics": [
            {
                "metric_id": metric.metric_id,
                "metric_type": (
                    metric.metric_type.value
                ),
                "value": metric.value,
                "unit": metric.unit,
                "timestamp": (
                    metric.timestamp.isoformat()
                ),
            }
            for metric in metrics
        ],
        "alerts": [
            {
                "alert_id": alert.alert_id,
                "severity": (
                    alert.severity.value
                ),
                "message": alert.message,
                "value": alert.value,
                "threshold": alert.threshold,
            }
            for alert in alerts
        ],
    }


@router.get(
    "/resources/{resource_id}/metrics",
)
def get_metrics(
    resource_id: str,
    user=Depends(
        require_permission(
            "monitoring:read"
        )
    ),
):

    metrics = monitoring.latest(
        resource_id
    )

    return [
        {
            "metric_id": metric.metric_id,
            "metric_type": (
                metric.metric_type.value
            ),
            "value": metric.value,
            "unit": metric.unit,
            "timestamp": (
                metric.timestamp.isoformat()
            ),
        }
        for metric in metrics
    ]


@router.get(
    "/resources/{resource_id}/health",
)
def get_health(
    resource_id: str,
    user=Depends(
        require_permission(
            "monitoring:read"
        )
    ),
):

    health = monitoring.health(
        resource_id
    )

    return {
        "resource_id": (
            health.resource_id
        ),
        "status": (
            health.status.value
        ),
        "checks": health.checks,
        "timestamp": (
            health.timestamp.isoformat()
        ),
    }


@router.get(
    "/alerts",
)
def get_alerts(
    user=Depends(
        require_permission(
            "monitoring:read"
        )
    ),
):

    return [
        {
            "alert_id": alert.alert_id,
            "resource_id": alert.resource_id,
            "metric_type": (
                alert.metric_type.value
            ),
            "value": alert.value,
            "threshold": alert.threshold,
            "severity": (
                alert.severity.value
            ),
            "status": (
                alert.status.value
            ),
            "message": alert.message,
        }
        for alert
        in monitoring.alert_engine.alerts
    ]