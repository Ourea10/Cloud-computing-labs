from .enums import DeliveryModel
from .models import CostEstimate


class CostModel:

    def estimate(
        self,
        model: DeliveryModel,
        workload_size: int,
    ) -> CostEstimate:

        if model == DeliveryModel.IAAS:

            infrastructure = (
                workload_size * 10
            )

            operations = (
                workload_size * 5
            )

            platform = 0

        elif model == DeliveryModel.PAAS:

            infrastructure = 0

            operations = (
                workload_size * 2
            )

            platform = (
                workload_size * 12
            )

        else:

            infrastructure = 0

            operations = 0

            platform = (
                workload_size * 20
            )

        total = (
            infrastructure
            + operations
            + platform
        )

        return CostEstimate(
            delivery_model=model,
            infrastructure_cost=infrastructure,
            operations_cost=operations,
            platform_cost=platform,
            total_cost=total,
        )