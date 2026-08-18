from .models import StorageResource
from .exceptions import ResourceNotFoundError


class StorageManager:

    def __init__(self):

        self.resources: dict[
            str,
            StorageResource,
        ] = {}

    def register(
        self,
        storage: StorageResource,
    ):

        self.resources[
            storage.storage_id
        ] = storage

    def get(
        self,
        storage_id: str,
    ) -> StorageResource:

        if storage_id not in self.resources:

            raise ResourceNotFoundError(
                f"Storage not found: "
                f"{storage_id}"
            )

        return self.resources[
            storage_id
        ]

    def allocate(
        self,
        storage_id: str,
        amount_gb: int,
    ):

        storage = self.get(
            storage_id
        )

        if (
            storage.used_gb
            + amount_gb
            > storage.capacity_gb
        ):

            raise ValueError(
                "Storage capacity exceeded"
            )

        storage.used_gb += amount_gb

    def available_capacity(
        self,
        storage_id: str,
    ) -> int:

        storage = self.get(
            storage_id
        )

        return (
            storage.capacity_gb
            - storage.used_gb
        )