from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any


class ScalingDirection(str, Enum):
    SCALE_OUT = "scale_out"
    SCALE_IN = "scale_in"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


class FailoverMode(str, Enum):
    ACTIVE_ACTIVE = "active_active"
    ACTIVE_PASSIVE = "active_passive"


class ResourceState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"


class DeviceType(str, Enum):
    SERVER = "server"
    CONTAINER = "container"
    STORAGE = "storage"
    CLIENT = "client"


@dataclass(frozen=True)
class ScalingPolicy:
    min_instances: int
    max_instances: int
    scale_out_threshold: float
    scale_in_threshold: float


@dataclass(frozen=True)
class ScalingEvent:
    timestamp: datetime
    direction: ScalingDirection
    resource_group: str
    previous_count: int
    new_count: int
    reason: str


@dataclass
class BackendTarget:
    resource_id: str
    address: str
    port: int

    health: HealthStatus = HealthStatus.UNKNOWN
    weight: int = 1

    active_connections: int = 0


@dataclass(frozen=True)
class SLAObjective:
    name: str
    target: float
    metric: str


@dataclass(frozen=True)
class SLAObservation:
    timestamp: datetime
    metric: str
    value: float
    target: float
    passed: bool


@dataclass(frozen=True)
class PricingRule:
    resource_type: str
    unit: str
    price_per_unit: float


@dataclass(frozen=True)
class UsageEvent:
    timestamp: datetime
    tenant_id: str
    resource_id: str
    resource_type: str
    quantity: float
    unit: str


@dataclass(frozen=True)
class AuditEvent:
    timestamp: datetime
    actor: str
    tenant_id: str | None
    action: str
    resource_type: str
    resource_id: str | None
    success: bool
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class FailoverResource:
    resource_id: str
    address: str
    state: ResourceState = ResourceState.ACTIVE


@dataclass
class ClusterMember:
    resource_id: str
    state: ResourceState = ResourceState.ACTIVE


@dataclass
class Device:
    device_id: str
    device_type: DeviceType
    endpoint: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)