from pydantic import BaseModel


class UserCreate(BaseModel):

    email: str
    password: str


class LoginRequest(BaseModel):

    email: str
    password: str


class ProjectCreate(BaseModel):

    name: str
    description: str = ""


class ResourceCreate(BaseModel):

    name: str
    resource_type: str


class MetricCreate(BaseModel):

    cpu_usage: float
    memory_usage: float


class AlertCreate(BaseModel):

    metric: str
    threshold: float