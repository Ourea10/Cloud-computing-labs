# Chapter 5 — Cloud-Enabling Technology

## Objective

This chapter implements simplified versions of the
technologies that enable cloud computing.

Topics demonstrated:

- network behavior
- virtualization
- hypervisors
- virtual machines
- service APIs

---

# 1. Network

`network.py` models:

    latency
    bandwidth
    payload size
    transfer time

The purpose is to understand why cloud systems are
affected by network latency and bandwidth.

---

# 2. Virtualization

`virtualization.py` builds on the `ComputeResource`
created in Chapter 1.

The relationship is:

    Physical ComputeResource
             ↓
         Hypervisor
          /       \
        VM-01    VM-02

The hypervisor tracks allocated CPU and memory.

---

# 3. Service APIs

`service_api.py` represents a simplified cloud service
interface.

The provider exposes operations such as:

    create_resource()
    get_resource()

This demonstrates an important cloud principle:

Resources are not manipulated directly by consumers.

Consumers interact through service interfaces.

---

# Run

```bash
python -m experiments.ch05_enabling_technology.demo
```

Run the tests from repository root:

```bash
pytest experiments/ch05_enabling_technology
```
