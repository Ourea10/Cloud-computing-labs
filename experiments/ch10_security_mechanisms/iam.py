from experiments.ch10_security_mechanisms.models import (
    AccessDecision,
    Role,
    User,
    UserStatus,
)


class IAMService:

    def __init__(self):

        self.users: dict[
            str,
            User,
        ] = {}

        self.roles: dict[
            str,
            Role,
        ] = {}

        self.user_roles: dict[
            str,
            set[str],
        ] = {}

    def add_user(
        self,
        user: User,
    ) -> None:

        self.users[user.user_id] = user

    def add_role(
        self,
        role: Role,
    ) -> None:

        self.roles[role.name] = role

    def assign_role(
        self,
        user_id: str,
        role_name: str,
    ) -> None:

        self.user_roles.setdefault(
            user_id,
            set(),
        ).add(role_name)

    def authorize(
        self,
        user_id: str,
        permission: str,
    ) -> AccessDecision:

        user = self.users[user_id]

        if user.status != UserStatus.ACTIVE:
            return AccessDecision.DENY

        role_names = self.user_roles.get(
            user_id,
            set(),
        )

        for role_name in role_names:

            role = self.roles[role_name]

            if permission in role.permissions:
                return AccessDecision.ALLOW

        return AccessDecision.DENY