class SecurityError(Exception):
    """Base security exception."""


class AuthenticationError(SecurityError):
    pass


class AuthorizationError(SecurityError):
    pass


class InvalidTokenError(AuthenticationError):
    pass


class ExpiredTokenError(AuthenticationError):
    pass


class CredentialNotFoundError(SecurityError):
    pass


class EncryptionError(SecurityError):
    pass