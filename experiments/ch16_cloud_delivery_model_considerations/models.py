from dataclasses import dataclass, field

from .enums import (
    DeliveryModel,
    Layer,
    Responsibility,
)


@dataclass
class LayerResponsibility:

    layer: Layer
    responsibility: Responsibility


@dataclass
class DeliveryModelDefinition:

    model: DeliveryModel
    name: str
    description: str

    responsibilities: list[
        LayerResponsibility
    ] = field(default_factory=list)


@dataclass
class Workload:

    workload_id: str
    name: str

    requires_os_control: bool
    requires_runtime_control: bool
    requires_application_control: bool

    operational_complexity: int
    scalability_requirement: int

    budget: float


@dataclass
class DeliveryRecommendation:

    workload_id: str
    model: DeliveryModel
    score: float
    reasons: list[str]


@dataclass
class CostEstimate:

    delivery_model: DeliveryModel

    infrastructure_cost: float
    operations_cost: float
    platform_cost: float

    total_cost: float


@dataclass
class RiskAssessment:

    delivery_model: DeliveryModel

    operational_risk: int
    vendor_lock_in_risk: int
    management_risk: int

    total_risk: int