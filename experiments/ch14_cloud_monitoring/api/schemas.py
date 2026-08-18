from pydantic import BaseModel


class MetricResponse(BaseModel):

    metric_id: str
    resource_id: str
    metric_type: str
    value: float
    unit: str
    timestamp: str


class HealthResponse(BaseModel):

    resource_id: str
    status: str
    checks: dict[str, bool]
    timestamp: str


class AlertResponse(BaseModel):

    alert_id: str
    resource_id: str
    metric_type: str
    value: float
    threshold: float
    severity: str
    status: str
    message: str