from .models import Role

from .security_manager import (
    SecurityManager,
)


def main():

    security = SecurityManager()

    # -------------------------------
    # 1. Configure roles
    # -------------------------------

    security.authorization.register_role(
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

    security.authorization.register_role(
        Role(
            name="customer",
            permissions={
                "resource:create",
                "resource:read",
                "billing:read",
            },
        )
    )

    security.authorization.register_role(
        Role(
            name="auditor",
            permissions={
                "resource:read",
                "billing:read",
                "audit:read",
            },
        )
    )

    # -------------------------------
    # 2. Register users
    # -------------------------------

    security.authentication.register_user(
        user_id="user-001",
        username="alice",
        password="AlicePassword123!",
        role="customer",
    )

    security.authentication.register_user(
        user_id="user-002",
        username="admin",
        password="AdminPassword123!",
        role="admin",
    )

    # -------------------------------
    # 3. Login
    # -------------------------------

    token = security.login(
        username="alice",
        password="AlicePassword123!",
    )

    print(
        "Access token:"
    )

    print(token.token)

    # -------------------------------
    # 4. Authentication
    # -------------------------------

    user = security.authenticate(
        token.token
    )

    print(
        "\nAuthenticated user:"
    )

    print(user)

    # -------------------------------
    # 5. Authorization
    # -------------------------------

    security.authorize(
        user,
        "resource:read",
    )

    print(
        "\nresource:read -> ALLOWED"
    )

    # -------------------------------
    # 6. Unauthorized operation
    # -------------------------------

    try:

        security.authorize(
            user,
            "security:manage",
        )

    except Exception as exc:

        print(
            "\nsecurity:manage -> DENIED"
        )

        print(exc)

    # -------------------------------
    # 7. Credential
    # -------------------------------

    credential = (
        security.credentials.store(
            user_id=user.user_id,
            credential_type="api_key",
            value="super-secret-api-key",
        )
    )

    print(
        "\nStored credential:"
    )

    print(
        credential.encrypted_value
    )

    print(
        "\nDecrypted credential:"
    )

    print(
        security.credentials.retrieve(
            credential.credential_id
        )
    )

    # -------------------------------
    # 8. Audit
    # -------------------------------

    print(
        "\nAudit events:"
    )

    for event in security.audit.events:

        print(
            event.action.value,
            event.success,
            event.message,
        )


if __name__ == "__main__":
    main()