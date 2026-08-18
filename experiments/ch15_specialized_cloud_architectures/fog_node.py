from .models import FogNode


class FogNodeManager:

    def __init__(self):

        self.nodes: dict[
            str,
            FogNode,
        ] = {}

    def register(
        self,
        node: FogNode,
    ):

        self.nodes[
            node.node_id
        ] = node

    def attach_edge_node(
        self,
        fog_id: str,
        edge_id: str,
    ):

        fog = self.nodes[
            fog_id
        ]

        if (
            edge_id
            not in fog.edge_nodes
        ):

            fog.edge_nodes.append(
                edge_id
            )

    def aggregate(
        self,
        fog_id: str,
        measurements: list[float],
    ):

        if not measurements:

            return {
                "fog_node": fog_id,
                "average": None,
            }

        return {
            "fog_node": fog_id,
            "average": (
                sum(measurements)
                / len(measurements)
            ),
        }