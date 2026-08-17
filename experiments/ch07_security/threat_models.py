from dataclasses import dataclass
from enum import Enum


class ThreatAgent(str, Enum):
    ANONYMOUS_ATTACKER = "anonymous_attacker"
    MALICIOUS_SERVICE_AGENT = "malicious_service_agent"
    TRUSTED_ATTACKER = "trusted_attacker"
    MALICIOUS_INSIDER = "malicious_insider"


class ThreatCategory(str, Enum):
    NETWORK = "network"
    AUTHORIZATION = "authorization"
    AVAILABILITY = "availability"
    VIRTUALIZATION = "virtualization"
    CONTAINERIZATION = "containerization"
    APPLICATION = "application"
    HUMAN = "human"
    PERSISTENCE = "persistence"


@dataclass(frozen=True)
class Threat:
    name: str
    category: ThreatCategory
    description: str


@dataclass(frozen=True)
class Vulnerability:
    name: str
    description: str
    affected_asset: str


@dataclass(frozen=True)
class Exploit:
    name: str
    vulnerability: str
    impact: str


@dataclass(frozen=True)
class AttackVector:
    name: str
    entry_point: str
    description: str


@dataclass(frozen=True)
class SecurityIncident:
    threat: Threat
    agent: ThreatAgent
    attack_vector: AttackVector
    asset: str