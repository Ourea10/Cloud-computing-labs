from pydantic import BaseModel


class WorkloadRequest(BaseModel):

    workload_id: str
    name: str

    requires_os_control: bool
    requires_runtime_control: bool
    requires_application_control: bool

    operational_complexity: int
    scalability_requirement: int

    budget: float


class EvaluationRequest(BaseModel):

    workload_id: str
    workload_size: int