from .models import VirtualSwitch


class VirtualSwitchManager:

    def __init__(self):

        self.switches: dict[
            str,
            VirtualSwitch,
        ] = {}

    def create(
        self,
        switch_id: str,
        name: str,
    ):

        switch = VirtualSwitch(
            switch_id=switch_id,
            name=name,
        )

        self.switches[
            switch_id
        ] = switch

        return switch

    def connect(
        self,
        switch_id: str,
        resource_id: str,
    ):

        switch = self.switches[
            switch_id
        ]

        if (
            resource_id
            not in switch.connected_resources
        ):

            switch.connected_resources.append(
                resource_id
            )

    def disconnect(
        self,
        switch_id: str,
        resource_id: str,
    ):

        switch = self.switches[
            switch_id
        ]

        if (
            resource_id
            in switch.connected_resources
        ):

            switch.connected_resources.remove(
                resource_id
            )

    def resources(
        self,
        switch_id: str,
    ):

        return self.switches[
            switch_id
        ].connected_resources