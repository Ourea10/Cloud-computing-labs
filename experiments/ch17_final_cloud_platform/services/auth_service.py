import hashlib
import uuid

from ..models import User
from ..repositories.user_repository import (
    UserRepository,
)
from ..exceptions import (
    UserAlreadyExistsError,
    AuthenticationError,
)

class AuthService:

    def __init__(
        self,
        repository: UserRepository,
    ):

        self.repository = repository

    def _hash_password(
        self,
        password: str,
    ):

        return hashlib.sha256(
            password.encode()
        ).hexdigest()

    def register(
        self,
        email: str,
        password: str,
    ):

        existing = (
            self.repository.find_by_email(
                email
            )
        )

        if existing:

            raise UserAlreadyExistsError(
                "User already exists"
            )

        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=(
                self._hash_password(
                    password
                )
            ),
        )

        return self.repository.create(
            user
        )

    def authenticate(
        self,
        email: str,
        password: str,
    ):

        user = (
            self.repository.find_by_email(
                email
            )
        )

        if not user:

            return None

        if user.password_hash != (
            self._hash_password(
                password
            )
        ):

            return None

        return user