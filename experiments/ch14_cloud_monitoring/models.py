from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MetricType(str, Enum):
    CPU = "cpu"
    MEMORY = "memory"
    NETWORK_IN = "network_in"
    NETWORK_OUT = "network_out"


class ResourceHealth(str, Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"


@dataclass
class Metric:
    metric_id: str
    resource_id: str
    metric_type: MetricType
    value: float
    unit: str
    timestamp: datetime


@dataclass
class AlertRule:
    rule_id: str
    resource_id: str | None
    metric_type: MetricType
    operator: str
    threshold: float
    severity: AlertSeverity
    message: str


@dataclass
class Alert:
    alert_id: str
    rule_id: str
    resource_id: str
    metric_type: MetricType
    value: float
    threshold: float
    severity: AlertSeverity
    status: AlertStatus
    message: str
    created_at: datetime
    resolved_at: datetime | None = None


@dataclass
class HealthStatus:
    resource_id: str
    status: ResourceHealth
    checks: dict[str, bool]
    timestamp: datetime