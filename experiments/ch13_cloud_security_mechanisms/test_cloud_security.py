import pytest

from .models import Role

from .security_manager import (
    SecurityManager,
)

from .exceptions import (
    AuthenticationError,
    AuthorizationError,
)


@pytest.fixture
def security():

    manager = SecurityManager()

    manager.authorization.register_role(
        Role(
            name="admin",
            permissions={
                "resource:create",
                "resource:read",
                "resource:delete",
                "security:manage",
                "audit:read",
            },
        )
    )

    manager.authorization.register_role(
        Role(
            name="customer",
            permissions={
                "resource:create",
                "resource:read",
            },
        )
    )

    manager.authentication.register_user(
        user_id="user-001",
        username="alice",
        password="Password123!",
        role="customer",
    )

    return manager


def test_password_hash_is_not_plaintext(
    security,
):

    user = (
        security.authentication.users[
            "user-001"
        ]
    )

    assert user.password_hash != (
        "Password123!"
    )

    assert ":" in user.password_hash


def test_login(
    security,
):

    token = security.login(
        username="alice",
        password="Password123!",
    )

    assert token.token

    user = security.authenticate(
        token.token
    )

    assert user.username == "alice"


def test_invalid_password(
    security,
):

    with pytest.raises(
        AuthenticationError
    ):

        security.login(
            username="alice",
            password="wrong",
        )


def test_authorization_allowed(
    security,
):

    token = security.login(
        username="alice",
        password="Password123!",
    )

    user = security.authenticate(
        token.token
    )

    security.authorize(
        user,
        "resource:read",
    )


def test_authorization_denied(
    security,
):

    token = security.login(
        username="alice",
        password="Password123!",
    )

    user = security.authenticate(
        token.token
    )

    with pytest.raises(
        AuthorizationError
    ):

        security.authorize(
            user,
            "security:manage",
        )


def test_credential_encryption(
    security,
):

    token = security.login(
        username="alice",
        password="Password123!",
    )

    user = security.authenticate(
        token.token
    )

    credential = (
        security.credentials.store(
            user_id=user.user_id,
            credential_type="api_key",
            value="my-secret-key",
        )
    )

    assert (
        credential.encrypted_value
        != "my-secret-key"
    )

    decrypted = (
        security.credentials.retrieve(
            credential.credential_id
        )
    )

    assert decrypted == (
        "my-secret-key"
    )


def test_audit_login(
    security,
):

    security.login(
        username="alice",
        password="Password123!",
    )

    events = (
        security.audit
        .get_events_for_user(
            "user-001"
        )
    )

    assert len(events) == 1

    assert events[0].success is True


def test_failed_login_is_audited(
    security,
):

    with pytest.raises(
        AuthenticationError
    ):

        security.login(
            username="alice",
            password="wrong",
        )

    events = (
        security.audit
        .get_failed_events()
    )

    assert len(events) == 1