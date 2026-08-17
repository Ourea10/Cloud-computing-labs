from fastapi import APIRouter, Depends, HTTPException, status

from app.security import create_lab_token, get_current_user
from app.security_store import RESOURCES, User


router = APIRouter(prefix="/security", tags=["security"])


@router.post("/token")
def issue_token(username: str) -> dict[str, str]:
    try:
        token = create_lab_token(username)
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown user",
        ) from error

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me")
def current_user(user: User = Depends(get_current_user)) -> User:
    return user


@router.get("/resources")
def tenant_resources(user: User = Depends(get_current_user)) -> list[dict[str, str]]:
    if user.role == "admin":
        resources = RESOURCES.values()
    else:
        resources = (
            resource
            for resource in RESOURCES.values()
            if resource.tenant_id == user.tenant_id
        )

    return [
        {
            "resource_id": resource.resource_id,
            "tenant_id": resource.tenant_id,
            "name": resource.name,
        }
        for resource in resources
    ]


@router.get("/resources/{resource_id}")
def get_resource(
    resource_id: str,
    user: User = Depends(get_current_user),
) -> dict[str, str]:
    resource = RESOURCES.get(resource_id)

    if resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found",
        )

    if user.role != "admin" and resource.tenant_id != user.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this resource is forbidden",
        )

    return {
        "resource_id": resource.resource_id,
        "tenant_id": resource.tenant_id,
        "name": resource.name,
    }
