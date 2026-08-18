from dataclasses import dataclass
from datetime import datetime


@dataclass
class MaintenanceWindow:

    resource_id: str
    start: datetime
    end: datetime
    reason: str


class MaintenanceManager:

    def __init__(self):

        self.windows: list[
            MaintenanceWindow
        ] = []

    def schedule(
        self,
        resource_id: str,
        start: datetime,
        end: datetime,
        reason: str,
    ):

        if end <= start:

            raise ValueError(
                "Maintenance end must "
                "be after start"
            )

        window = MaintenanceWindow(
            resource_id=resource_id,
            start=start,
            end=end,
            reason=reason,
        )

        self.windows.append(
            window
        )

        return window

    def is_maintenance(
        self,
        resource_id: str,
        timestamp: datetime,
    ) -> bool:

        return any(
            window.resource_id
            == resource_id
            and window.start
            <= timestamp
            <= window.end
            for window
            in self.windows
        )