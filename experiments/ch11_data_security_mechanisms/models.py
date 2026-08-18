from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class ScanResult(str, Enum):
    CLEAN = "clean"
    MALICIOUS = "malicious"
    SUSPICIOUS = "suspicious"


class DataClassification(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class DLPAction(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    ALERT = "alert"


class BackupStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class TrafficProtocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"
    HTTPS = "https"


@dataclass
class FileObject:
    file_id: str
    name: str
    content: bytes
    owner: str
    classification: DataClassification


@dataclass
class ScanReport:
    file_id: str
    result: ScanResult
    findings: list[str] = field(
        default_factory=list
    )


@dataclass
class CodeAnalysisReport:
    file_id: str
    suspicious_patterns: list[str]
    risk_score: int

    @property
    def malicious(self) -> bool:
        return self.risk_score >= 70


@dataclass
class DLPPolicy:
    name: str
    classification: DataClassification
    action: DLPAction
    destination_type: str


@dataclass
class DLPEvent:
    file_id: str
    user_id: str
    destination: str
    action: DLPAction
    reason: str


@dataclass
class TPMKey:
    key_id: str
    public_key: str


@dataclass
class BackupSnapshot:
    backup_id: str
    resource_id: str
    created_at: datetime
    data: bytes
    checksum: str


@dataclass
class RecoveryResult:
    backup_id: str
    resource_id: str
    restored: bool


@dataclass
class ActivityEvent:
    timestamp: datetime
    user_id: str
    resource_id: str
    action: str
    source_ip: str
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class TrafficEvent:
    timestamp: datetime
    source_ip: str
    destination_ip: str
    destination_port: int
    protocol: TrafficProtocol
    bytes_transferred: int


@dataclass
class DataLossEvent:
    timestamp: datetime
    resource_id: str
    user_id: str
    operation: str
    data_size: int
    reason: str