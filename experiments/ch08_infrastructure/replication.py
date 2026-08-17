from copy import deepcopy
from dataclasses import dataclass

from experiments.ch08_infrastructure.models import (
    StorageVolume,
    VirtualServer,
)


@dataclass(frozen=True)
class ReplicationRecord:

    source_id: str
    replica_id: str
    resource_type: str


class ResourceReplicator:

    def __init__(self):

        self.records: list[
            ReplicationRecord
        ] = []

    def replicate_server(
        self,
        source: VirtualServer,
        replica_id: str,
    ) -> VirtualServer:

        replica = deepcopy(source)

        replica.server_id = replica_id

        replica.private_ip = None
        replica.public_ip = None

        self.records.append(
            ReplicationRecord(
                source_id=source.server_id,
                replica_id=replica_id,
                resource_type="virtual_server",
            )
        )

        return replica

    def replicate_volume(
        self,
        source: StorageVolume,
        replica_id: str,
    ) -> StorageVolume:

        replica = deepcopy(source)

        replica.volume_id = replica_id

        replica.attached_server_id = None

        self.records.append(
            ReplicationRecord(
                source_id=source.volume_id,
                replica_id=replica_id,
                resource_type="storage",
            )
        )

        return replica