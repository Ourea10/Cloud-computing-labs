from experiments.ch07_security.audit import (
    AuditLogger,
)

from experiments.ch07_security.authorization import (
    Principal,
    ResourceOwnership,
    Role,
    can_access,
    can_modify,
)

from experiments.ch07_security.case_study import (
    build_risk_register,
)

from experiments.ch07_security.rate_limiter import (
    RateLimiter,
)

from experiments.ch07_security.threat_catalog import (
    load_threat_catalog,
)


def show_security_properties():
    print("=== Security Properties ===")

    properties = [
        "confidentiality",
        "integrity",
        "availability",
        "authenticity",
    ]

    for property_name in properties:
        print(f"- {property_name}")


def show_threat_catalog():
    print("\n=== Threat Catalog ===")

    threats = load_threat_catalog()

    for threat in threats.values():
        print(
            f"{threat.name}: "
            f"{threat.category.value}"
        )


def show_authorization():
    print("\n=== Authorization ===")

    tenant_a_user = Principal(
        user_id="alice",
        tenant_id="tenant-a",
        role=Role.VIEWER,
    )

    tenant_a_resource = ResourceOwnership(
        resource_id="resource-a",
        tenant_id="tenant-a",
    )

    tenant_b_resource = ResourceOwnership(
        resource_id="resource-b",
        tenant_id="tenant-b",
    )

    print(
        "Tenant A -> Tenant A:",
        can_access(
            tenant_a_user,
            tenant_a_resource,
        ),
    )

    print(
        "Tenant A -> Tenant B:",
        can_access(
            tenant_a_user,
            tenant_b_resource,
        ),
    )

    print(
        "Viewer modify:",
        can_modify(
            tenant_a_user,
            tenant_a_resource,
        ),
    )


def show_rate_limiting():
    print("\n=== Rate Limiting ===")

    limiter = RateLimiter(
        max_requests=3,
        window_seconds=60,
    )

    for attempt in range(1, 6):
        allowed = limiter.allow(
            "login:alice"
        )

        print(
            f"Attempt {attempt}: "
            f"{'allowed' if allowed else 'blocked'}"
        )


def show_audit():
    print("\n=== Audit Logging ===")

    logger = AuditLogger()

    logger.record(
        event_type="authentication",
        actor="alice",
        resource="api",
        action="login",
        outcome="success",
    )

    logger.record(
        event_type="authorization",
        actor="alice",
        resource="resource-b",
        action="read",
        outcome="denied",
        details="Cross-tenant access",
    )

    for event in logger.events:
        print(
            event.timestamp.isoformat(),
            event.event_type,
            event.actor,
            event.action,
            event.outcome,
        )


def show_risk_register():
    print("\n=== Risk Register ===")

    risks = build_risk_register()

    for risk in risks:
        print(
            f"{risk.threat}: "
            f"score={risk.score} "
            f"level={risk.level.value}"
        )


def main():
    show_security_properties()
    show_threat_catalog()
    show_authorization()
    show_rate_limiting()
    show_audit()
    show_risk_register()


if __name__ == "__main__":
    main()