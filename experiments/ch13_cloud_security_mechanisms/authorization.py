from .exceptions import AuthorizationError
from .models import Role, User


class AuthorizationService:

    def __init__(self):

        self.roles: dict[
            str,
            Role,
        ] = {}

    def register_role(
        self,
        role: Role,
    ) -> None:

        self.roles[
            role.name
        ] = role

    def has_permission(
        self,
        user: User,
        permission: str,
    ) -> bool:

        role = self.roles.get(
            user.role
        )

        if role is None:
            return False

        return permission in role.permissions

    def require_permission(
        self,
        user: User,
        permission: str,
    ) -> None:

        if not self.has_permission(
            user,
            permission,
        ):

            raise AuthorizationError(
                (
                    f"User '{user.username}' "
                    f"does not have permission "
                    f"'{permission}'"
                )
            )