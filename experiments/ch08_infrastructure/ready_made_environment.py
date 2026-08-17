from copy import deepcopy
from dataclasses import dataclass

from experiments.ch08_infrastructure.models import (
    StorageVolume,
    VirtualServer,
)


@dataclass(frozen=True)
class EnvironmentTemplate:
    template_id: str
    name: str
    base_image: str
    packages: tuple[str, ...] = ()
    environment_variables: dict[str, str] | None = None


@dataclass(frozen=True)
class EnvironmentInstance:
    instance_id: str
    template_id: str
    name: str
    base_image: str
    packages: tuple[str, ...]
    environment_variables: dict[str, str]


class ReadyMadeEnvironmentManager:
    def __init__(self):
        self.templates: dict[str, EnvironmentTemplate] = {}
        self.instances: dict[str, EnvironmentInstance] = {}

    def register(self, template: EnvironmentTemplate) -> None:
        if template.template_id in self.templates:
            raise ValueError("Environment template already exists")

        self.templates[template.template_id] = template

    def provision(
        self,
        template_id: str,
        instance_id: str,
    ) -> EnvironmentInstance:
        if template_id not in self.templates:
            raise ValueError("Unknown environment template")

        if instance_id in self.instances:
            raise ValueError("Environment instance already exists")

        template = self.templates[template_id]
        instance = EnvironmentInstance(
            instance_id=instance_id,
            template_id=template.template_id,
            name=template.name,
            base_image=template.base_image,
            packages=template.packages,
            environment_variables=dict(template.environment_variables or {}),
        )
        self.instances[instance_id] = instance
        return instance


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
