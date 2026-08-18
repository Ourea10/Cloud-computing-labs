from ..repositories.alert_repository import (
    AlertRepository,
)

from ..services.alert_service import (
    AlertService,
)


def test_alert():

    repository = AlertRepository()

    service = AlertService(
        repository
    )

    alert = service.create(
        resource_id="resource-1",
        metric="cpu",
        threshold=80,
    )

    service.evaluate(
        alert,
        90,
    )

    assert alert.triggered is True