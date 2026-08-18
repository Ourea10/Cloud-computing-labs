import hashlib
import secrets

from experiments.ch11_data_security_mechanisms.models import (
    TPMKey,
)


class TrustedPlatformModule:

    def __init__(self):

        self.keys: dict[
            str,
            str,
        ] = {}

    def generate_key(
        self,
        key_id: str,
    ) -> TPMKey:

        private_material = secrets.token_hex(32)

        public_material = hashlib.sha256(
            private_material.encode()
        ).hexdigest()

        self.keys[key_id] = private_material

        return TPMKey(
            key_id=key_id,
            public_key=public_material,
        )

    def sign(
        self,
        key_id: str,
        message: bytes,
    ) -> str:

        private_material = self.keys[
            key_id
        ]

        return hashlib.sha256(
            (
                private_material
                + message.hex()
            ).encode()
        ).hexdigest()