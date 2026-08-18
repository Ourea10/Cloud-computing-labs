class CloudManagementError(Exception):
    """Base exception for Chapter 12."""


class ResourceNotFoundError(
    CloudManagementError
):
    pass


class ResourceQuotaExceededError(
    CloudManagementError
):
    pass


class InvalidResourceOperationError(
    CloudManagementError
):
    pass


class SLANotFoundError(
    CloudManagementError
):
    pass


class BillingError(
    CloudManagementError
):
    pass