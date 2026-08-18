import secrets


class SSOService:

    def __init__(self):

        self.sessions: dict[
            str,
            str,
        ] = {}

    def create_session(
        self,
        user_id: str,
    ) -> str:

        token = secrets.token_urlsafe(32)

        self.sessions[token] = user_id

        return token

    def authenticate(
        self,
        token: str,
    ) -> str | None:

        return self.sessions.get(token)

    def revoke(
        self,
        token: str,
    ) -> None:

        self.sessions.pop(
            token,
            None,
        )