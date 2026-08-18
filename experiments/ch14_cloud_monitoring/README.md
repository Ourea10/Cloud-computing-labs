# Chapter 14 — Cloud Monitoring

## Objective

This chapter adds monitoring capabilities to the cloud
management platform.

The implementation covers:

- Metric collection
- Metric storage
- Resource health checking
- Alert rules
- Alert evaluation
- Monitoring API
- Security integration

---

# Why Monitoring?

A cloud management platform needs to know not only whether
a resource exists, but also whether the resource is operating
correctly.

Example:

    Resource:
        vm-001

    Metrics:

        CPU       87%
        Memory    91%
        Network   300 MB/s

Monitoring converts these measurements into information
about system health.

---

# Architecture

    Client
      |
      v
    Authentication
      |
      v
    Authorization
      |
      v
    Cloud Management
      |
      v
    Monitoring Service
      |
      +------------------+
      |                  |
      v                  v
    Metrics            Health
      |
      v
    Alert Engine
      |
      v
    Alerts

---

# Metric Collection

MetricCollector simulates the collection of:

    CPU
    Memory
    Network In
    Network Out

The collector generates metrics locally.

This allows the monitoring system to be developed without
requiring AWS.

---

# Metric Storage

MetricStore keeps historical measurements.

Each metric contains:

    resource_id
    metric_type
    value
    unit
    timestamp

The timestamp is important because monitoring data is
time-series data.

---

# Health Checking

HealthChecker evaluates the latest metrics.

Example:

    CPU < 80%
    Memory < 80%

        => HEALTHY

    CPU >= 80%

        => WARNING

    CPU >= 95%

        => CRITICAL

---

# Alerting

AlertEngine evaluates metrics against alert rules.

Example:

    IF CPU >= 80
    THEN WARNING

or:

    IF CPU >= 95
    THEN CRITICAL

This separates:

    measurement

from:

    decision

---

# Security Integration

Chapter 14 reuses the security mechanisms from Chapter 13.

Monitoring operations require permissions.

Example:

    monitoring:read
    monitoring:manage
    monitoring:configure

A customer can read monitoring information but cannot
change monitoring configuration.

---

# Integration with Chapter 12

Chapter 12 introduced cloud resources.

Chapter 14 monitors those resources.

    Chapter 12

    Resource
        |
        v
    Resource Manager


    Chapter 14

    Resource
        |
        v
    Monitoring
        |
        +-- Metrics
        +-- Health
        +-- Alerts

---

# Integration with Chapter 13

Chapter 13 provides:

    Authentication
    Authorization
    RBAC
    Audit

Chapter 14 reuses those mechanisms instead of implementing
a second authentication system.

---

# API

Run:

    uvicorn experiments.ch14_cloud_monitoring.api.app:app --reload

Swagger:

    http://localhost:8000/docs

Endpoints:

    POST /api/v1/resources/{resource_id}/metrics

    GET /api/v1/resources/{resource_id}/metrics

    GET /api/v1/resources/{resource_id}/health

    GET /api/v1/alerts

---

# Example

Collect metrics:

    POST /api/v1/resources/vm-001/metrics

Possible response:

    {
        "resource_id": "vm-001",
        "metrics": [
            {
                "metric_type": "cpu",
                "value": 87.2,
                "unit": "percent"
            }
        ],
        "alerts": [
            {
                "severity": "warning",
                "message": "CPU usage exceeded warning threshold"
            }
        ]
    }

---

# AWS Mapping

| Local implementation | AWS |
|---|---|
| MetricCollector | CloudWatch metrics |
| MetricStore | CloudWatch / time-series storage |
| AlertEngine | CloudWatch Alarms |
| HealthChecker | CloudWatch + application health checks |
| Monitoring API | API Gateway |
| Audit | CloudTrail / CloudWatch Logs |
| Security | IAM / Cognito |
| Application runtime | Lambda / ECS |

---

# Why This Is Useful

The project is intentionally designed so that the monitoring
logic does not depend directly on AWS.

The architecture is:

    Application
        |
        v
    MonitoringService
        |
        v
    MetricCollector

The collector can later be replaced with:

    AWSCloudWatchMetricCollector

without rewriting the alerting and health-checking logic.

This demonstrates separation between application logic
and cloud infrastructure.

---

# Run Demo

    python -m experiments.ch14_cloud_monitoring.demo

---

# Run Tests

    pytest experiments/ch14_cloud_monitoring -v