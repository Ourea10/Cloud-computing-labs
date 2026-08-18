from .audit import AuditLogger
from .authentication import (
    AuthenticationService,
)
from .authorization import (
    AuthorizationService,
)
from .credentials import (
    CredentialManager,
)
from .encryption import (
    EncryptionService,
)
from .models import AuditAction


class SecurityManager:

    def __init__(self):

        self.authentication = (
            AuthenticationService()
        )

        self.authorization = (
            AuthorizationService()
        )

        self.encryption = (
            EncryptionService()
        )

        self.credentials = (
            CredentialManager(
                self.encryption
            )
        )

        self.audit = (
            AuditLogger()
        )

    def login(
        self,
        username: str,
        password: str,
    ):

        try:

            token = (
                self.authentication.login(
                    username,
                    password,
                )
            )

            self.audit.log(
                user_id=token.user_id,
                action=AuditAction.LOGIN,
                resource=None,
                success=True,
            )

            return token

        except Exception as exc:

            self.audit.log(
                user_id=None,
                action=AuditAction.LOGIN,
                resource=None,
                success=False,
                message=str(exc),
            )

            raise

    def authenticate(
        self,
        token: str,
    ):

        return (
            self.authentication.authenticate(
                token
            )
        )

    def authorize(
        self,
        user,
        permission: str,
    ):

        return (
            self.authorization
            .require_permission(
                user,
                permission,
            )
        )