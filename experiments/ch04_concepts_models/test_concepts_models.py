import pytest

from experiments.ch01_introduction.resource import (
    ComputeResource,
)

from .cloud_environment import CloudEnvironment
from .tenant import Tenant


def create_environment():
    environment = CloudEnvironment()

    environment.add_resource(
        ComputeResource(
            resource_id="server-01",
            cpu=8,
            memory=16384,
        )
    )

    environment.add_resource(
        ComputeResource(
            resource_id="server-02",
            cpu=8,
            memory=16384,
        )
    )

    environment.register_tenant(
        Tenant(
            tenant_id="tenant-a",
            name="Company A",
        )
    )

    environment.register_tenant(
        Tenant(
            tenant_id="tenant-b",
            name="Company B",
        )
    )

    return environment


def test_tenant_can_allocate_resource():
    environment = create_environment()

    resource = environment.allocate(
        tenant_id="tenant-a",
        cpu=4,
        memory=4096,
    )

    resources = environment.resources_for_tenant(
        "tenant-a"
    )

    assert resource in resources


def test_tenant_isolation():
    environment = create_environment()

    resource = environment.allocate(
        tenant_id="tenant-a",
        cpu=4,
        memory=4096,
    )

    with pytest.raises(ValueError):
        environment.release(
            tenant_id="tenant-b",
            resource_id=resource.resource_id,
        )
