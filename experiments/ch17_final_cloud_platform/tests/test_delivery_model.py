from ..services.delivery_service import (
    DeliveryService,
)


def test_get_serverless_model():

    service = DeliveryService()

    model = service.get_model(
        "serverless"
    )

    assert model.name == "Serverless"

    assert (
        model.compute
        == "Provider"
    )

    assert (
        model.application
        == "Customer"
    )


def test_compare_iaas_and_serverless():

    service = DeliveryService()

    result = service.compare(
        "iaas",
        "serverless",
    )

    assert (
        result["first"].name
        == "IaaS"
    )

    assert (
        result["second"].name
        == "Serverless"
    )


def test_recommend_serverless():

    service = DeliveryService()

    model = service.recommend(
        {
            "minimal_operations": True
        }
    )

    assert (
        model.name
        == "Serverless"
    )


def test_recommend_iaas():

    service = DeliveryService()

    model = service.recommend(
        {
            "maximum_control": True
        }
    )

    assert (
        model.name
        == "IaaS"
    )