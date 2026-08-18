from .models import (
    ConnectionPath,
    PathStatus,
    ConnectionType,
)

from .exceptions import (
    NoAvailablePathError,
)


class MultipathManager:

    def __init__(self):

        self.paths: dict[
            str,
            ConnectionPath,
        ] = {}

    def add_path(
        self,
        path_id: str,
        source_id: str,
        target_id: str,
        connection_type: ConnectionType,
    ):

        path = ConnectionPath(
            path_id=path_id,
            source_id=source_id,
            target_id=target_id,
            connection_type=connection_type,
            status=PathStatus.ACTIVE,
        )

        self.paths[
            path_id
        ] = path

    def fail_path(
        self,
        path_id: str,
    ):

        self.paths[
            path_id
        ].status = PathStatus.FAILED

    def restore_path(
        self,
        path_id: str,
    ):

        self.paths[
            path_id
        ].status = PathStatus.ACTIVE

    def set_maintenance(
        self,
        path_id: str,
    ):

        self.paths[
            path_id
        ].status = PathStatus.MAINTENANCE

    def get_available_path(
        self,
        source_id: str,
        target_id: str,
    ):

        for path in self.paths.values():

            if (
                path.source_id
                == source_id
                and path.target_id
                == target_id
                and path.status
                == PathStatus.ACTIVE
            ):

                return path

        raise NoAvailablePathError(
            f"No available path from "
            f"{source_id} to {target_id}"
        )

    def available_paths(
        self,
        source_id: str,
        target_id: str,
    ):

        return [
            path
            for path in self.paths.values()
            if (
                path.source_id
                == source_id
                and path.target_id
                == target_id
                and path.status
                == PathStatus.ACTIVE
            )
        ]