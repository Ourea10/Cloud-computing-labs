# Chapter 3 — Understanding Cloud Computing

## Objective

This chapter turns cloud-computing concepts into executable
models.

The main concepts demonstrated are:

- workload
- horizontal scaling
- elasticity
- resource utilization
- cloud benefits
- cloud risks

---

## System evolution

Chapter 1:

    ResourcePool

Chapter 2:

    CloudProvider
         ↓
    ResourcePool

Chapter 3:

    Workload
       ↓
    Utilization
       ↓
    AutoScaler
       ↓
    CloudProvider
       ↓
    ResourcePool

---

## Experiment 1 — Workload

`workload.py` models a workload requesting CPU and memory.

The purpose is to distinguish:

    resource capacity

from:

    workload demand

This distinction is necessary for understanding scaling.

---

## Experiment 2 — Scaling

`scaling.py` implements a simplified scaling policy.

If utilization becomes high:

    scale_out

If utilization becomes low:

    scale_in

Otherwise:

    keep

This demonstrates the control logic behind elasticity.

---

## Experiment 3 — Risk

`risk.py` models cloud risks discussed in the chapter.

Examples:

- vendor lock-in
- cost overruns

The goal is to connect technical implementation with
the non-technical risks of cloud adoption.

---

## Run

```bash
python -m experiments.ch03_cloud_computing.demo
```

Run the tests from repository root:

```bash
pytest experiments/ch03_cloud_computing
```
