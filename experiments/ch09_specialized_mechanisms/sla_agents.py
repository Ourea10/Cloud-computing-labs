from collections.abc import Callable

from experiments.ch09_specialized_mechanisms.models import (
    SLAObservation,
    SLAObjective,
    utc_now,
)


class SLAMonitorPollingAgent:

    def poll(
        self,
        metric_provider: Callable[[], float],
    ) -> float:

        return metric_provider()


class SLAMonitoringAgent:

    def evaluate(
        self,
        objective: SLAObjective,
        value: float,
    ) -> SLAObservation:

        passed = value >= objective.target

        return SLAObservation(
            timestamp=utc_now(),
            metric=objective.metric,
            value=value,
            target=objective.target,
            passed=passed,
        )