from dataclasses import dataclass


@dataclass(frozen=True)
class IntrusionAlert:
    source_ip: str
    reason: str
    severity: str


class IntrusionDetectionSystem:

    def __init__(
        self,
        failed_attempt_threshold: int = 5,
    ):

        self.threshold = (
            failed_attempt_threshold
        )

    def analyze_authentication_attempts(
        self,
        source_ip: str,
        failed_attempts: int,
    ) -> IntrusionAlert | None:

        if (
            failed_attempts
            >= self.threshold
        ):

            return IntrusionAlert(
                source_ip=source_ip,
                reason=(
                    "Excessive failed "
                    "authentication attempts"
                ),
                severity="high",
            )

        return None