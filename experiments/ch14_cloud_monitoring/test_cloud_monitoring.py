from datetime import datetime, timezone

import pytest

from .alert_engine import (
    AlertEngine,
)

from .health_checker import (
    HealthChecker,
)

from .models import (
    AlertRule,
    AlertSeverity,
    Metric,
    MetricType,
)

from .monitoring_service import (
    MonitoringService,
)


def test_metric_collection():

    monitoring = MonitoringService()

    metrics, alerts = (
        monitoring.collect(
            "vm-001"
        )
    )

    assert len(metrics) == 4

    assert all(
        metric.resource_id
        == "vm-001"
        for metric in metrics
    )


def test_metric_store():

    monitoring = MonitoringService()

    monitoring.collect(
        "vm-001"
    )

    metrics = (
        monitoring.store
        .get_resource_metrics(
            "vm-001"
        )
    )

    assert len(metrics) == 4


def test_alert_rule():

    engine = AlertEngine()

    engine.register_rule(
        AlertRule(
            rule_id="cpu-warning",
            resource_id=None,
            metric_type=MetricType.CPU,
            operator=">=",
            threshold=80,
            severity=AlertSeverity.WARNING,
            message="High CPU",
        )
    )

    metric = Metric(
        metric_id="metric-001",
        resource_id="vm-001",
        metric_type=MetricType.CPU,
        value=90,
        unit="percent",
        timestamp=datetime.now(
            timezone.utc
        ),
    )

    alerts = engine.evaluate(
        metric
    )

    assert len(alerts) == 1

    assert alerts[0].severity == (
        AlertSeverity.WARNING
    )


def test_no_alert_when_below_threshold():

    engine = AlertEngine()

    engine.register_rule(
        AlertRule(
            rule_id="cpu-warning",
            resource_id=None,
            metric_type=MetricType.CPU,
            operator=">=",
            threshold=80,
            severity=AlertSeverity.WARNING,
            message="High CPU",
        )
    )

    metric = Metric(
        metric_id="metric-001",
        resource_id="vm-001",
        metric_type=MetricType.CPU,
        value=50,
        unit="percent",
        timestamp=datetime.now(
            timezone.utc
        ),
    )

    alerts = engine.evaluate(
        metric
    )

    assert alerts == []


def test_health_status():

    monitoring = MonitoringService()

    monitoring.collect(
        "vm-001"
    )

    health = monitoring.health(
        "vm-001"
    )

    assert health.resource_id == (
        "vm-001"
    )

    assert health.status is not None


def test_alert_resource_specific_rule():

    engine = AlertEngine()

    engine.register_rule(
        AlertRule(
            rule_id="vm-001-cpu",
            resource_id="vm-001",
            metric_type=MetricType.CPU,
            operator=">",
            threshold=70,
            severity=AlertSeverity.CRITICAL,
            message="VM 001 CPU critical",
        )
    )

    metric = Metric(
        metric_id="metric-001",
        resource_id="vm-002",
        metric_type=MetricType.CPU,
        value=90,
        unit="percent",
        timestamp=datetime.now(
            timezone.utc
        ),
    )

    alerts = engine.evaluate(
        metric
    )

    assert alerts == []