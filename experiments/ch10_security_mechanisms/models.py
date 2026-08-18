from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class EncryptionMode(str, Enum):
    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"


class AccessDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


class SecurityEventType(str, Enum):
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NETWORK = "network"
    INTRUSION = "intrusion"
    VPN = "vpn"
    MFA = "mfa"


class UserStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    LOCKED = "locked"


@dataclass(frozen=True)
class EncryptedData:
    algorithm: str
    ciphertext: str


@dataclass(frozen=True)
class HashResult:
    algorithm: str
    digest: str


@dataclass(frozen=True)
class DigitalSignature:
    algorithm: str
    signature: str


@dataclass
class SecurityRule:
    protocol: Protocol
    port: int
    source: str
    action: AccessDecision


@dataclass
class SecurityGroup:
    group_id: str
    rules: list[SecurityRule] = field(
        default_factory=list
    )


@dataclass
class FirewallRule:
    protocol: Protocol
    port: int
    source: str
    destination: str
    action: AccessDecision


@dataclass
class User:
    user_id: str
    username: str
    tenant_id: str
    status: UserStatus = UserStatus.ACTIVE


@dataclass
class Role:
    name: str
    permissions: set[str] = field(
        default_factory=set
    )


@dataclass
class Certificate:
    subject: str
    issuer: str
    serial_number: str
    public_key: str
    valid_from: datetime
    valid_until: datetime


@dataclass
class AuthenticationEvent:
    timestamp: datetime
    user_id: str
    source_ip: str
    success: bool
    method: str


@dataclass
class NetworkEvent:
    timestamp: datetime
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: Protocol
    blocked: bool


@dataclass
class SecurityEvent:
    timestamp: datetime
    event_type: SecurityEventType
    actor: str
    source_ip: str
    action: str
    success: bool
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)