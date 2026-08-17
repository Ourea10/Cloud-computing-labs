from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    VIEWER = "viewer"
    OPERATOR = "operator"
    ADMIN = "admin"


@dataclass(frozen=True)
class Principal:
    user_id: str
    tenant_id: str
    role: Role


@dataclass(frozen=True)
class ResourceOwnership:
    resource_id: str
    tenant_id: str


def can_access(
    principal: Principal,
    resource: ResourceOwnership,
) -> bool:

    if principal.role == Role.ADMIN:
        return True

    return (
        principal.tenant_id
        == resource.tenant_id
    )


def can_modify(
    principal: Principal,
    resource: ResourceOwnership,
) -> bool:

    if principal.role in {
        Role.ADMIN,
        Role.OPERATOR,
    }:
        return can_access(
            principal,
            resource,
        )

    return False