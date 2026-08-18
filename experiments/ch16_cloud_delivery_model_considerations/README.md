# Chapter 16 — Cloud Delivery Model Considerations

This chapter converts the cloud delivery model concepts
from the book into executable Python code.

The main concepts are:

- Infrastructure as a Service
- Platform as a Service
- Software as a Service
- Provider responsibility
- Customer responsibility
- Workload characteristics
- Delivery model selection
- Cost considerations
- Risk considerations

---

# 1. IaaS

Infrastructure is provided by the cloud provider.

The customer is responsible for higher-level components.

    Customer
       |
       +-- Operating System
       +-- Runtime
       +-- Application
       +-- Data
       |
       v
    Provider
       |
       +-- Compute
       +-- Storage
       +-- Network
       +-- Physical infrastructure

Implementation:

    iaas.py

---

# 2. PaaS

The provider manages infrastructure and platform.

The customer mainly manages:

    Application
    Data

Implementation:

    paas.py

The customer does not need to manually install the
operating system or runtime.

---

# 3. SaaS

The provider delivers a complete application.

The customer consumes the service.

Implementation:

    saas.py

The customer does not deploy or manage the application
infrastructure.

---

# 4. Responsibility Matrix

Implementation:

    responsibility.py

The matrix answers:

    Who manages this layer?

Example:

    IaaS
        Compute       -> Provider
        Storage       -> Provider
        OS            -> Customer
        Runtime       -> Customer
        Application   -> Customer

    PaaS
        Compute       -> Provider
        OS            -> Provider
        Runtime       -> Provider
        Application   -> Customer

    SaaS
        Compute       -> Provider
        OS            -> Provider
        Runtime       -> Provider
        Application   -> Provider

---

# 5. Workload

A workload is represented by:

    workload.py

Each workload defines requirements such as:

    OS control
    Runtime control
    Application control
    Operational complexity
    Scalability requirement
    Budget

---

# 6. Delivery Model Selection

Implementation:

    delivery_model_selector.py

The selector evaluates the workload and recommends:

    IaaS
    PaaS
    SaaS

This demonstrates that delivery model selection should
start from workload requirements rather than simply
choosing a cloud service.

---

# 7. Cost

Implementation:

    cost_model.py

The cost model is intentionally simplified.

It demonstrates the conceptual trade-off:

    IaaS
        More infrastructure responsibility

    PaaS
        More provider-managed infrastructure

    SaaS
        Maximum provider-managed functionality

The numbers are NOT AWS prices.

---

# 8. Risk

Implementation:

    risk_model.py

Different models produce different risks.

IaaS:

    High operational responsibility
    Lower provider dependency

PaaS:

    Lower operational responsibility
    Higher platform dependency

SaaS:

    Very low operational responsibility
    High provider dependency

---

# Integration with Previous Chapters

This chapter must not be treated as an isolated project.

---

## Chapter 13 — Security

Every delivery model still requires security.

For example:

    SaaS
      |
      +-- Identity
      +-- Access control
      +-- Data protection

Chapter 16 uses the security abstraction introduced
in Chapter 13 rather than creating a completely separate
security architecture.

---

## Chapter 14 — Monitoring

Delivery model changes what should be monitored.

IaaS:

    VM
    Disk
    Network
    OS
    Application

PaaS:

    Platform
    Application
    Requests
    Runtime

SaaS:

    Service availability
    Application behavior
    User-facing metrics

The monitoring system from Chapter 14 should therefore
observe the resources introduced here.

---

## Chapter 15 — Specialized Architecture

Chapter 15 introduced:

    Edge
    Fog
    Multipath
    Specialized storage
    Federation
    Metacloud

Chapter 16 determines how these capabilities may be
delivered.

For example:

    Edge workload
        |
        +-- IaaS
        +-- PaaS
        +-- SaaS

The architecture and delivery model are separate decisions.

---

# AWS Mapping

## IaaS

Typical AWS concepts:

    EC2
    EBS
    VPC

The customer manages the operating system and applications.

---

## PaaS

Examples of AWS managed-platform concepts:

    Elastic Beanstalk
    ECS
    Lambda
    RDS

The provider manages progressively more of the
underlying infrastructure.

---

## SaaS

AWS is not itself simply a SaaS provider for every service.

SaaS is a delivery model.

Examples of SaaS-style applications can be built or
consumed on top of cloud infrastructure.

---

# Main Architecture

    Workload
       |
       v
    Requirements
       |
       v
    Delivery Model Selector
       |
       +---------+---------+
       |         |         |
       v         v         v
     IaaS      PaaS      SaaS
       |         |         |
       +---------+---------+
                 |
                 v
          Responsibility
                 |
        +--------+--------+
        |                 |
        v                 v
     Customer          Provider
        |                 |
        +--------+--------+
                 |
                 v
             Monitoring
             Chapter 14
                 |
                 v
              Security
             Chapter 13

---

# Run

    python -m experiments.ch16_cloud_delivery_model_considerations.demo

---

# Tests

    pytest experiments/ch16_cloud_delivery_model_considerations -v

---

# Learning Objective

The important lesson of this chapter is:

    Cloud service selection
            !=
    Architecture selection
            !=
    Delivery model selection

A workload should first be understood in terms of:

    requirements
    control
    responsibility
    cost
    operational complexity
    risk

Only then should an appropriate delivery model be selected.