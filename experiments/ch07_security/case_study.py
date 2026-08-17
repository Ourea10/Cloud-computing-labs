import json
from pathlib import Path

from experiments.ch07_security.risk_assessment import (
    RiskAssessment,
    assess,
)


def load_case() -> dict:
    path = Path(__file__).parent / "case_study.json"

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_risk_register() -> list[RiskAssessment]:
    return [
        assess(
            threat="insufficient_authorization",
            vulnerability=(
                "Missing tenant ownership check"
            ),
            likelihood=4,
            impact=5,
        ),
        assess(
            threat="sql_injection",
            vulnerability=(
                "Unsafe query construction"
            ),
            likelihood=3,
            impact=5,
        ),
        assess(
            threat="brute_force",
            vulnerability=(
                "Unlimited authentication attempts"
            ),
            likelihood=4,
            impact=4,
        ),
        assess(
            threat="denial_of_service",
            vulnerability=(
                "Uncontrolled request rate"
            ),
            likelihood=4,
            impact=4,
        ),
        assess(
            threat="containerization_attack",
            vulnerability=(
                "Over-privileged container"
            ),
            likelihood=2,
            impact=5,
        ),
        assess(
            threat="remote_code_execution",
            vulnerability=(
                "Unsafe command execution"
            ),
            likelihood=2,
            impact=5,
        ),
    ]