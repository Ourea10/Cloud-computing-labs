from .models import DirectIOAccess
from .exceptions import ResourceNotFoundError


class DirectIOManager:

    def __init__(self):

        self.access: list[
            DirectIOAccess
        ] = []

    def grant_access(
        self,
        resource_id: str,
        lun_id: str,
        client_id: str,
    ):

        access = DirectIOAccess(
            resource_id=resource_id,
            lun_id=lun_id,
            client_id=client_id,
            enabled=True,
        )

        self.access.append(
            access
        )

        return access

    def revoke_access(
        self,
        client_id: str,
        lun_id: str,
    ):

        found = False

        for access in self.access:

            if (
                access.client_id
                == client_id
                and access.lun_id
                == lun_id
            ):

                access.enabled = False
                found = True

        if not found:

            raise ResourceNotFoundError(
                "Direct I/O access not found"
            )

    def can_access(
        self,
        client_id: str,
        lun_id: str,
    ) -> bool:

        return any(
            access.enabled
            and access.client_id
            == client_id
            and access.lun_id
            == lun_id
            for access in self.access
        )