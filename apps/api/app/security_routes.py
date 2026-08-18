from fastapi import APIRouter, Depends, HTTPException, status

from app.security import (
    create_lab_token,
    get_current_user,
)

from app.security_store import (
    RESOURCES,
    User,
)


router = APIRouter(
    prefix="/security",
    tags=["security"],
)


@router.post("/token")
def create_token(
    username: str,
):
    try:
        token = create_lab_token(
            username
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "tenant_id": current_user.tenant_id,
        "role": current_user.role,
    }


@router.get("/resources/{resource_id}")
def get_resource(
    resource_id: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    resource = RESOURCES.get(
        resource_id
    )

    if resource is None:
        raise HTTPException(
            status_code=404,
            detail="Resource not found",
        )

    if (
        current_user.role != "admin"
        and current_user.tenant_id
        != resource.tenant_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Cross-tenant access denied",
        )

    return resource