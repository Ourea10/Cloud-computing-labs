from .cost_model import CostModel
from .delivery_model_selector import (
    DeliveryModelSelector,
)
from .enums import (
    DeliveryModel,
    Layer,
    Responsibility,
)
from .models import Workload
from .responsibility import (
    ResponsibilityManager,
)
from .risk_model import RiskModel


def test_iaas_responsibility():

    manager = ResponsibilityManager()

    assert (
        manager.get_responsibility(
            DeliveryModel.IAAS,
            Layer.OPERATING_SYSTEM,
        )
        == Responsibility.CUSTOMER
    )


def test_iaas_provider_responsibility():

    manager = ResponsibilityManager()

    assert (
        manager.get_responsibility(
            DeliveryModel.IAAS,
            Layer.COMPUTE,
        )
        == Responsibility.PROVIDER
    )


def test_paas_runtime_is_provider():

    manager = ResponsibilityManager()

    assert (
        manager.get_responsibility(
            DeliveryModel.PAAS,
            Layer.RUNTIME,
        )
        == Responsibility.PROVIDER
    )


def test_saas_application_is_provider():

    manager = ResponsibilityManager()

    assert (
        manager.get_responsibility(
            DeliveryModel.SAAS,
            Layer.APPLICATION,
        )
        == Responsibility.PROVIDER
    )


def test_legacy_workload_prefers_iaas():

    selector = DeliveryModelSelector()

    workload = Workload(
        workload_id="legacy",
        name="Legacy ERP",
        requires_os_control=True,
        requires_runtime_control=True,
        requires_application_control=True,
        operational_complexity=7,
        scalability_requirement=5,
        budget=1000,
    )

    result = selector.select(
        workload
    )

    assert (
        result.model
        == DeliveryModel.IAAS
    )


def test_application_workload_prefers_paas():

    selector = DeliveryModelSelector()

    workload = Workload(
        workload_id="api",
        name="API",
        requires_os_control=False,
        requires_runtime_control=False,
        requires_application_control=True,
        operational_complexity=6,
        scalability_requirement=9,
        budget=1000,
    )

    result = selector.select(
        workload
    )

    assert (
        result.model
        == DeliveryModel.PAAS
    )


def test_finished_service_prefers_saas():

    selector = DeliveryModelSelector()

    workload = Workload(
        workload_id="email",
        name="Email",
        requires_os_control=False,
        requires_runtime_control=False,
        requires_application_control=False,
        operational_complexity=9,
        scalability_requirement=8,
        budget=1000,
    )

    result = selector.select(
        workload
    )

    assert (
        result.model
        == DeliveryModel.SAAS
    )


def test_cost_model():

    model = CostModel()

    result = model.estimate(
        DeliveryModel.IAAS,
        10,
    )

    assert (
        result.total_cost
        == 150
    )


def test_risk_model():

    model = RiskModel()

    result = model.assess(
        DeliveryModel.IAAS
    )

    assert (
        result.total_risk
        == 20
    )