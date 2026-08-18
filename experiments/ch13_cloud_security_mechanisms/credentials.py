from datetime import datetime, timezone
from uuid import uuid4

from .exceptions import CredentialNotFoundError

from .models import Credential


class CredentialManager:

    def __init__(
        self,
        encryption_service,
    ):

        self.encryption = (
            encryption_service
        )

        self.credentials: dict[
            str,
            Credential,
        ] = {}

    def store(
        self,
        user_id: str,
        credential_type: str,
        value: str,
    ) -> Credential:

        credential = Credential(
            credential_id=str(uuid4()),
            user_id=user_id,
            credential_type=credential_type,
            encrypted_value=(
                self.encryption.encrypt(
                    value
                )
            ),
            created_at=datetime.now(
                timezone.utc
            ),
        )

        self.credentials[
            credential.credential_id
        ] = credential

        return credential

    def retrieve(
        self,
        credential_id: str,
    ) -> str:

        credential = self.credentials.get(
            credential_id
        )

        if credential is None:

            raise CredentialNotFoundError(
                f"Credential "
                f"{credential_id} not found"
            )

        return self.encryption.decrypt(
            credential.encrypted_value
        )

    def delete(
        self,
        credential_id: str,
    ) -> None:

        if credential_id not in (
            self.credentials
        ):

            raise CredentialNotFoundError(
                f"Credential "
                f"{credential_id} not found"
            )

        del self.credentials[
            credential_id
        ]