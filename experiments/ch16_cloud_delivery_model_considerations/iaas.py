from dataclasses import dataclass


@dataclass
class VirtualMachine:

    vm_id: str
    cpu: int
    memory_gb: int
    disk_gb: int

    operating_system: str | None = None
    runtime: str | None = None


class IaaSProvider:

    def __init__(self):

        self.vms: dict[
            str,
            VirtualMachine,
        ] = {}

    def provision_vm(
        self,
        vm_id: str,
        cpu: int,
        memory_gb: int,
        disk_gb: int,
    ):

        vm = VirtualMachine(
            vm_id=vm_id,
            cpu=cpu,
            memory_gb=memory_gb,
            disk_gb=disk_gb,
        )

        self.vms[
            vm_id
        ] = vm

        return vm

    def configure_os(
        self,
        vm_id: str,
        operating_system: str,
    ):

        vm = self.vms[
            vm_id
        ]

        vm.operating_system = (
            operating_system
        )

    def configure_runtime(
        self,
        vm_id: str,
        runtime: str,
    ):

        vm = self.vms[
            vm_id
        ]

        vm.runtime = runtime