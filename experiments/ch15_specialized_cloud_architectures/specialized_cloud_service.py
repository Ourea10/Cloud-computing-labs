from .direct_io import (
    DirectIOManager,
)

from .edge_node import (
    EdgeNodeManager,
)

from .federated_cloud import (
    FederationManager,
)

from .fog_node import (
    FogNodeManager,
)

from .maintenance import (
    MaintenanceManager,
)

from .metacloud import (
    MetaCloud,
)

from .multipath import (
    MultipathManager,
)

from .physical_connection import (
    PhysicalConnectionManager,
)

from .storage import (
    StorageManager,
)

from .virtual_switch import (
    VirtualSwitchManager,
)


class SpecializedCloudService:

    def __init__(self):

        self.storage = (
            StorageManager()
        )

        self.direct_io = (
            DirectIOManager()
        )

        self.virtual_switch = (
            VirtualSwitchManager()
        )

        self.multipath = (
            MultipathManager()
        )

        self.physical = (
            PhysicalConnectionManager()
        )

        self.maintenance = (
            MaintenanceManager()
        )

        self.edge = (
            EdgeNodeManager()
        )

        self.fog = (
            FogNodeManager()
        )

        self.metacloud = (
            MetaCloud()
        )

        self.federation = (
            FederationManager()
        )