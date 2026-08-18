from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class AuditAction(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    RESOURCE_CREATE = "resource.create"
    RESOURCE_READ = "resource.read"
    RESOURCE_DELETE = "resource.delete"
    BILLING_READ = "billing.read"
    SECURITY_CHANGE = "security.change"


@dataclass
class User:
    user_id: str
    username: str
    password_hash: str
    role: str
    status: UserStatus = UserStatus.ACTIVE


@dataclass
class Role:
    name: str
    permissions: set[str] = field(
        default_factory=set
    )


@dataclass
class AccessToken:
    token: str
    user_id: str
    expires_at: datetime


@dataclass
class Credential:
    credential_id: str
    user_id: str
    credential_type: str
    encrypted_value: str
    created_at: datetime


@dataclass
class AuditEvent:
    event_id: str
    user_id: str | None
    action: AuditAction
    resource: str | None
    timestamp: datetime
    success: bool
    message: str = ""