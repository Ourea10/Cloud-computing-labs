from cryptography.fernet import (
    Fernet,
)

from .exceptions import EncryptionError


class EncryptionService:

    def __init__(
        self,
        key: bytes | None = None,
    ):

        self.key = (
            key
            or Fernet.generate_key()
        )

        self.cipher = Fernet(
            self.key
        )

    def encrypt(
        self,
        value: str,
    ) -> str:

        try:

            encrypted = (
                self.cipher.encrypt(
                    value.encode()
                )
            )

            return encrypted.decode()

        except Exception as exc:

            raise EncryptionError(
                "Encryption failed"
            ) from exc

    def decrypt(
        self,
        value: str,
    ) -> str:

        try:

            decrypted = (
                self.cipher.decrypt(
                    value.encode()
                )
            )

            return decrypted.decode()

        except Exception as exc:

            raise EncryptionError(
                "Decryption failed"
            ) from exc