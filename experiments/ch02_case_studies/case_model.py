from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceRequirement:
    cpu: int
    memory: int


@dataclass(frozen=True)
class CloudCase:
    name: str
    resource_requirements: ResourceRequirement
    desired_instances: int
    characteristics: list[str]