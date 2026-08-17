# Chapter 9 — Specialized Cloud Mechanisms

## Objective

Chapter 8 created the infrastructure resources.

Chapter 9 adds runtime mechanisms that control,
monitor, distribute, protect, and persist those
resources.

The mechanisms implemented are:

1. Automated Scaling Listener
2. Load Balancer
3. SLA Monitor
4. Pay-Per-Use Monitor
5. Audit Monitor
6. Failover System
7. Resource Cluster
8. Multi-Device Broker
9. State Management Database

---

# Chapter 8 vs Chapter 9

Chapter 8:

    Create infrastructure

Chapter 9:

    Operate infrastructure

Example:

    Chapter 8

        Virtual Server
             |
             v
        Physical Host


    Chapter 9

        Usage
          |
          v
        Scaling
          |
          v
        Virtual Server


---

# 9.1 Automated Scaling Listener

File:

    scaling.py

The listener observes resource metrics and
determines whether a resource group should
scale in or scale out.

The implementation separates:

    Observation
        |
        v
    Scaling Decision
        |
        v
    Infrastructure Action

Example:

    CPU = 85%
    threshold = 70%

    scale-out decision

The listener does not directly contain
infrastructure logic.

---

# 9.2 Load Balancer

File:

    load_balancer.py

The load balancer distributes requests across
healthy backend resources.

The lab uses round-robin selection.

Example:

    Request 1 -> server-1
    Request 2 -> server-2
    Request 3 -> server-3
    Request 4 -> server-1

If a backend becomes unhealthy, it is removed
from request selection.

---

# 9.3 SLA Monitor

Files:

    sla_monitor.py
    sla_agents.py

The SLA monitor evaluates service metrics
against defined objectives.

The implementation separates:

    SLA Monitor Polling Agent
        |
        v
    collect metric

    SLA Monitoring Agent
        |
        v
    evaluate metric

Example:

    Availability target = 99%

    Observation = 99.5%

    Result = PASS

---

# 9.4 Pay-Per-Use Monitor

File:

    pay_per_use.py

The monitor converts resource usage into
charges.

Example:

    5 vCPU-hours
    price = $0.02 / vCPU-hour

    cost = $0.10

The prices used in this repository are
fictional laboratory values.

They are not AWS prices.

---

# 9.5 Audit Monitor

File:

    audit_monitor.py

The audit monitor records operations such as:

    create_server
    delete_server
    attach_storage
    failover
    scale_out

An audit event contains:

    actor
    tenant
    action
    resource
    result
    metadata

This mechanism connects directly to the
security concepts from Chapter 7.

---

# 9.6 Failover System

File:

    failover.py

Two modes are implemented.

## Active-Passive

    Primary
      ACTIVE

    Secondary
      INACTIVE

After failure:

    Primary
      FAILED

    Secondary
      ACTIVE


## Active-Active

    Server A
      ACTIVE

    Server B
      ACTIVE

If A fails:

    Server A
      FAILED

    Server B
      ACTIVE

Active-active allows multiple resources to
serve traffic simultaneously.

---

# 9.7 Resource Cluster

File:

    resource_cluster.py

A resource cluster groups multiple resources
into one logical group.

Example:

    api-cluster

        server-1
        server-2
        server-3
        server-4

The cluster can calculate its health ratio.

Example:

    4 / 4 = 100%

    3 / 4 = 75%

    2 / 4 = 50%

    1 / 4 = 25%

---

# 9.8 Multi-Device Broker

File:

    multi_device_broker.py

The broker allows devices/resources to
communicate through topics.

Example:

    server-001
        |
        | publish
        v
    metrics.cpu
        |
        v
    monitor-001
        |
        | consume

This creates an abstraction between the
producer and consumer.

---

# 9.9 State Management Database

File:

    state_management.py

The state management database persists
resource state outside of the Python process.

Example:

    server-001
    type = virtual_server
    tenant = tenant-a
    state = running

SQLite is used for the local laboratory.

The goal is to demonstrate the mechanism,
not to build a production database.

---

# Integration with Chapter 8

Chapter 9 consumes the mechanisms created
in Chapter 8.

    Cloud Usage Monitor
             |
             v
    Automated Scaling Listener
             |
             v
    Virtual Server


    Virtual Servers
             |
             v
       Load Balancer


    Resource Replication
             |
             v
       Failover System


    Resource Usage
             |
             v
       Pay-Per-Use


    Infrastructure Operations
             |
             v
       Audit Monitor


    Resource State
             |
             v
    State Management DB

---

# Integration with Chapter 7

Chapter 7 introduced:

    Authentication
    Authorization
    Tenant isolation
    Security boundaries

Chapter 9 extends those concepts.

Example:

    Alice
      |
      v
    tenant-a
      |
      v
    server-a

The audit monitor records:

    actor = alice
    tenant = tenant-a

The state database also stores:

    tenant_id = tenant-a

This allows the system to maintain tenant
ownership across runtime mechanisms.

---

# Main Runtime Scenario

The main experiment simulates:

    1. API starts with two servers.

    2. Usage monitor reports high CPU.

    3. Automated Scaling Listener detects
       threshold violation.

    4. A new virtual server is provisioned.

    5. The Load Balancer adds the new server.

    6. One backend becomes unhealthy.

    7. The Load Balancer stops routing traffic
       to that backend.

    8. Failover promotes a secondary resource.

    9. SLA Monitor records availability.

    10. Pay-Per-Use Monitor calculates usage cost.

    11. Audit Monitor records all operations.

    12. State Management Database persists
        resource state.

This is the main Chapter 9 integration scenario.

---

# Run

From repository root:

```bash
python -m experiments.ch09_specialized_mechanisms.demo