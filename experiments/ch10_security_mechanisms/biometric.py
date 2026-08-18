import hashlib


class BiometricService:

    def __init__(self):

        self.templates: dict[
            str,
            str,
        ] = {}

    def enroll(
        self,
        user_id: str,
        biometric_value: str,
    ) -> None:

        self.templates[user_id] = (
            hashlib.sha256(
                biometric_value.encode()
            ).hexdigest()
        )

    def verify(
        self,
        user_id: str,
        biometric_value: str,
    ) -> bool:

        expected = self.templates.get(
            user_id
        )

        if expected is None:
            return False

        actual = hashlib.sha256(
            biometric_value.encode()
        ).hexdigest()

        return actual == expected