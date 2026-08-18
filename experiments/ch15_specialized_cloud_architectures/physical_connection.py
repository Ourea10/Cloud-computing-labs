from .models import (
    ConnectionPath,
    ConnectionType,
    PathStatus,
)


class PhysicalConnectionManager:

    def __init__(self):

        self.connections: dict[
            str,
            ConnectionPath,
        ] = {}

    def connect(
        self,
        connection_id: str,
        source_id: str,
        target_id: str,
    ):

        connection = ConnectionPath(
            path_id=connection_id,
            source_id=source_id,
            target_id=target_id,
            connection_type=(
                ConnectionType.PHYSICAL
            ),
            status=PathStatus.ACTIVE,
        )

        self.connections[
            connection_id
        ] = connection

        return connection

    def disconnect(
        self,
        connection_id: str,
    ):

        self.connections[
            connection_id
        ].status = PathStatus.FAILED

    def active_connections(self):

        return [
            connection
            for connection
            in self.connections.values()
            if connection.status
            == PathStatus.ACTIVE
        ]