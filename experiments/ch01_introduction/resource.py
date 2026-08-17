from dataclasses import dataclass


@dataclass
class ComputeResource:
    resource_id: str
    cpu: int
    memory: int
    allocated: bool = False

    def allocate(self):
        if self.allocated:
            raise RuntimeError(
                f"Resource {self.resource_id} is already allocated"
            )

        self.allocated = True

    def release(self):
        self.allocated = False