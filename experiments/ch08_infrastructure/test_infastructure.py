import pytest

from experiments.ch08_infrastructure.container import (
    ContainerManager,
)

from experiments.ch08_infrastructure.hypervisor import (
    Hypervisor,
    PhysicalHost,
)

from experiments.ch08_infrastructure.models import (
    NetworkProtocol,
    ResourceUsage,
    StorageType,
)

from experiments.ch08_infrastructure.network_perimeter import (
    LogicalNetworkPerimeter,
)

from experiments.ch08_infrastructure.ready_made_environment import (
    EnvironmentTemplate,
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


def test_network_perimeter_allows_https():

    perimeter = LogicalNetworkPerimeter(
        name="test"
    )

    perimeter.add_rule(
        NetworkProtocol.TCP,
        443,
        "0.0.0.0/0",
        "allow",
    )

    assert perimeter.allows(
        NetworkProtocol.TCP,
        443,
        "1.2.3.4",
    )


def test_network_perimeter_blocks_ssh_from_internet():

    perimeter = LogicalNetworkPerimeter(
        name="test"
    )

    perimeter.add_rule(
        NetworkProtocol.TCP,
        22,
        "10.0.0.0/24",
        "allow",
    )

    assert not perimeter.allows(
        NetworkProtocol.TCP,
        22,
        "1.2.3.4",
    )


def test_hypervisor_allocates_vm():

    host = PhysicalHost(
        host_id="host",
        total_cpu=4,
        total_memory_mb=8192,
    )

    hypervisor = Hypervisor(host)

    manager = VirtualServerManager()

    server = manager.create(
        server_id="vm-1",
        tenant_id="tenant-a",
        cpu_cores=2,
        memory_mb=4096,
        image="ubuntu",
    )

    hypervisor.create_vm(server)

    assert host.used_cpu == 2
    assert host.used_memory_mb == 4096


def test_hypervisor_rejects_over_allocation():

    host = PhysicalHost(
        host_id="host",
        total_cpu=4,
        total_memory_mb=8192,
    )

    hypervisor = Hypervisor(host)

    manager = VirtualServerManager()

    server = manager.create(
        server_id="vm-1",
        tenant_id="tenant-a",
        cpu_cores=8,
        memory_mb=4096,
        image="ubuntu",
    )

    with pytest.raises(RuntimeError):
        hypervisor.create_vm(server)


def test_storage_can_attach():

    manager = CloudStorageManager()

    volume = manager.create_volume(
        volume_id="volume-1",
        tenant_id="tenant-a",
        storage_type=StorageType.BLOCK,
        size_gb=20,
    )

    manager.attach(
        volume.volume_id,
        "server-1",
    )

    assert (
        volume.attached_server_id
        == "server-1"
    )


def test_storage_cannot_attach_twice():

    manager = CloudStorageManager()

    volume = manager.create_volume(
        volume_id="volume-1",
        tenant_id="tenant-a",
        storage_type=StorageType.BLOCK,
        size_gb=20,
    )

    manager.attach(
        volume.volume_id,
        "server-1",
    )

    with pytest.raises(RuntimeError):
        manager.attach(
            volume.volume_id,
            "server-2",
        )


def test_usage_monitor_records_usage():

    monitor = CloudUsageMonitor()

    monitor.record(
        ResourceUsage(
            resource_id="server-1",
            cpu_percent=50,
            memory_mb=1024,
            network_bytes=100,
            storage_bytes=200,
        )
    )

    latest = monitor.latest(
        "server-1"
    )

    assert latest is not None
    assert (
        latest.usage.cpu_percent
        == 50
    )


def test_resource_replication():

    manager = VirtualServerManager()

    source = manager.create(
        server_id="source",
        tenant_id="tenant-a",
        cpu_cores=2,
        memory_mb=2048,
        image="ubuntu",
    )

    source_ip = source.private_ip

    replicator = ResourceReplicator()

    replica = replicator.replicate_server(
        source,
        "replica",
    )

    assert replica.server_id == "replica"
    assert replica.private_ip is None
    assert source.private_ip == source_ip


def test_ready_made_environment():

    manager = (
        ReadyMadeEnvironmentManager()
    )

    template = EnvironmentTemplate(
        template_id="python",
        name="Python",
        base_image="python:3.12",
        packages=(
            "fastapi",
            "uvicorn",
        ),
    )

    manager.register(template)

    instance = manager.provision(
        "python",
        "env-1",
    )

    assert instance.template_id == "python"
    assert "fastapi" in instance.packages


def test_container_can_start():

    manager = ContainerManager()

    container = manager.create(
        container_id="container-1",
        tenant_id="tenant-a",
        image="api:1",
        cpu_limit=1,
        memory_limit_mb=512,
        server_id="server-1",
    )

    assert not container.running

    manager.start(
        container.container_id
    )

    assert container.running