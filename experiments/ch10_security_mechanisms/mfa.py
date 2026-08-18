import secrets


class MFAService:

    def __init__(self):

        self.codes: dict[
            str,
            str,
        ] = {}

    def generate_code(
        self,
        user_id: str,
    ) -> str:

        code = str(
            secrets.randbelow(1_000_000)
        ).zfill(6)

        self.codes[user_id] = code

        return code

    def verify(
        self,
        user_id: str,
        code: str,
    ) -> bool:

        expected = self.codes.get(
            user_id
        )

        if expected is None:
            return False

        if expected != code:
            return False

        del self.codes[user_id]

        return True