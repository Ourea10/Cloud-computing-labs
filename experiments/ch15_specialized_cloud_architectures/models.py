from dataclasses import dataclass, field
from enum import Enum


class ResourceType(str, Enum):
    VM = "vm"
    STORAGE = "storage"
    EDGE_NODE = "edge_node"
    FOG_NODE = "fog_node"


class ConnectionType(str, Enum):
    NETWORK = "network"
    PHYSICAL = "physical"
    DIRECT_IO = "direct_io"


class PathStatus(str, Enum):
    ACTIVE = "active"
    FAILED = "failed"
    MAINTENANCE = "maintenance"


class NodeType(str, Enum):
    EDGE = "edge"
    FOG = "fog"
    CLOUD = "cloud"


class ProviderStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


@dataclass
class StorageResource:
    storage_id: str
    name: str
    capacity_gb: int
    used_gb: int
    lun_id: str
    physical: bool = False


@dataclass
class DirectIOAccess:
    resource_id: str
    lun_id: str
    client_id: str
    enabled: bool


@dataclass
class VirtualSwitch:
    switch_id: str
    name: str
    connected_resources: list[str] = field(
        default_factory=list
    )


@dataclass
class ConnectionPath:
    path_id: str
    source_id: str
    target_id: str
    connection_type: ConnectionType
    status: PathStatus


@dataclass
class EdgeNode:
    node_id: str
    name: str
    location: str
    capabilities: list[str]
    connected_devices: list[str] = field(
        default_factory=list
    )


@dataclass
class FogNode:
    node_id: str
    name: str
    region: str
    edge_nodes: list[str] = field(
        default_factory=list
    )


@dataclass
class CloudProvider:
    provider_id: str
    name: str
    region: str
    services: list[str]
    status: ProviderStatus


@dataclass
class FederatedResource:
    resource_id: str
    provider_id: str
    resource_type: ResourceType
    location: str