from enum import Enum


class DeliveryModel(str, Enum):

    IAAS = "iaas"
    PAAS = "paas"
    SAAS = "saas"


class Responsibility(str, Enum):

    CUSTOMER = "customer"
    PROVIDER = "provider"
    SHARED = "shared"


class Layer(str, Enum):

    FACILITY = "facility"
    NETWORK = "network"
    STORAGE = "storage"
    COMPUTE = "compute"
    OPERATING_SYSTEM = "operating_system"
    RUNTIME = "runtime"
    DATABASE = "database"
    APPLICATION = "application"
    DATA = "data"
    IDENTITY = "identity"