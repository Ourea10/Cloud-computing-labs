from experiments.ch07_security.security_models import (
    SecurityPolicy,
)


POLICIES = [
    SecurityPolicy(
        name="Authentication Required",
        statement=(
            "Every protected API endpoint must require "
            "an authenticated identity."
        ),
        enforcement="API authentication dependency",
    ),
    SecurityPolicy(
        name="Tenant Isolation",
        statement=(
            "A tenant may access only resources belonging "
            "to that tenant unless explicitly granted "
            "administrative permission."
        ),
        enforcement="Authorization layer",
    ),
    SecurityPolicy(
        name="Rate Limit Authentication",
        statement=(
            "Repeated authentication failures must be "
            "rate limited."
        ),
        enforcement="Rate limiter",
    ),
    SecurityPolicy(
        name="Security Audit",
        statement=(
            "Authentication and authorization failures "
            "must be recorded."
        ),
        enforcement="Audit logger",
    ),
]