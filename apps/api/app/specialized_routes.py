from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from pydantic import BaseModel, Field

from app.security import (
    get_current_user,
)

from app.security_store import User

from app.specialized import (
    audit_monitor,
    load_balancer,
    state_database,
)

from experiments.ch09_specialized_mechanisms.models import (
    BackendTarget,
    HealthStatus,
)


class AuditEventRequest(BaseModel):
    action: str
    resource_type: str
    resource_id: str | None = None
    success: bool = True
    metadata: dict = Field(default_factory=dict)


class LoadBalancerTargetRequest(BaseModel):
    resource_id: str
    address: str
    port: int
    health: HealthStatus = HealthStatus.UNKNOWN


router = APIRouter(
    prefix="/specialized",
    tags=["specialized mechanisms"],
)


@router.post("/audit", status_code=201)
def record_audit_event(
    payload: AuditEventRequest,
    current_user: User = Depends(get_current_user),
):
    event = audit_monitor.record(
        actor=current_user.username,
        tenant_id=current_user.tenant_id,
        action=payload.action,
        resource_type=payload.resource_type,
        resource_id=payload.resource_id,
        success=payload.success,
        metadata=payload.metadata,
    )

    return event


@router.post("/load-balancer/targets", status_code=201)
def register_load_balancer_target(
    payload: LoadBalancerTargetRequest,
    current_user: User = Depends(get_current_user),
):
    target = BackendTarget(
        resource_id=payload.resource_id,
        address=payload.address,
        port=payload.port,
        health=payload.health,
    )
    load_balancer.register(target)

    return {
        "resource_id": target.resource_id,
        "address": target.address,
        "port": target.port,
        "health": target.health,
        "tenant_id": current_user.tenant_id,
    }


@router.get("/state/{resource_id}")
def get_resource_state(
    resource_id: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    resource = state_database.get_resource(
        resource_id
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    if (
        resource["tenant_id"]
        != current_user.tenant_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Resource belongs to another tenant",
        )

    return resource


@router.get("/audit")
def get_audit_events(
    current_user: User = Depends(
        get_current_user
    ),
):

    events = [
        event
        for event in audit_monitor.events
        if event.tenant_id
        == current_user.tenant_id
    ]

    return events


@router.get("/load-balancer/targets")
def get_load_balancer_targets(
    current_user: User = Depends(
        get_current_user
    ),
):

    return [
        {
            "resource_id": target.resource_id,
            "address": target.address,
            "port": target.port,
            "health": target.health,
            "connections": (
                target.active_connections
            ),
        }
        for target
        in load_balancer.targets.values()
    ]
