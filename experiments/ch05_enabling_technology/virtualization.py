from dataclasses import dataclass

from experiments.ch01_introduction.resource import (
    ComputeResource,
)


@dataclass
class VirtualMachine:
    vm_id: str
    cpu: int
    memory: int
    host: ComputeResource | None = None
    running: bool = False


class Hypervisor:
    def __init__(
        self,
        host: ComputeResource,
    ):
        self.host = host
        self.virtual_machines: list[
            VirtualMachine
        ] = []

    @property
    def allocated_cpu(self) -> int:
        return sum(
            vm.cpu
            for vm in self.virtual_machines
        )

    @property
    def allocated_memory(self) -> int:
        return sum(
            vm.memory
            for vm in self.virtual_machines
        )

    def create_vm(
        self,
        vm_id: str,
        cpu: int,
        memory: int,
    ) -> VirtualMachine:

        if (
            self.allocated_cpu + cpu
            > self.host.cpu
        ):
            raise RuntimeError(
                "Insufficient CPU capacity"
            )

        if (
            self.allocated_memory + memory
            > self.host.memory
        ):
            raise RuntimeError(
                "Insufficient memory capacity"
            )

        vm = VirtualMachine(
            vm_id=vm_id,
            cpu=cpu,
            memory=memory,
            host=self.host,
        )

        self.virtual_machines.append(vm)

        return vm

    def start_vm(
        self,
        vm: VirtualMachine,
    ):
        vm.running = True