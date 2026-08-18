from datetime import datetime, timedelta

import pytest

from .direct_io import (
    DirectIOManager,
)

from .edge_node import (
    EdgeNodeManager,
)

from .fog_node import (
    FogNodeManager,
)

from .models import (
    ConnectionType,
    EdgeNode,
    FogNode,
    PathStatus,
    ResourceType,
    StorageResource,
)

from .multipath import (
    MultipathManager,
)

from .storage import (
    StorageManager,
)


def test_storage_allocation():

    manager = StorageManager()

    manager.register(
        StorageResource(
            storage_id="storage-001",
            name="storage",
            capacity_gb=1000,
            used_gb=300,
            lun_id="lun-001",
        )
    )

    manager.allocate(
        "storage-001",
        200,
    )

    assert (
        manager.available_capacity(
            "storage-001"
        )
        == 500
    )


def test_storage_capacity_limit():

    manager = StorageManager()

    manager.register(
        StorageResource(
            storage_id="storage-001",
            name="storage",
            capacity_gb=1000,
            used_gb=900,
            lun_id="lun-001",
        )
    )

    with pytest.raises(
        ValueError
    ):

        manager.allocate(
            "storage-001",
            200,
        )


def test_direct_io():

    manager = DirectIOManager()

    manager.grant_access(
        "vm-001",
        "lun-001",
        "client-001",
    )

    assert manager.can_access(
        "client-001",
        "lun-001",
    )


def test_direct_io_revoke():

    manager = DirectIOManager()

    manager.grant_access(
        "vm-001",
        "lun-001",
        "client-001",
    )

    manager.revoke_access(
        "client-001",
        "lun-001",
    )

    assert not manager.can_access(
        "client-001",
        "lun-001",
    )


def test_multipath_failover():

    manager = MultipathManager()

    manager.add_path(
        "path-a",
        "vm-001",
        "storage-001",
        ConnectionType.NETWORK,
    )

    manager.add_path(
        "path-b",
        "vm-001",
        "storage-001",
        ConnectionType.NETWORK,
    )

    assert len(
        manager.available_paths(
            "vm-001",
            "storage-001",
        )
    ) == 2

    manager.fail_path(
        "path-a"
    )

    paths = manager.available_paths(
        "vm-001",
        "storage-001",
    )

    assert len(paths) == 1
    assert paths[0].path_id == "path-b"


def test_edge_processing():

    manager = EdgeNodeManager()

    manager.register(
        EdgeNode(
            node_id="edge-001",
            name="edge",
            location="factory-a",
            capabilities=[
                "sensor-processing"
            ],
        )
    )

    result = manager.process(
        "edge-001",
        {
            "temperature": 80
        },
    )

    assert result["processed"] is True


def test_fog_aggregation():

    manager = FogNodeManager()

    manager.register(
        FogNode(
            node_id="fog-001",
            name="fog",
            region="region-a",
        )
    )

    result = manager.aggregate(
        "fog-001",
        [80, 82, 78, 80],
    )

    assert result["average"] == 80


def test_empty_fog_data():

    manager = FogNodeManager()

    manager.register(
        FogNode(
            node_id="fog-001",
            name="fog",
            region="region-a",
        )
    )

    result = manager.aggregate(
        "fog-001",
        [],
    )

    assert result["average"] is None