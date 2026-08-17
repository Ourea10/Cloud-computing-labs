import pytest

from resource import ComputeResource
from resource_pool import ResourcePool


def create_pool():
    pool = ResourcePool()

    pool.add(
        ComputeResource(
            resource_id="server-01",
            cpu=4,
            memory=8192,
        )
    )

    pool.add(
        ComputeResource(
            resource_id="server-02",
            cpu=8,
            memory=16384,
        )
    )

    return pool


def test_resource_is_allocated():
    pool = create_pool()

    resource = pool.allocate(
        cpu=2,
        memory=4096,
    )

    assert resource.resource_id == "server-01"
    assert resource.allocated is True


def test_resource_can_be_released():
    pool = create_pool()

    resource = pool.allocate(
        cpu=2,
        memory=4096,
    )

    pool.release(resource.resource_id)

    assert resource.allocated is False


def test_resource_exhaustion():
    pool = ResourcePool()

    pool.add(
        ComputeResource(
            resource_id="server-01",
            cpu=2,
            memory=2048,
        )
    )

    pool.allocate(
        cpu=2,
        memory=2048,
    )

    with pytest.raises(RuntimeError):
        pool.allocate(
            cpu=2,
            memory=2048,
        )