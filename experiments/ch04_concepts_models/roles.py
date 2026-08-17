from enum import Enum


class CloudRole(str, Enum):
    PROVIDER = "cloud_provider"
    CONSUMER = "cloud_consumer"
    BROKER = "cloud_broker"
    SERVICE_OWNER = "cloud_service_owner"
    RESOURCE_ADMIN = "cloud_resource_admin"