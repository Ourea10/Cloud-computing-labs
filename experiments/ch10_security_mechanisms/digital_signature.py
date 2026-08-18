from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import (
    PKCS1v15,
)
from cryptography.exceptions import InvalidSignature

from experiments.ch10_security_mechanisms.models import (
    DigitalSignature,
)


class DigitalSignatureService:

    def __init__(self):

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        self.public_key = (
            self.private_key.public_key()
        )

    def sign(
        self,
        message: str,
    ) -> DigitalSignature:

        signature = self.private_key.sign(
            message.encode(),
            PKCS1v15(),
            hashes.SHA256(),
        )

        return DigitalSignature(
            algorithm="RSA-SHA256",
            signature=signature.hex(),
        )

    def verify(
        self,
        message: str,
        signature: DigitalSignature,
    ) -> bool:

        try:

            self.public_key.verify(
                bytes.fromhex(
                    signature.signature
                ),
                message.encode(),
                PKCS1v15(),
                hashes.SHA256(),
            )

            return True

        except InvalidSignature:

            return False