from fastapi import APIRouter, Depends

from ..models import (
    AuditAction,
)

from .dependencies import (
    get_current_user,
    require_permission,
    security_manager,
)

from .schemas import (
    CredentialRequest,
    CredentialResponse,
    LoginRequest,
    LoginResponse,
)


router = APIRouter()


@router.post(
    "/auth/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
):

    token = security_manager.login(
        username=request.username,
        password=request.password,
    )

    return LoginResponse(
        access_token=token.token
    )


@router.post(
    "/credentials",
    response_model=CredentialResponse,
)
def create_credential(
    request: CredentialRequest,
    user=Depends(
        require_permission(
            "security:manage"
        )
    ),
):

    credential = (
        security_manager.credentials.store(
            user_id=user.user_id,
            credential_type=(
                request.credential_type
            ),
            value=request.value,
        )
    )

    security_manager.audit.log(
        user_id=user.user_id,
        action=AuditAction.SECURITY_CHANGE,
        resource=credential.credential_id,
        success=True,
    )

    return CredentialResponse(
        credential_id=credential.credential_id,
        credential_type=(
            credential.credential_type
        ),
    )


@router.get("/me")
def get_me(
    user=Depends(
        get_current_user
    ),
):

    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
    }


@router.get("/audit")
def get_audit_events(
    user=Depends(
        require_permission(
            "audit:read"
        )
    ),
):

    return (
        security_manager.audit.events
    )