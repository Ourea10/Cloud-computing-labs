from .enums import DeliveryModel

from .models import (
    DeliveryRecommendation,
    Workload,
)


class DeliveryModelSelector:

    def select(
        self,
        workload: Workload,
    ):

        scores = {
            DeliveryModel.IAAS: 0,
            DeliveryModel.PAAS: 0,
            DeliveryModel.SAAS: 0,
        }

        reasons = {
            DeliveryModel.IAAS: [],
            DeliveryModel.PAAS: [],
            DeliveryModel.SAAS: [],
        }

        # OS control strongly favors IaaS.

        if workload.requires_os_control:

            scores[
                DeliveryModel.IAAS
            ] += 5

            reasons[
                DeliveryModel.IAAS
            ].append(
                "Workload requires OS control"
            )

        else:

            scores[
                DeliveryModel.PAAS
            ] += 2

            scores[
                DeliveryModel.SAAS
            ] += 2

        # Runtime control favors IaaS.

        if workload.requires_runtime_control:

            scores[
                DeliveryModel.IAAS
            ] += 4

            reasons[
                DeliveryModel.IAAS
            ].append(
                "Workload requires runtime control"
            )

        else:

            scores[
                DeliveryModel.PAAS
            ] += 3

        # Application control.

        if workload.requires_application_control:

            scores[
                DeliveryModel.PAAS
            ] += 4

            reasons[
                DeliveryModel.PAAS
            ].append(
                "Customer needs application control"
            )

        else:

            scores[
                DeliveryModel.SAAS
            ] += 5

            reasons[
                DeliveryModel.SAAS
            ].append(
                "Customer can consume a finished service"
            )

        # High operational complexity makes SaaS
        # more attractive.

        if workload.operational_complexity >= 8:

            scores[
                DeliveryModel.SAAS
            ] += 3

            reasons[
                DeliveryModel.SAAS
            ].append(
                "High operational complexity"
            )

        # High scalability favors managed platforms.

        if workload.scalability_requirement >= 8:

            scores[
                DeliveryModel.PAAS
            ] += 2

            reasons[
                DeliveryModel.PAAS
            ].append(
                "High scalability requirement"
            )

        selected = max(
            scores,
            key=scores.get,
        )

        return DeliveryRecommendation(
            workload_id=workload.workload_id,
            model=selected,
            score=scores[selected],
            reasons=reasons[selected],
        )