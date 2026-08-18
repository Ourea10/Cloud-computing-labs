from datetime import datetime, timezone
from uuid import uuid4

from .exceptions import (
    UnsupportedOperatorError,
)

from .models import (
    Alert,
    AlertRule,
    AlertStatus,
)


class AlertEngine:

    def __init__(self):

        self.rules: dict[
            str,
            AlertRule,
        ] = {}

        self.alerts: list[Alert] = []

    def register_rule(
        self,
        rule: AlertRule,
    ) -> None:

        self.rules[
            rule.rule_id
        ] = rule

    def evaluate(
        self,
        metric,
    ) -> list[Alert]:

        triggered = []

        for rule in self.rules.values():

            if (
                rule.resource_id
                and rule.resource_id
                != metric.resource_id
            ):
                continue

            if (
                rule.metric_type
                != metric.metric_type
            ):
                continue

            matched = self._compare(
                metric.value,
                rule.operator,
                rule.threshold,
            )

            if not matched:
                continue

            alert = Alert(
                alert_id=str(uuid4()),
                rule_id=rule.rule_id,
                resource_id=metric.resource_id,
                metric_type=metric.metric_type,
                value=metric.value,
                threshold=rule.threshold,
                severity=rule.severity,
                status=AlertStatus.ACTIVE,
                message=rule.message,
                created_at=datetime.now(
                    timezone.utc
                ),
            )

            self.alerts.append(
                alert
            )

            triggered.append(
                alert
            )

        return triggered

    def _compare(
        self,
        value: float,
        operator: str,
        threshold: float,
    ) -> bool:

        if operator == ">":
            return value > threshold

        if operator == ">=":
            return value >= threshold

        if operator == "<":
            return value < threshold

        if operator == "<=":
            return value <= threshold

        if operator == "==":
            return value == threshold

        raise UnsupportedOperatorError(
            f"Unsupported operator: "
            f"{operator}"
        )