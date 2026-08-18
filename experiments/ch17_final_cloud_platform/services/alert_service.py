import uuid

from ..models import Alert
from ..repositories.alert_repository import (
    AlertRepository,
)


class AlertService:

    def __init__(
        self,
        repository: AlertRepository,
    ):

        self.repository = repository

    def create(
        self,
        resource_id,
        metric,
        threshold,
    ):

        alert = Alert(
            id=str(uuid.uuid4()),
            resource_id=resource_id,
            metric=metric,
            threshold=threshold,
            triggered=False,
        )

        return self.repository.create(
            alert
        )

    def evaluate(
        self,
        alert,
        value,
    ):

        alert.triggered = (
            value >= alert.threshold
        )

        return alert