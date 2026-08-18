from fastapi import APIRouter, HTTPException

from ..cloud_manager import CloudManager
from ..models import (
    ResourceType,
    SLAPolicy,
)

from .schemas import (
    CreateVMRequest,
    ResourceResponse,
    SLARequest,
    UsageRequest,
)


router = APIRouter()

cloud_manager = CloudManager()


@router.post(
    "/resources/vm",
    response_model=ResourceResponse,
)
def create_vm(
    request: CreateVMRequest,
):

    try:

        resource = cloud_manager.create_vm(
            owner_id=request.owner_id,
            name=request.name,
            cpu=request.cpu,
            memory_gb=request.memory_gb,
            storage_gb=request.storage_gb,
        )

        return ResourceResponse(
            resource_id=resource.resource_id,
            owner_id=resource.owner_id,
            name=resource.name,
            status=resource.status.value,
            cpu=resource.cpu,
            memory_gb=resource.memory_gb,
            storage_gb=resource.storage_gb,
            region=resource.region,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/sla")
def create_sla(
    request: SLARequest,
):

    policy = cloud_manager.create_sla(
        SLAPolicy(
            sla_id=request.sla_id,
            customer_id=request.customer_id,
            resource_id=request.resource_id,
            availability_target=(
                request.availability_target
            ),
            response_time_target_ms=(
                request.response_time_target_ms
            ),
            monthly_price=(
                request.monthly_price
            ),
        )
    )

    return policy


@router.post("/usage")
def record_usage(
    request: UsageRequest,
):

    cloud_manager.record_usage(
        resource_id=request.resource_id,
        owner_id=request.owner_id,
        resource_type=ResourceType(
            request.resource_type
        ),
        quantity=request.quantity,
        unit=request.unit,
    )

    return {
        "status": "recorded"
    }


@router.get(
    "/billing/{customer_id}/{period}"
)
def generate_invoice(
    customer_id: str,
    period: str,
):

    invoice = (
        cloud_manager.generate_invoice(
            customer_id=customer_id,
            period=period,
        )
    )

    return invoice
