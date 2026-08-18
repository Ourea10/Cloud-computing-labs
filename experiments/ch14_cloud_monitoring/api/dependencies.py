from fastapi import Header, HTTPException

from experiments.ch13_cloud_security_mechanisms.api.dependencies import (
    security_manager,
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