from fastapi import Header, HTTPException

from ..security_manager import (
    SecurityManager,
)
from ..models import Role


security_manager = SecurityManager()


security_manager.authorization.register_role(
    Role(
        name="admin",
        permissions={
            "resource:create",
            "resource:read",
            "resource:delete",
            "billing:read",
            "security:manage",
            "audit:read",
        },
    )
)
security_manager.authorization.register_role(
    Role(
        name="customer",
        permissions={
            "resource:create",
            "resource:read",
            "billing:read",
        },
    )
)
security_manager.authorization.register_role(
    Role(
        name="auditor",
        permissions={
            "resource:read",
            "billing:read",
            "audit:read",
        },
    )
)

security_manager.authentication.register_user(
    "user-001",
    "alice",
    "AlicePassword123!",
    "customer",
)
security_manager.authentication.register_user(
    "user-002",
    "admin",
    "AdminPassword123!",
    "admin",
)
security_manager.authentication.register_user(
    "user-003",
    "auditor",
    "AuditorPassword123!",
    "auditor",
)


def get_current_user(
    authorization: str | None = Header(
        default=None
    ),
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    token = authorization.removeprefix(
        "Bearer "
    )

    try:

        return security_manager.authenticate(
            token
        )

    except Exception as exc:

        raise HTTPException(
            status_code=401,
            detail=str(exc),
        )


def require_permission(
    permission: str,
):

    def dependency(
        authorization: str | None = Header(
            default=None
        ),
    ):

        user = get_current_user(
            authorization
        )

        try:

            security_manager.authorize(
                user,
                permission,
            )

        except Exception as exc:

            raise HTTPException(
                status_code=403,
                detail=str(exc),
            )

        return user

    return dependency
