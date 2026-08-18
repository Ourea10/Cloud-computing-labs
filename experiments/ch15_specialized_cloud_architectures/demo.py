from experiments.ch15_specialized_cloud_architectures.models import (
    ConnectionType,
    EdgeNode,
    FogNode,
    ResourceType,
    StorageResource,
    CloudProvider,
    ProviderStatus,
    FederatedResource,
)

from experiments.ch15_specialized_cloud_architectures.specialized_cloud_service import (
    SpecializedCloudService,
)


def main():

    service = (
        SpecializedCloudService()
    )

    # ==================================================
    # 1. Storage
    # ==================================================

    storage = StorageResource(
        storage_id="storage-001",
        name="primary-storage",
        capacity_gb=1000,
        used_gb=300,
        lun_id="lun-001",
    )

    service.storage.register(
        storage
    )

    print("=== STORAGE ===")

    print(
        "Before:",
        service.storage.available_capacity(
            "storage-001"
        ),
        "GB available",
    )

    service.storage.allocate(
        "storage-001",
        200,
    )

    print(
        "After:",
        service.storage.available_capacity(
            "storage-001"
        ),
        "GB available",
    )

    # ==================================================
    # 2. Direct I/O
    # ==================================================

    print("\n=== DIRECT I/O ===")

    service.direct_io.grant_access(
        resource_id="vm-001",
        lun_id="lun-001",
        client_id="application-001",
    )

    print(
        "Access:",
        service.direct_io.can_access(
            "application-001",
            "lun-001",
        ),
    )

    # ==================================================
    # 3. Virtual switch
    # ==================================================

    print("\n=== VIRTUAL SWITCH ===")

    service.virtual_switch.create(
        "switch-001",
        "application-switch",
    )

    service.virtual_switch.connect(
        "switch-001",
        "vm-001",
    )

    service.virtual_switch.connect(
        "switch-001",
        "vm-002",
    )

    print(
        service.virtual_switch.resources(
            "switch-001"
        )
    )

    # ==================================================
    # 4. Multipath
    # ==================================================

    print("\n=== MULTIPATH ===")

    service.multipath.add_path(
        "path-a",
        "vm-001",
        "storage-001",
        ConnectionType.NETWORK,
    )

    service.multipath.add_path(
        "path-b",
        "vm-001",
        "storage-001",
        ConnectionType.NETWORK,
    )

    print(
        "Available paths:",
        len(
            service.multipath.available_paths(
                "vm-001",
                "storage-001",
            )
        ),
    )

    service.multipath.fail_path(
        "path-a"
    )

    print(
        "After path-a failure:",
        len(
            service.multipath.available_paths(
                "vm-001",
                "storage-001",
            )
        ),
    )

    # ==================================================
    # 5. Edge computing
    # ==================================================

    print("\n=== EDGE ===")

    service.edge.register(
        EdgeNode(
            node_id="edge-001",
            name="factory-edge",
            location="factory-a",
            capabilities=[
                "camera-processing",
                "sensor-processing",
            ],
        )
    )

    service.edge.connect_device(
        "edge-001",
        "camera-001",
    )

    result = service.edge.process(
        "edge-001",
        {
            "temperature": 81.2,
            "object_detected": True,
        },
    )

    print(result)

    # ==================================================
    # 6. Fog computing
    # ==================================================

    print("\n=== FOG ===")

    service.fog.register(
        FogNode(
            node_id="fog-001",
            name="factory-fog",
            region="region-a",
        )
    )

    service.fog.attach_edge_node(
        "fog-001",
        "edge-001",
    )

    result = service.fog.aggregate(
        "fog-001",
        [80, 82, 78, 81],
    )

    print(result)

    # ==================================================
    # 7. Federation
    # ==================================================

    print("\n=== FEDERATED CLOUD ===")

    service.federation.register_provider(
        CloudProvider(
            provider_id="aws",
            name="AWS",
            region="ap-southeast-1",
            services=[
                "compute",
                "storage",
            ],
            status=ProviderStatus.AVAILABLE,
        )
    )

    service.federation.register_provider(
        CloudProvider(
            provider_id="azure",
            name="Azure",
            region="southeast-asia",
            services=[
                "compute",
                "storage",
            ],
            status=ProviderStatus.AVAILABLE,
        )
    )

    service.federation.add_resource(
        FederatedResource(
            resource_id="aws-vm-001",
            provider_id="aws",
            resource_type=ResourceType.VM,
            location="ap-southeast-1",
        )
    )

    service.federation.add_resource(
        FederatedResource(
            resource_id="azure-vm-001",
            provider_id="azure",
            resource_type=ResourceType.VM,
            location="southeast-asia",
        )
    )

    resources = (
        service.federation.find_resources(
            ResourceType.VM
        )
    )

    for resource in resources:

        print(
            resource.resource_id,
            resource.provider_id,
        )


if __name__ == "__main__":
    main()