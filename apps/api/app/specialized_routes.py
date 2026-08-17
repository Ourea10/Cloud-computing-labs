from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.security import (
    get_current_user,
)

from app.security_store import User

from app.specialized import (
    audit_monitor,
    load_balancer,
    pay_per_use,
    state_database,
)


router = APIRouter(
    prefix="/specialized",
    tags=["specialized mechanisms"],
)


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