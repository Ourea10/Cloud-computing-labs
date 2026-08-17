# Chapter 2 — Case Study Background

## Objective

This chapter applies the resource-pooling mechanism from
Chapter 1 to cloud computing case studies.

The three cases are:

- ATN
- DTGOV
- Innovartus Technologies Inc.

---

## Relationship with Chapter 1

Chapter 1 implemented:

    ComputeResource
          ↓
    ResourcePool
          ↓
    allocate()
          ↓
    release()

Chapter 2 builds a simplified cloud provider on top of it:

    CloudProvider
          ↓
    ResourcePool
          ↓
    ComputeResource

This is the first example of reusing a previous chapter
instead of creating an isolated implementation.

---

## Files

### `cases.json`

Contains the workload requirements used by the experiments.

### `case_model.py`

Defines the domain models:

- ResourceRequirement
- CloudCase

### `case_loader.py`

Loads case-study data from `cases.json`.

### `cloud_provider.py`

Builds a cloud-provider abstraction on top of the
Chapter 1 resource pool.

### `demo.py`

Runs the case-study provisioning experiment.

### `test_case_studies.py`

Verifies resource provisioning and release.

---

## Run

From repository root:

```bash
python -m experiments.ch02_case_studies.demo
```

Run the tests from repository root:

```bash
pytest experiments/ch02_case_studies
```
