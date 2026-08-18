class ApplicationError(Exception):
    """Base exception for the application."""


class ResourceNotFoundError(ApplicationError):
    """Raised when a requested resource does not exist."""


class UserAlreadyExistsError(ApplicationError):
    """Raised when attempting to create an existing user."""


class AuthenticationError(ApplicationError):
    """Raised when authentication fails."""


class AuthorizationError(ApplicationError):
    """Raised when a user is not allowed to perform an action."""


class InvalidResourceStateError(ApplicationError):
    """Raised when a resource transition is invalid."""


class DeliveryModelError(ApplicationError):
    """Raised when delivery model evaluation fails."""