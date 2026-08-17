# Chapter 4 — Fundamental Concepts and Models

## Objective

This chapter turns the conceptual cloud model into a
multi-tenant environment.

---

# System evolution

Chapter 1:

    ResourcePool

Chapter 2:

    CloudProvider
        ↓
    ResourcePool

Chapter 3:

    Workload
        ↓
    Scaling Policy

Chapter 4:

    CloudEnvironment
        ↓
    Tenants
        ↓
    ResourcePool
        ↓
    ComputeResources

---

# Roles

`roles.py` represents cloud participants such as:

- provider
- consumer
- broker
- service owner
- resource administrator

---

# Multitenancy

`tenant.py` defines a tenant.

`cloud_environment.py` associates resources with tenants.

Example:

    Cloud Environment
       │
       ├── Tenant A
       │     ├── server-01
       │     └── server-02
       │
       └── Tenant B
             └── server-03

The important concept is logical isolation.

Tenant A must not be able to release Tenant B's resources.

---

# Delivery models

`delivery_models.py` represents:

- IaaS
- PaaS
- SaaS

These are models of how responsibility is divided between
the provider and consumer.

---

# Deployment models

`deployment_models.yaml` contains:

- public cloud
- private cloud
- hybrid cloud
- multicloud

These describe how cloud infrastructure is organized and
consumed.

---

# Run

```bash
python -m experiments.ch04_concepts_models.demo
```

Run the tests from repository root:

```bash
pytest experiments/ch04_concepts_models
```
