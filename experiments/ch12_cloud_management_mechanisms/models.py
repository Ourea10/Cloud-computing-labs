from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ResourceType(str, Enum):
    VM = "vm"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"


class ResourceStatus(str, Enum):
    PROVISIONING = "provisioning"
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"


class OperationStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


@dataclass
class Resource:
    resource_id: str
    owner_id: str
    resource_type: ResourceType
    name: str
    status: ResourceStatus
    cpu: int = 0
    memory_gb: int = 0
    storage_gb: int = 0
    region: str = "local"


@dataclass
class ResourceOperation:
    operation_id: str
    resource_id: str
    operation: str
    status: OperationStatus
    created_at: datetime
    message: str = ""


@dataclass
class ResourceQuota:
    owner_id: str
    max_cpu: int
    max_memory_gb: int
    max_storage_gb: int


@dataclass
class ResourceUsage:
    owner_id: str
    cpu: int
    memory_gb: int
    storage_gb: int


@dataclass
class SLAPolicy:
    sla_id: str
    customer_id: str
    resource_id: str
    availability_target: float
    response_time_target_ms: int
    monthly_price: float


@dataclass
class SLAEvent:
    event_id: str
    sla_id: str
    timestamp: datetime
    availability: float
    response_time_ms: int
    violated: bool
    reason: str = ""


@dataclass
class PricingRule:
    resource_type: ResourceType
    unit: str
    price_per_unit: float


@dataclass
class UsageRecord:
    resource_id: str
    owner_id: str
    resource_type: ResourceType
    quantity: float
    unit: str
    timestamp: datetime


@dataclass
class InvoiceItem:
    description: str
    quantity: float
    unit_price: float
    amount: float


@dataclass
class Invoice:
    invoice_id: str
    customer_id: str
    period: str
    items: list[InvoiceItem] = field(
        default_factory=list
    )
    total: float = 0.0