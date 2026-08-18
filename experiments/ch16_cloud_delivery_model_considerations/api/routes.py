from fastapi import APIRouter, Depends

from .dependencies import (
    require_permission,
)

from .schemas import (
    EvaluationRequest,
    WorkloadRequest,
)

from ..delivery_service import (
    DeliveryService,
)

from ..models import Workload


router = APIRouter()

service = DeliveryService()


@router.post(
    "/workloads"
)
def register_workload(
    request: WorkloadRequest,
    user=Depends(
        require_permission(
            "workload:manage"
        )
    ),
):

    workload = Workload(
        workload_id=request.workload_id,
        name=request.name,
        requires_os_control=(
            request.requires_os_control
        ),
        requires_runtime_control=(
            request.requires_runtime_control
        ),
        requires_application_control=(
            request.requires_application_control
        ),
        operational_complexity=(
            request.operational_complexity
        ),
        scalability_requirement=(
            request.scalability_requirement
        ),
        budget=request.budget,
    )

    service.workloads.register(
        workload
    )

    return {
        "workload_id":
            workload.workload_id,
        "name":
            workload.name,
    }


@router.post(
    "/evaluate"
)
def evaluate(
    request: EvaluationRequest,
    user=Depends(
        require_permission(
            "workload:read"
        )
    ),
):

    return service.evaluate(
        request.workload_id,
        request.workload_size,
    )


@router.get(
    "/models/{model}"
)
def responsibility_matrix(
    model: str,
    user=Depends(
        require_permission(
            "workload:read"
        )
    ),
):

    from ..enums import DeliveryModel

    delivery_model = (
        DeliveryModel(model)
    )

    return service.responsibility.matrix(
        delivery_model
    )