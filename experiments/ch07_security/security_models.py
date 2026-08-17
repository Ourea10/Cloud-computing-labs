from dataclasses import dataclass
from enum import Enum


class SecurityProperty(str, Enum):
    CONFIDENTIALITY = "confidentiality"
    INTEGRITY = "integrity"
    AVAILABILITY = "availability"
    AUTHENTICITY = "authenticity"


class ControlType(str, Enum):
    PREVENTIVE = "preventive"
    DETECTIVE = "detective"
    CORRECTIVE = "corrective"


@dataclass(frozen=True)
class SecurityControl:
    name: str
    control_type: ControlType
    protects: set[SecurityProperty]
    description: str


@dataclass(frozen=True)
class SecurityPolicy:
    name: str
    statement: str
    enforcement: str