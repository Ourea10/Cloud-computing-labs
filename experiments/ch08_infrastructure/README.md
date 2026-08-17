# Chapter 8 — Cloud Infrastructure Mechanisms

## Objective

Chapter 8 converts cloud infrastructure concepts into
executable Python mechanisms.

The implementation models:

1. Logical Network Perimeter
2. Virtual Server
3. Hypervisor
4. Cloud Storage Device
5. Cloud Usage Monitor
6. Resource Replication
7. Ready-Made Environment
8. Container

The mechanisms are then integrated into the Cloud Lab API.

---

# Architecture

    Client
      |
      v
    FastAPI
      |
      +-------------------+
      |                   |
      v                   v
    Security        Infrastructure
      |                   |
      |          +--------+--------+
      |          |        |        |
      |         VM     Storage  Container
      |          |
      |      Hypervisor
      |          |
      |      Physical Host
      |
      +---- Tenant Isolation

---

# 8.1 Logical Network Perimeter

Implemented in:

    network_perimeter.py

The mechanism defines a logical boundary around
cloud resources.

Example:

    Internet -> HTTPS -> ALLOW
    Internet -> SSH   -> DENY
    Internal -> SSH   -> ALLOW

This concept connects directly with Chapter 7
security boundaries.

---

# 8.2 Virtual Server

Implemented in:

    virtual_server.py

A virtual server models a VM provisioned from
shared physical resources.

Each server has:

- CPU
- memory
- image
- private IP
- tenant
- lifecycle state

Lifecycle:

    PROVISIONING
         |
         v
      RUNNING
         |
         v
      STOPPED

---

# 8.3 Hypervisor

Implemented in:

    hypervisor.py

The hypervisor manages virtual servers on a
physical host.

Example:

    Physical Host
    CPU = 8
    RAM = 16 GB

            |
            v

    VM A = 2 CPU / 4 GB
    VM B = 4 CPU / 8 GB

The hypervisor prevents allocation beyond
physical capacity.

This demonstrates resource virtualization.

---

# 8.4 Cloud Storage Device

Implemented in:

    storage.py

Storage volumes are separate infrastructure
resources that can be attached to virtual servers.

Example:

    VM
     |
     +---- Block Volume

The model supports:

- volume creation
- attachment
- detachment

---

# 8.5 Cloud Usage Monitor

Implemented in:

    usage_monitor.py

The monitor records:

- CPU usage
- memory usage
- network usage
- storage usage

This mechanism becomes a foundation for
future chapters.

Chapter 9 will use usage information for
specialized mechanisms such as scaling.

Chapter 17 will use usage information for
cost calculations.

Chapter 18 will use usage information for
service quality and SLA calculations.

---

# 8.6 Resource Replication

Implemented in:

    replication.py

Replication creates another instance of a
resource.

Important:

A replica does not reuse the source network
identity.

Example:

    Source
    server-001
    10.0.0.1

        |
        v

    Replica
    server-002
    new network identity

Replication prepares the system for future
redundancy and failover architectures.

---

# 8.7 Ready-Made Environment

Implemented in:

    ready_made_environment.py

A ready-made environment is a preconfigured
environment template.

Example:

    FastAPI Template
        |
        +-- Python
        +-- FastAPI
        +-- Uvicorn
        +-- Configuration

The template can be provisioned repeatedly.

This is conceptually related to:

- VM images
- AMIs
- container images
- preconfigured environments

---

# 8.8 Container

Implemented in:

    container.py

Containers are treated as cloud infrastructure
resources.

Each container has:

- image
- CPU limit
- memory limit
- tenant
- server
- lifecycle state

Chapter 6 focused on how containers work.

Chapter 8 focuses on how containers become
infrastructure mechanisms.

---

# Integration with Chapter 7

Chapter 7 introduced:

    Authentication
    Authorization
    Tenant Isolation

Chapter 8 applies those concepts to infrastructure.

Example:

    Alice
      |
      v
    tenant-a
      |
      v
    create server
      |
      v
    server belongs to tenant-a

The API never creates infrastructure without
an authenticated identity.

---

# Integration with previous chapters

Chapter 1:

    Resource Pool

Chapter 2:

    Cloud Provider / Consumer

Chapter 3:

    Cloud characteristics

Chapter 4:

    Multitenancy

Chapter 5:

    Network + virtualization + service API

Chapter 6:

    Containerization

Chapter 7:

    Security

Chapter 8:

    Infrastructure mechanisms

The repository is intentionally cumulative.

---

# Run the experiments

From repository root:

```bash
python -m experiments.ch08_infrastructure.demo

# Chapter 8 → AWS Mapping

This chapter implements cloud infrastructure mechanisms
locally in Python before mapping them to AWS.

| Cloud Mechanism | Local Implementation | AWS Equivalent |
|---|---|---|
| Logical Network Perimeter | LogicalNetworkPerimeter | VPC / Security Groups / NACL |
| Virtual Server | VirtualServer | EC2 |
| Hypervisor | Hypervisor | AWS virtualization layer |
| Cloud Storage Device | StorageVolume | EBS / S3 / EFS |
| Cloud Usage Monitor | CloudUsageMonitor | CloudWatch |
| Resource Replication | ResourceReplicator | AMI / Snapshot / replication mechanisms |
| Ready-Made Environment | EnvironmentTemplate | AMI / container image |
| Container | ContainerInstance | ECS / Fargate |

Important:

The local implementation is a conceptual model.

It is not intended to reproduce the internal
implementation of AWS services.