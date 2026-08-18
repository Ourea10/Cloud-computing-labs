from abc import ABC, abstractmethod


class StorageProvider(ABC):

    @abstractmethod
    def put(
        self,
        key: str,
        data: bytes,
    ):
        pass

    @abstractmethod
    def get(
        self,
        key: str,
    ):
        pass


class LocalStorageProvider(
    StorageProvider
):

    def __init__(self):

        self.objects = {}

    def put(
        self,
        key,
        data,
    ):

        self.objects[
            key
        ] = data

    def get(
        self,
        key,
    ):

        return self.objects.get(
            key
        )