from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:

    id: str
    email: str
    password_hash: str


@dataclass
class Project:

    id: str
    owner_id: str
    name: str
    description: str


@dataclass
class Resource:

    id: str
    project_id: str
    name: str
    resource_type: str
    status: str


@dataclass
class Metric:

    resource_id: str
    cpu_usage: float
    memory_usage: float
    timestamp: datetime


@dataclass
class Alert:

    id: str
    resource_id: str
    metric: str
    threshold: float
    triggered: bool