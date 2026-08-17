from dataclasses import dataclass, field
from enum import Enum


class ServerState(str, Enum):
    PROVISIONING = "provisioning"
    RUNNING = "running"
    STOPPED = "stopped"
    FAILED = "failed"


class StorageType(str, Enum):
    BLOCK = "block"
    OBJECT = "object"
    FILE = "file"


class NetworkProtocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"


@dataclass(frozen=True)
class NetworkRule:
    protocol: NetworkProtocol
    port: int
    source: str
    action: str


@dataclass
class VirtualServer:
    server_id: str
    tenant_id: str

    cpu_cores: int
    memory_mb: int

    image: str

    state: ServerState = ServerState.PROVISIONING

    private_ip: str | None = None
    public_ip: str | None = None


@dataclass
class StorageVolume:
    volume_id: str
    tenant_id: str

    storage_type: StorageType
    size_gb: int

    attached_server_id: str | None = None


@dataclass
class ContainerInstance:
    container_id: str
    tenant_id: str

    image: str

    cpu_limit: float
    memory_limit_mb: int

    server_id: str

    running: bool = False


@dataclass
class ResourceUsage:
    resource_id: str
    cpu_percent: float
    memory_mb: int
    network_bytes: int
    storage_bytes: int


@dataclass
class InfrastructureEnvironment:
    name: str

    servers: dict[str, VirtualServer] = field(
        default_factory=dict
    )

    volumes: dict[str, StorageVolume] = field(
        default_factory=dict
    )

    containers: dict[str, ContainerInstance] = field(
        default_factory=dict
    )