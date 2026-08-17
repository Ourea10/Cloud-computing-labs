import pytest

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

from experiments.ch07_security.rate_limiter import (
    RateLimiter,
)

from experiments.ch07_security.risk_assessment import (
    RiskLevel,
    assess,
)

from experiments.ch07_security.threat_catalog import (
    load_threat_catalog,
)


def test_threat_catalog_contains_sql_injection():
    threats = load_threat_catalog()

    assert "sql_injection" in threats


def test_tenant_can_access_own_resource():
    principal = Principal(
        user_id="alice",
        tenant_id="tenant-a",
        role=Role.VIEWER,
    )

    resource = ResourceOwnership(
        resource_id="resource-a",
        tenant_id="tenant-a",
    )

    assert can_access(
        principal,
        resource,
    )


def test_tenant_cannot_access_other_tenant():
    principal = Principal(
        user_id="alice",
        tenant_id="tenant-a",
        role=Role.VIEWER,
    )

    resource = ResourceOwnership(
        resource_id="resource-b",
        tenant_id="tenant-b",
    )

    assert not can_access(
        principal,
        resource,
    )


def test_viewer_cannot_modify():
    principal = Principal(
        user_id="alice",
        tenant_id="tenant-a",
        role=Role.VIEWER,
    )

    resource = ResourceOwnership(
        resource_id="resource-a",
        tenant_id="tenant-a",
    )

    assert not can_modify(
        principal,
        resource,
    )


def test_admin_can_access_any_tenant():
    principal = Principal(
        user_id="admin",
        tenant_id="platform",
        role=Role.ADMIN,
    )

    resource = ResourceOwnership(
        resource_id="resource-b",
        tenant_id="tenant-b",
    )

    assert can_access(
        principal,
        resource,
    )


def test_rate_limiter_blocks_after_limit():
    limiter = RateLimiter(
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.allow("client")
    assert limiter.allow("client")
    assert not limiter.allow("client")


def test_risk_is_critical():
    risk = assess(
        threat="sql_injection",
        vulnerability="unsafe query",
        likelihood=4,
        impact=5,
    )

    assert risk.score == 20
    assert risk.level == RiskLevel.CRITICAL


def test_invalid_risk_values_are_rejected():
    with pytest.raises(ValueError):
        assess(
            threat="test",
            vulnerability="test",
            likelihood=6,
            impact=5,
        )


def test_audit_records_denied_event():
    logger = AuditLogger()

    logger.record(
        event_type="authorization",
        actor="alice",
        resource="resource-b",
        action="read",
        outcome="denied",
    )

    denied = logger.failed_events()

    assert len(denied) == 1
    assert denied[0].actor == "alice"