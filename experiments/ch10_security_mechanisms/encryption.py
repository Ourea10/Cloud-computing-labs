import base64

from cryptography.fernet import Fernet

from experiments.ch10_security_mechanisms.models import (
    EncryptedData,
)


class SymmetricEncryption:

    def __init__(self, key: bytes | None = None):

        self.key = key or Fernet.generate_key()

        self.cipher = Fernet(self.key)

    def encrypt(
        self,
        plaintext: str,
    ) -> EncryptedData:

        ciphertext = self.cipher.encrypt(
            plaintext.encode()
        )

        return EncryptedData(
            algorithm="Fernet",
            ciphertext=base64.b64encode(
                ciphertext
            ).decode(),
        )

    def decrypt(
        self,
        encrypted: EncryptedData,
    ) -> str:

        ciphertext = base64.b64decode(
            encrypted.ciphertext
        )

        plaintext = self.cipher.decrypt(
            ciphertext
        )

        return plaintext.decode()