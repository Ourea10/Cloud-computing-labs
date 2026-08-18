from abc import ABC, abstractmethod


class ComputeProvider(ABC):

    @abstractmethod
    def create(
        self,
        name: str,
    ):
        pass

    @abstractmethod
    def delete(
        self,
        resource_id: str,
    ):
        pass


class LocalComputeProvider(
    ComputeProvider
):

    def __init__(self):

        self.resources = {}

    def create(
        self,
        name,
    ):

        resource_id = (
            f"local-compute-{len(self.resources) + 1}"
        )

        self.resources[
            resource_id
        ] = {
            "name": name,
            "status": "running",
        }

        return resource_id

    def delete(
        self,
        resource_id,
    ):

        self.resources.pop(
            resource_id,
            None,
        )