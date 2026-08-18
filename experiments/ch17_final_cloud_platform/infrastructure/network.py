from abc import ABC, abstractmethod


class NetworkProvider(ABC):

    @abstractmethod
    def create_network(
        self,
        name: str,
        cidr: str,
    ):
        pass

    @abstractmethod
    def create_subnet(
        self,
        network_id: str,
        name: str,
        cidr: str,
    ):
        pass


class LocalNetworkProvider(
    NetworkProvider
):

    def __init__(self):

        self.networks = {}
        self.subnets = {}

    def create_network(
        self,
        name: str,
        cidr: str,
    ):

        network_id = (
            f"local-vpc-{len(self.networks) + 1}"
        )

        self.networks[network_id] = {
            "name": name,
            "cidr": cidr,
        }

        return network_id

    def create_subnet(
        self,
        network_id: str,
        name: str,
        cidr: str,
    ):

        if network_id not in self.networks:
            raise ValueError(
                "Network does not exist"
            )

        subnet_id = (
            f"local-subnet-{len(self.subnets) + 1}"
        )

        self.subnets[subnet_id] = {
            "network_id": network_id,
            "name": name,
            "cidr": cidr,
        }

        return subnet_id