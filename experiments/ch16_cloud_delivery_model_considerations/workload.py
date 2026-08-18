from .models import Workload


class WorkloadManager:

    def __init__(self):

        self.workloads: dict[
            str,
            Workload,
        ] = {}

    def register(
        self,
        workload: Workload,
    ):

        self.workloads[
            workload.workload_id
        ] = workload

    def get(
        self,
        workload_id: str,
    ):

        return self.workloads[
            workload_id
        ]

    def list(self):

        return list(
            self.workloads.values()
        )