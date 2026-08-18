from pydantic import BaseModel


class CreateVMRequest(BaseModel):

    owner_id: str
    name: str
    cpu: int
    memory_gb: int
    storage_gb: int


class ResourceResponse(BaseModel):

    resource_id: str
    owner_id: str
    name: str
    status: str
    cpu: int
    memory_gb: int
    storage_gb: int
    region: str


class SLARequest(BaseModel):

    sla_id: str
    customer_id: str
    resource_id: str
    availability_target: float
    response_time_target_ms: int
    monthly_price: float


class UsageRequest(BaseModel):

    resource_id: str
    owner_id: str
    resource_type: str
    quantity: float
    unit: str