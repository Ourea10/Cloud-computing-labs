import hashlib

from experiments.ch10_security_mechanisms.models import (
    HashResult,
)


class HashingService:

    def hash(
        self,
        value: str,
        algorithm: str = "sha256",
    ) -> HashResult:

        hasher = hashlib.new(
            algorithm
        )

        hasher.update(
            value.encode()
        )

        return HashResult(
            algorithm=algorithm,
            digest=hasher.hexdigest(),
        )

    def verify(
        self,
        value: str,
        expected_digest: str,
        algorithm: str = "sha256",
    ) -> bool:

        result = self.hash(
            value=value,
            algorithm=algorithm,
        )

        return result.digest == expected_digest