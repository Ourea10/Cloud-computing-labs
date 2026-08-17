from experiments.ch01_introduction.resource import (
    ComputeResource,
)

from .network import NetworkPath
from .service_api import CloudResourceService
from .virtualization import Hypervisor


def run_virtualization_demo():
    print("=== Virtualization ===")

    host = ComputeResource(
        resource_id="physical-server-01",
        cpu=8,
        memory=16384,
    )

    hypervisor = Hypervisor(host)

    vm1 = hypervisor.create_vm(
        vm_id="vm-01",
        cpu=2,
        memory=4096,
    )

    vm2 = hypervisor.create_vm(
        vm_id="vm-02",
        cpu=4,
        memory=8192,
    )

    hypervisor.start_vm(vm1)
    hypervisor.start_vm(vm2)

    print(
        f"Host: {host.resource_id}"
    )

    for vm in hypervisor.virtual_machines:
        print(
            vm.vm_id,
            vm.cpu,
            vm.memory,
            vm.running,
        )


def run_network_demo():
    print("\n=== Network ===")

    network = NetworkPath(
        latency_ms=10,
        bandwidth_mbps=100,
    )

    transfer_time = network.transfer_time_ms(
        payload_size_bytes=1_000_000
    )

    print(
        f"Transfer time: "
        f"{transfer_time:.2f} ms"
    )


def run_api_demo():
    print("\n=== Service API ===")

    service = CloudResourceService()

    response = service.create_resource(
        resource_id="resource-01",
        cpu=4,
        memory=8192,
    )

    print(response.status_code)
    print(response.body)

    response = service.get_resource(
        "resource-01"
    )

    print(response.status_code)
    print(response.body)


def main():
    run_virtualization_demo()
    run_network_demo()
    run_api_demo()


if __name__ == "__main__":
    main()
