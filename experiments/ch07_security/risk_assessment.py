from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True)
class RiskAssessment:
    threat: str
    vulnerability: str
    likelihood: int
    impact: int

    @property
    def score(self) -> int:
        return self.likelihood * self.impact

    @property
    def level(self) -> RiskLevel:
        score = self.score

        if score >= 20:
            return RiskLevel.CRITICAL

        if score >= 12:
            return RiskLevel.HIGH

        if score >= 6:
            return RiskLevel.MEDIUM

        return RiskLevel.LOW


def assess(
    threat: str,
    vulnerability: str,
    likelihood: int,
    impact: int,
) -> RiskAssessment:

    if not 1 <= likelihood <= 5:
        raise ValueError(
            "Likelihood must be between 1 and 5."
        )

    if not 1 <= impact <= 5:
        raise ValueError(
            "Impact must be between 1 and 5."
        )

    return RiskAssessment(
        threat=threat,
        vulnerability=vulnerability,
        likelihood=likelihood,
        impact=impact,
    )