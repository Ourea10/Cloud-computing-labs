from ..repositories.user_repository import (
    UserRepository,
)

from ..services.auth_service import (
    AuthService,
)


def test_register_and_login():

    repository = UserRepository()

    service = AuthService(
        repository
    )

    user = service.register(
        "test@example.com",
        "password",
    )

    assert user.email == (
        "test@example.com"
    )

    authenticated = service.authenticate(
        "test@example.com",
        "password",
    )

    assert authenticated is not None