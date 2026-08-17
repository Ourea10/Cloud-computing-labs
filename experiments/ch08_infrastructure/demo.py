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


def demo_network():

    print("=== Logical Network Perimeter ===")

    perimeter = LogicalNetworkPerimeter(
        name="cloud-lab"
    )

    perimeter.add_rule(
        protocol=NetworkProtocol.TCP,
        port=443,
        source="0.0.0.0/0",
        action="allow",
    )

    perimeter.add_rule(
        protocol=NetworkProtocol.TCP,
        port=22,
        source="10.0.0.0/24",
        action="allow",
    )

    print(
        "Internet HTTPS:",
        perimeter.allows(
            NetworkProtocol.TCP,
            443,
            "203.0.113.10",
        ),
    )

    print(
        "Internet SSH:",
        perimeter.allows(
            NetworkProtocol.TCP,
            22,
            "203.0.113.10",
        ),
    )

    print(
        "Internal SSH:",
        perimeter.allows(
            NetworkProtocol.TCP,
            22,
            "10.0.0.10",
        ),
    )


def demo_virtualization():

    print("\n=== Hypervisor ===")

    host = PhysicalHost(
        host_id="host-001",
        total_cpu=8,
        total_memory_mb=16384,
    )

    hypervisor = Hypervisor(host)

    manager = VirtualServerManager()

    server_a = manager.create(
        server_id="server-a",
        tenant_id="tenant-a",
        cpu_cores=2,
        memory_mb=4096,
        image="ubuntu:24.04",
    )

    hypervisor.create_vm(
        server_a
    )

    print(
        "Used CPU:",
        host.used_cpu,
    )

    print(
        "Used memory:",
        host.used_memory_mb,
    )

    server_b = manager.create(
        server_id="server-b",
        tenant_id="tenant-b",
        cpu_cores=4,
        memory_mb=8192,
        image="ubuntu:24.04",
    )

    hypervisor.create_vm(
        server_b
    )

    print(
        "Used CPU:",
        host.used_cpu,
    )

    print(
        "Used memory:",
        host.used_memory_mb,
    )


def demo_storage():

    print("\n=== Cloud Storage ===")

    storage = CloudStorageManager()

    volume = storage.create_volume(
        volume_id="volume-001",
        tenant_id="tenant-a",
        storage_type="block",
        size_gb=20,
    )

    storage.attach(
        volume.volume_id,
        "server-a",
    )

    print(volume)


def demo_usage():

    print("\n=== Cloud Usage Monitor ===")

    monitor = CloudUsageMonitor()

    monitor.record(
        ResourceUsage(
            resource_id="server-a",
            cpu_percent=43.5,
            memory_mb=2100,
            network_bytes=500000,
            storage_bytes=1000000,
        )
    )

    monitor.record(
        ResourceUsage(
            resource_id="server-a",
            cpu_percent=67.2,
            memory_mb=2500,
            network_bytes=900000,
            storage_bytes=1200000,
        )
    )

    latest = monitor.latest(
        "server-a"
    )

    print(latest)


def demo_replication():

    print("\n=== Resource Replication ===")

    manager = VirtualServerManager()

    server = manager.create(
        server_id="server-source",
        tenant_id="tenant-a",
        cpu_cores=2,
        memory_mb=2048,
        image="ubuntu:24.04",
    )

    replicator = ResourceReplicator()

    replica = replicator.replicate_server(
        source=server,
        replica_id="server-replica",
    )

    print(
        "Source:",
        server.server_id,
        server.private_ip,
    )

    print(
        "Replica:",
        replica.server_id,
        replica.private_ip,
    )


def demo_ready_made_environment():

    print("\n=== Ready-Made Environment ===")

    manager = (
        ReadyMadeEnvironmentManager()
    )

    template = EnvironmentTemplate(
        template_id="fastapi-01",
        name="FastAPI Environment",
        base_image="python:3.12-slim",
        packages=(
            "fastapi",
            "uvicorn",
        ),
        environment_variables={
            "APP_ENV": "cloud-lab",
        },
    )

    manager.register(template)

    environment = manager.provision(
        template_id="fastapi-01",
        instance_id="env-001",
    )

    print(environment)


def demo_container():

    print("\n=== Container ===")

    manager = ContainerManager()

    container = manager.create(
        container_id="container-001",
        tenant_id="tenant-a",
        image="cloud-lab-api:1.0",
        cpu_limit=1.0,
        memory_limit_mb=512,
        server_id="server-a",
    )

    manager.start(
        container.container_id
    )

    print(container)


def main():

    demo_network()
    demo_virtualization()
    demo_storage()
    demo_usage()
    demo_replication()
    demo_ready_made_environment()
    demo_container()


if __name__ == "__main__":
    main()