from .enums import DeliveryModel
from .models import RiskAssessment


class RiskModel:

    def assess(
        self,
        model: DeliveryModel,
    ) -> RiskAssessment:

        if model == DeliveryModel.IAAS:

            operational = 8
            lock_in = 4
            management = 8

        elif model == DeliveryModel.PAAS:

            operational = 4
            lock_in = 6
            management = 5

        else:

            operational = 2
            lock_in = 9
            management = 3

        return RiskAssessment(
            delivery_model=model,
            operational_risk=operational,
            vendor_lock_in_risk=lock_in,
            management_risk=management,
            total_risk=(
                operational
                + lock_in
                + management
            ),
        )