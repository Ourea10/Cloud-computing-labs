from .models import EdgeNode


class EdgeNodeManager:

    def __init__(self):

        self.nodes: dict[
            str,
            EdgeNode,
        ] = {}

    def register(
        self,
        node: EdgeNode,
    ):

        self.nodes[
            node.node_id
        ] = node

    def connect_device(
        self,
        node_id: str,
        device_id: str,
    ):

        node = self.nodes[
            node_id
        ]

        if (
            device_id
            not in node.connected_devices
        ):

            node.connected_devices.append(
                device_id
            )

    def process(
        self,
        node_id: str,
        data: dict,
    ) -> dict:

        node = self.nodes[
            node_id
        ]

        result = {
            "node_id": node.node_id,
            "location": node.location,
            "processed": True,
            "data": data,
        }

        return result