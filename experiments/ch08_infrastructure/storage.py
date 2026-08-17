from experiments.ch08_infrastructure.models import (
    StorageType,
    StorageVolume,
)


class CloudStorageManager:

    def __init__(self):
        self.volumes: dict[
            str,
            StorageVolume,
        ] = {}

    def create_volume(
        self,
        volume_id: str,
        tenant_id: str,
        storage_type: StorageType,
        size_gb: int,
    ) -> StorageVolume:

        if volume_id in self.volumes:
            raise ValueError(
                "Volume already exists"
            )

        if size_gb <= 0:
            raise ValueError(
                "Volume size must be positive"
            )

        volume = StorageVolume(
            volume_id=volume_id,
            tenant_id=tenant_id,
            storage_type=storage_type,
            size_gb=size_gb,
        )

        self.volumes[volume_id] = volume

        return volume

    def attach(
        self,
        volume_id: str,
        server_id: str,
    ) -> None:

        volume = self.volumes.get(
            volume_id
        )

        if volume is None:
            raise KeyError(
                "Volume not found"
            )

        if volume.attached_server_id:
            raise RuntimeError(
                "Volume is already attached"
            )

        volume.attached_server_id = server_id

    def detach(
        self,
        volume_id: str,
    ) -> None:

        volume = self.volumes.get(
            volume_id
        )

        if volume is None:
            raise KeyError(
                "Volume not found"
            )

        volume.attached_server_id = None