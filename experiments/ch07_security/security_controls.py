from experiments.ch07_security.security_models import (
    ControlType,
    SecurityControl,
    SecurityProperty,
)


CONTROLS = [
    SecurityControl(
        name="Authentication",
        control_type=ControlType.PREVENTIVE,
        protects={
            SecurityProperty.AUTHENTICITY,
        },
        description=(
            "Verify the identity of a caller before "
            "allowing access to protected resources."
        ),
    ),
    SecurityControl(
        name="Authorization",
        control_type=ControlType.PREVENTIVE,
        protects={
            SecurityProperty.CONFIDENTIALITY,
            SecurityProperty.INTEGRITY,
        },
        description=(
            "Verify whether an authenticated identity "
            "has permission to perform an operation."
        ),
    ),
    SecurityControl(
        name="Rate Limiting",
        control_type=ControlType.PREVENTIVE,
        protects={
            SecurityProperty.AVAILABILITY,
        },
        description=(
            "Limit repeated requests to reduce brute-force "
            "and resource exhaustion attacks."
        ),
    ),
    SecurityControl(
        name="Audit Logging",
        control_type=ControlType.DETECTIVE,
        protects={
            SecurityProperty.INTEGRITY,
            SecurityProperty.AUTHENTICITY,
        },
        description=(
            "Record security-relevant events for investigation."
        ),
    ),
    SecurityControl(
        name="Input Validation",
        control_type=ControlType.PREVENTIVE,
        protects={
            SecurityProperty.INTEGRITY,
        },
        description=(
            "Validate external input before processing."
        ),
    ),
]