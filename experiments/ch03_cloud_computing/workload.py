from dataclasses import dataclass


@dataclass
class Workload:
    name: str
    cpu_demand: float
    memory_demand: float

    @property
    def total_demand(self) -> float:
        return (
            self.cpu_demand
            + self.memory_demand
        )