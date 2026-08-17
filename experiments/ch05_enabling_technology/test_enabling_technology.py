import pytest

from experiments.ch01_introduction.resource import (
    ComputeResource,
)

from .network import NetworkPath
from .service_api import CloudResourceService
from .virtualization import Hypervisor


def test_hypervisor_creates_vm():
    host = ComputeResource(
        resource_id="host-01",
        cpu=8,
        memory=16384,
    )

    hypervisor = Hypervisor(host)

    vm = hypervisor.create_vm(
        vm_id="vm-01",
        cpu=4,
        memory=8192,
    )

    assert vm.host == host
    assert vm.cpu == 4
    assert vm.memory == 8192


def test_hypervisor_rejects_overallocation():
    host = ComputeResource(
        resource_id="host-01",
        cpu=4,
        memory=4096,
    )

    hypervisor = Hypervisor(host)

    hypervisor.create_vm(
        vm_id="vm-01",
        cpu=4,
        memory=4096,
    )

    with pytest.raises(RuntimeError):
        hypervisor.create_vm(
            vm_id="vm-02",
            cpu=1,
            memory=1024,
        )


def test_network_transfer_time():
    network = NetworkPath(
        latency_ms=10,
        bandwidth_mbps=100,
    )

    result = network.transfer_time_ms(
        1_000_000
    )

    assert result > 10


def test_service_api():
    service = CloudResourceService()

    created = service.create_resource(
        resource_id="resource-01",
        cpu=2,
        memory=4096,
    )

    assert created.status_code == 201

    result = service.get_resource(
        "resource-01"
    )

    assert result.status_code == 200
