from experiments.ch08_infrastructure.container import (
    ContainerManager,
)

from experiments.ch08_infrastructure.hypervisor import (
    Hypervisor,
    PhysicalHost,
)

from experiments.ch08_infrastructure.models import (
    StorageType,
)

from experiments.ch08_infrastructure.network_perimeter import (
    LogicalNetworkPerimeter,
)

from experiments.ch08_infrastructure.ready_made_environment import (
    ReadyMadeEnvironmentManager,
)

from experiments.ch08_infrastructure.replication import (
    ResourceReplicator,
)

from experiments.ch08_infrastructure.storage import (
    CloudStorageManager,
)

from experiments.ch08_infrastructure.usage_monitor import (
    CloudUsageMonitor,
)

from experiments.ch08_infrastructure.virtual_server import (
    VirtualServerManager,
)


class CloudInfrastructure:

    def __init__(self):

        self.network = (
            LogicalNetworkPerimeter(
                name="cloud-lab"
            )
        )

        self.host = PhysicalHost(
            host_id="host-001",
            total_cpu=16,
            total_memory_mb=32768,
        )

        self.hypervisor = Hypervisor(
            self.host
        )

        self.server_manager = (
            VirtualServerManager()
        )

        self.storage = (
            CloudStorageManager()
        )

        self.monitor = (
            CloudUsageMonitor()
        )

        self.replicator = (
            ResourceReplicator()
        )

        self.environment_manager = (
            ReadyMadeEnvironmentManager()
        )

        self.container_manager = (
            ContainerManager()
        )

    def create_server(
        self,
        server_id: str,
        tenant_id: str,
        cpu: int,
        memory_mb: int,
        image: str,
    ):

        server = self.server_manager.create(
            server_id=server_id,
            tenant_id=tenant_id,
            cpu_cores=cpu,
            memory_mb=memory_mb,
            image=image,
        )

        return self.hypervisor.create_vm(
            server
        )

    def create_storage(
        self,
        volume_id: str,
        tenant_id: str,
        size_gb: int,
    ):

        return self.storage.create_volume(
            volume_id=volume_id,
            tenant_id=tenant_id,
            storage_type=StorageType.BLOCK,
            size_gb=size_gb,
        )
