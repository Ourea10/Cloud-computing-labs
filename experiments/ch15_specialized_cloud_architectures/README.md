# Chapter 15 — Specialized Cloud Architectures

This chapter implements several specialized cloud
architecture patterns described in the book.

The implementation is intentionally local and does not
require AWS.

The purpose is to understand the architecture before
mapping it to real cloud services.

---

# Topics

This chapter covers:

- Direct I/O / LUN access
- Virtual switches
- Multipath resource access
- Physical connections
- Storage maintenance windows
- Edge computing
- Fog computing
- Data abstraction
- Metacloud
- Federated cloud

---

# 1. Direct I/O

Normal architecture:

    Application
        |
        v
      Network
        |
        v
      Storage

Direct I/O:

    Application
        |
        v
    Direct I/O
        |
        v
       LUN
        |
        v
     Storage

The implementation is in:

    direct_io.py

The manager controls which clients can directly access
specific LUNs.

---

# 2. Virtual Switch

Virtual resources can communicate through a software-defined
network switch.

    VM A
      |
      |
    Virtual Switch
      |
      |
    VM B

Implementation:

    virtual_switch.py

---

# 3. Multipath Access

A resource may have multiple paths to another resource.

    Server
      |
      +---- Path A ----+
      |                |
      +---- Path B ----+
                       |
                    Storage

If Path A fails, Path B remains available.

Implementation:

    multipath.py

This demonstrates the basic idea of high availability
through redundant resource paths.

---

# 4. Physical Connection

Some specialized architectures maintain physical resource
connections.

Implementation:

    physical_connection.py

The project models the connection as a resource path whose
connection type is:

    physical

---

# 5. Storage Maintenance

Storage resources may need maintenance windows.

Example:

    02:00 -> 03:00

During this period the resource may be unavailable or
restricted.

Implementation:

    maintenance.py

---

# 6. Edge Computing

Instead of sending all data to the cloud:

    Device
       |
       v
    Edge Node
       |
       v
      Cloud

The edge node processes data close to where it is generated.

Implementation:

    edge_node.py

---

# 7. Fog Computing

Fog introduces an intermediate layer between edge devices
and cloud infrastructure.

    Device
       |
       v
    Edge
       |
       v
     Fog
       |
       v
     Cloud

Implementation:

    fog_node.py

The example aggregates measurements from multiple edge
sources before sending the result upstream.

---

# 8. Data Abstraction

Applications should not need to know whether data comes from:

    Local
    Edge
    Cloud

Instead they depend on:

    DataProvider

Implementation:

    data_abstraction.py

This demonstrates abstraction and loose coupling.

---

# 9. Metacloud

A metacloud abstraction sits above multiple cloud providers.

    Application
         |
         v
      MetaCloud
      /   |   \
     /    |    \
   AWS  Azure  GCP

Implementation:

    metacloud.py

The application can interact with the abstraction instead
of directly coupling itself to one provider.

---

# 10. Federated Cloud

Federated cloud allows independently managed cloud providers
to participate in a common federation.

    AWS
      \
       \
     Federation
       /
      /
   Azure

Implementation:

    federated_cloud.py

The federation manager keeps track of providers and their
resources.

---

# Integration with Previous Chapters

## Chapter 12

Chapter 12 introduced cloud resources.

Chapter 15 extends the concept of resources into:

    Storage
    Network paths
    Physical connections
    Edge nodes
    Fog nodes
    Federated resources

---

## Chapter 13

Chapter 13 introduced:

    Authentication
    Authorization
    RBAC
    Security

Chapter 15 does not create another security system.

Specialized cloud operations should be protected by the
security mechanism from Chapter 13.

---

## Chapter 14

Chapter 14 introduced:

    Metrics
    Health
    Alerts

Chapter 15 introduces architectures that can generate
additional monitoring events.

Example:

    Path A fails
        |
        v
    Multipath failover
        |
        v
    Monitoring
        |
        v
      Alert

Therefore Chapter 15 is connected to Chapter 14 as well.

---

# Architecture

    Client
      |
      v
    Security
      |
      v
    Specialized Cloud Service
      |
      +------------------+
      |                  |
      v                  v
    Storage            Network
      |                  |
      +--------+---------+
               |
               v
        Edge / Fog Layer
               |
               v
         Meta / Federation
               |
               v
             Cloud

---

# AWS Mapping

| Local concept | AWS-related concept |
|---|---|
| StorageResource | EBS / EFS / S3 |
| Direct I/O | EBS / EC2 storage access patterns |
| VirtualSwitch | VPC / ENI / virtual networking |
| Multipath | redundant network/storage paths |
| PhysicalConnection | Direct Connect / physical infrastructure |
| MaintenanceWindow | AWS maintenance events / scheduled maintenance |
| EdgeNode | AWS IoT Greengrass / edge infrastructure |
| FogNode | distributed edge architecture |
| DataProvider | cloud abstraction layer |
| MetaCloud | multi-cloud abstraction |
| Federation | multi-cloud / federated architecture |

The local implementations are conceptual simulations.
They are not intended to reproduce the internal implementation
of AWS services.

---

# Run

    python -m experiments.ch15_specialized_cloud_architectures.demo

---

# Test

    pytest experiments/ch15_specialized_cloud_architectures -v

---

# Main Learning Objective

The main objective of this chapter is understanding that
cloud architecture does not always mean:

    Application -> Cloud -> Resource

Specialized workloads may require:

    Direct access
    Redundant paths
    Virtual networking
    Physical connections
    Edge processing
    Fog processing
    Multi-cloud abstraction
    Federation

These are architectural decisions rather than simply
individual cloud services.