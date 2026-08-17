from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    user_id: str
    username: str
    tenant_id: str
    role: str


@dataclass(frozen=True)
class Resource:
    resource_id: str
    tenant_id: str
    name: str


USERS = {
    "alice": User(
        user_id="user-001",
        username="alice",
        tenant_id="tenant-a",
        role="viewer",
    ),
    "bob": User(
        user_id="user-002",
        username="bob",
        tenant_id="tenant-b",
        role="operator",
    ),
    "admin": User(
        user_id="user-003",
        username="admin",
        tenant_id="platform",
        role="admin",
    ),
}


RESOURCES = {
    "resource-a": Resource(
        resource_id="resource-a",
        tenant_id="tenant-a",
        name="Tenant A API Server",
    ),
    "resource-b": Resource(
        resource_id="resource-b",
        tenant_id="tenant-b",
        name="Tenant B API Server",
    ),
}