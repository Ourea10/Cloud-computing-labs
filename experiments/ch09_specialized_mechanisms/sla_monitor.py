from collections.abc import Callable

from experiments.ch09_specialized_mechanisms.models import (
    SLAObservation,
    SLAObjective,
)

from experiments.ch09_specialized_mechanisms.sla_agents import (
    SLAMonitorPollingAgent,
    SLAMonitoringAgent,
)


class SLAMonitor:

    def __init__(self):

        self.polling_agent = (
            SLAMonitorPollingAgent()
        )

        self.monitoring_agent = (
            SLAMonitoringAgent()
        )

        self.objectives: dict[
            str,
            SLAObjective,
        ] = {}

        self.observations: list[
            SLAObservation
        ] = []

    def register_objective(
        self,
        objective: SLAObjective,
    ) -> None:

        self.objectives[
            objective.name
        ] = objective

    def check(
        self,
        objective_name: str,
        metric_provider: Callable[[], float],
    ) -> SLAObservation:

        objective = self.objectives[
            objective_name
        ]

        value = self.polling_agent.poll(
            metric_provider
        )

        observation = (
            self.monitoring_agent.evaluate(
                objective,
                value,
            )
        )

        self.observations.append(
            observation
        )

        return observation

    def availability(
        self,
        objective_name: str,
    ) -> float:

        observations = [
            observation
            for observation in self.observations
            if (
                observation.metric
                == self.objectives[
                    objective_name
                ].metric
            )
        ]

        if not observations:
            return 0.0

        passed = sum(
            observation.passed
            for observation in observations
        )

        return passed / len(observations) * 100