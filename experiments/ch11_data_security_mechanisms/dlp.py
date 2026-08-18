from experiments.ch11_data_security_mechanisms.models import (
    DataClassification,
    DLPAction,
    DLPEvent,
    DLPPolicy,
    FileObject,
)


class DLPSystem:

    def __init__(self):

        self.policies: list[
            DLPPolicy
        ] = []

    def add_policy(
        self,
        policy: DLPPolicy,
    ) -> None:

        self.policies.append(policy)

    def evaluate(
        self,
        file: FileObject,
        user_id: str,
        destination: str,
        destination_type: str,
    ) -> DLPEvent:

        for policy in self.policies:

            if (
                policy.classification
                == file.classification
                and policy.destination_type
                == destination_type
            ):

                return DLPEvent(
                    file_id=file.file_id,
                    user_id=user_id,
                    destination=destination,
                    action=policy.action,
                    reason=(
                        f"Policy '{policy.name}' "
                        f"matched"
                    ),
                )

        return DLPEvent(
            file_id=file.file_id,
            user_id=user_id,
            destination=destination,
            action=DLPAction.ALLOW,
            reason="No DLP policy matched",
        )