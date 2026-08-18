from .cost_model import CostModel
from .delivery_model_selector import (
    DeliveryModelSelector,
)
from .responsibility import (
    ResponsibilityManager,
)
from .risk_model import RiskModel
from .workload import WorkloadManager


class DeliveryService:

    def __init__(self):

        self.responsibility = (
            ResponsibilityManager()
        )

        self.workloads = (
            WorkloadManager()
        )

        self.selector = (
            DeliveryModelSelector()
        )

        self.cost = CostModel()

        self.risk = RiskModel()

    def recommend(
        self,
        workload_id: str,
    ):

        workload = (
            self.workloads.get(
                workload_id
            )
        )

        return self.selector.select(
            workload
        )

    def evaluate(
        self,
        workload_id: str,
        workload_size: int,
    ):

        recommendation = (
            self.recommend(
                workload_id
            )
        )

        cost = self.cost.estimate(
            recommendation.model,
            workload_size,
        )

        risk = self.risk.assess(
            recommendation.model
        )

        return {
            "workload_id": workload_id,
            "delivery_model": (
                recommendation.model.value
            ),
            "score": recommendation.score,
            "reasons": recommendation.reasons,
            "cost": {
                "total": cost.total_cost,
                "infrastructure": (
                    cost.infrastructure_cost
                ),
                "operations": (
                    cost.operations_cost
                ),
                "platform": (
                    cost.platform_cost
                ),
            },
            "risk": {
                "operational": (
                    risk.operational_risk
                ),
                "vendor_lock_in": (
                    risk.vendor_lock_in_risk
                ),
                "management": (
                    risk.management_risk
                ),
                "total": risk.total_risk,
            },
        }