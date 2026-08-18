class SpecializedCloudError(Exception):
    """Base exception."""


class ResourceNotFoundError(
    SpecializedCloudError
):
    pass


class ConnectionError(
    SpecializedCloudError
):
    pass


class NoAvailablePathError(
    SpecializedCloudError
):
    pass


class MaintenanceError(
    SpecializedCloudError
):
    pass


class ProviderUnavailableError(
    SpecializedCloudError
):
    pass