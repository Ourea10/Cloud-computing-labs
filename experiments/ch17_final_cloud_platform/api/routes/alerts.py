from fastapi import APIRouter

from ...schemas import AlertCreate

from ...services.alert_service import (
    AlertService,
)

from ..dependencies import (
    alert_repository,
)


router = APIRouter()

service = AlertService(
    alert_repository
)


@router.post(
    "/{resource_id}"
)
def create_alert(
    resource_id: str,
    request: AlertCreate,
):

    return service.create(
        resource_id=resource_id,
        metric=request.metric,
        threshold=request.threshold,
    )