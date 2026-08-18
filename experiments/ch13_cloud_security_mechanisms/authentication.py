import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from .exceptions import (
    AuthenticationError,
    ExpiredTokenError,
    InvalidTokenError,
)

from .models import (
    AccessToken,
    User,
)


class AuthenticationService:

    def __init__(
        self,
        token_ttl_minutes: int = 30,
    ):

        self.users: dict[
            str,
            User,
        ] = {}

        self.tokens: dict[
            str,
            AccessToken,
        ] = {}

        self.token_ttl_minutes = (
            token_ttl_minutes
        )

    def hash_password(
        self,
        password: str,
    ) -> str:

        salt = secrets.token_bytes(16)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            100_000,
        )

        return (
            salt.hex()
            + ":"
            + password_hash.hex()
        )

    def verify_password(
        self,
        password: str,
        stored_hash: str,
    ) -> bool:

        salt_hex, hash_hex = (
            stored_hash.split(":")
        )

        salt = bytes.fromhex(
            salt_hex
        )

        expected = bytes.fromhex(
            hash_hex
        )

        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            100_000,
        )

        return hmac.compare_digest(
            actual,
            expected,
        )

    def register_user(
        self,
        user_id: str,
        username: str,
        password: str,
        role: str,
    ) -> User:

        password_hash = (
            self.hash_password(
                password
            )
        )

        user = User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            role=role,
        )

        self.users[user_id] = user

        return user

    def login(
        self,
        username: str,
        password: str,
    ) -> AccessToken:

        user = next(
            (
                user
                for user in self.users.values()
                if user.username == username
            ),
            None,
        )

        if user is None:

            raise AuthenticationError(
                "Invalid username or password"
            )

        if not self.verify_password(
            password,
            user.password_hash,
        ):

            raise AuthenticationError(
                "Invalid username or password"
            )

        token = secrets.token_urlsafe(32)

        access_token = AccessToken(
            token=token,
            user_id=user.user_id,
            expires_at=(
                datetime.now(timezone.utc)
                + timedelta(
                    minutes=self.token_ttl_minutes
                )
            ),
        )

        self.tokens[token] = (
            access_token
        )

        return access_token

    def authenticate(
        self,
        token: str,
    ) -> User:

        access_token = self.tokens.get(
            token
        )

        if access_token is None:

            raise InvalidTokenError(
                "Invalid access token"
            )

        if (
            datetime.now(timezone.utc)
            >= access_token.expires_at
        ):

            del self.tokens[token]

            raise ExpiredTokenError(
                "Access token has expired"
            )

        user = self.users.get(
            access_token.user_id
        )

        if user is None:

            raise InvalidTokenError(
                "User no longer exists"
            )

        return user

    def logout(
        self,
        token: str,
    ) -> None:

        self.tokens.pop(
            token,
            None,
        )