from enum import Enum


class DeliveryModel(str, Enum):
    IAAS = "IaaS"
    PAAS = "PaaS"
    SAAS = "SaaS"


def describe(model: DeliveryModel) -> str:
    descriptions = {
        DeliveryModel.IAAS: (
            "Consumer manages workloads and much of the software stack."
        ),
        DeliveryModel.PAAS: (
            "Consumer deploys applications onto a managed platform."
        ),
        DeliveryModel.SAAS: (
            "Consumer uses a complete software service."
        ),
    }

    return descriptions[model]