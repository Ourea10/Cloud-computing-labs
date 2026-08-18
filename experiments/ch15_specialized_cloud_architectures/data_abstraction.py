from abc import ABC, abstractmethod


class DataProvider(ABC):

    @abstractmethod
    def get_data(
        self,
        key: str,
    ):
        pass


class LocalDataProvider(
    DataProvider
):

    def __init__(self):

        self.data = {}

    def put(
        self,
        key: str,
        value,
    ):

        self.data[key] = value

    def get_data(
        self,
        key: str,
    ):

        return self.data.get(
            key
        )


class EdgeDataProvider(
    DataProvider
):

    def __init__(self):

        self.data = {}

    def put(
        self,
        key: str,
        value,
    ):

        self.data[key] = value

    def get_data(
        self,
        key: str,
    ):

        return self.data.get(
            key
        )


class CloudDataProvider(
    DataProvider
):

    def __init__(self):

        self.data = {}

    def put(
        self,
        key: str,
        value,
    ):

        self.data[key] = value

    def get_data(
        self,
        key: str,
    ):

        return self.data.get(
            key
        )