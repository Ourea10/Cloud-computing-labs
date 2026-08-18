from fastapi import Header, HTTPException


def require_permission(
    permission: str,
):

    def dependency(
        authorization: str | None = Header(
            default=None
        ),
    ):

        if not authorization:

            raise HTTPException(
                status_code=401,
                detail="Authentication required",
            )

        # In the real integrated repository,
        # this dependency delegates to the
        # Chapter 13 security manager.

        return {
            "permission": permission
        }

    return dependency