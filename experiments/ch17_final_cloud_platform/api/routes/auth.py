from fastapi import APIRouter

from ...services.auth_service import (
    AuthService,
)

from ...schemas import (
    LoginRequest,
    UserCreate,
)

from ..dependencies import (
    user_repository,
)


router = APIRouter()

service = AuthService(
    user_repository
)


@router.post("/register")
def register(
    request: UserCreate,
):

    user = service.register(
        request.email,
        request.password,
    )

    return {
        "id": user.id,
        "email": user.email,
    }


@router.post("/login")
def login(
    request: LoginRequest,
):

    user = service.authenticate(
        request.email,
        request.password,
    )

    if not user:

        return {
            "authenticated": False
        }

    return {
        "authenticated": True,
        "user_id": user.id,
    }