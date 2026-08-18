from experiments.ch14_cloud_monitoring.models import (
    AlertRule,
    AlertSeverity,
    MetricType,
)

from experiments.ch14_cloud_monitoring.monitoring_service import (
    MonitoringService,
)


def main():

    monitoring = MonitoringService()

    # --------------------------------
    # 1. Register monitoring rules
    # --------------------------------

    monitoring.alert_engine.register_rule(
        AlertRule(
            rule_id="cpu-warning",
            resource_id=None,
            metric_type=MetricType.CPU,
            operator=">=",
            threshold=80,
            severity=AlertSeverity.WARNING,
            message=(
                "CPU usage exceeded "
                "warning threshold"
            ),
        )
    )

    monitoring.alert_engine.register_rule(
        AlertRule(
            rule_id="memory-warning",
            resource_id=None,
            metric_type=MetricType.MEMORY,
            operator=">=",
            threshold=80,
            severity=AlertSeverity.WARNING,
            message=(
                "Memory usage exceeded "
                "warning threshold"
            ),
        )
    )

    # --------------------------------
    # 2. Collect metrics
    # --------------------------------

    resource_id = "vm-001"

    metrics, alerts = (
        monitoring.collect(
            resource_id
        )
    )

    print("=== METRICS ===")

    for metric in metrics:

        print(
            metric.metric_type.value,
            metric.value,
            metric.unit,
        )

    # --------------------------------
    # 3. Alerts
    # --------------------------------

    print("\n=== ALERTS ===")

    if not alerts:

        print("No alerts")

    for alert in alerts:

        print(
            alert.severity.value,
            alert.message,
            f"value={alert.value}",
            f"threshold={alert.threshold}",
        )

    # --------------------------------
    # 4. Health
    # --------------------------------

    print("\n=== HEALTH ===")

    health = monitoring.health(
        resource_id
    )

    print(
        health.status.value
    )

    for check, result in (
        health.checks.items()
    ):

        print(
            check,
            "PASS" if result else "FAIL",
        )


if __name__ == "__main__":
    main()