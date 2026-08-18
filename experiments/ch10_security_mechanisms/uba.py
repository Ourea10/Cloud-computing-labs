from dataclasses import dataclass


@dataclass(frozen=True)
class UserBehavior:
    user_id: str
    login_count: int
    failed_login_count: int
    resource_actions: int


class UserBehaviorAnalytics:

    def analyze(
        self,
        behavior: UserBehavior,
    ) -> list[str]:

        anomalies = []

        if (
            behavior.failed_login_count
            > 10
        ):

            anomalies.append(
                "excessive_failed_logins"
            )

        if (
            behavior.resource_actions
            > 100
        ):

            anomalies.append(
                "unusual_resource_activity"
            )

        return anomalies