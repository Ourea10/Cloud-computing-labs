# Chapter 1 — Introduction

## 1. What is this experiment?

This experiment demonstrates the basic idea of cloud
resource pooling.

Instead of assigning one physical machine permanently
to one consumer, a provider maintains a shared pool
of computing resources and dynamically allocates them.

---

## 2. Files

### `resource.py`

Defines the basic computing resource.

A resource contains:

- resource ID
- CPU capacity
- memory capacity
- allocation state

### `resource_pool.py`

Implements the resource pool.

It is responsible for:

- adding resources
- finding an available resource
- allocating resources
- releasing resources

### `test_resource_pool.py`

Tests the resource pool behavior.

It verifies:

- successful allocation
- resource release
- resource exhaustion

### `demo.py`

Runs the experiment interactively.

Unlike the tests, this file is intended to help understand
the lifecycle of a cloud resource.

---

## 3. Run the experiment

From the repository root:

```bash
python experiments/ch01-introduction/demo.py