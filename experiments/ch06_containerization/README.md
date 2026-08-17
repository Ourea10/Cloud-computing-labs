# Chapter 6 — Understanding Containerization

## Objective

This chapter moves the cloud-lab application from a normal
Python process into containers.

The chapter demonstrates:

- virtualization vs containerization
- containers
- container images
- image layers
- container hosts
- multi-container environments
- container networking

---

# System evolution

Before Chapter 6:

    Python
       ↓
    FastAPI
       ↓
    PostgreSQL

After Chapter 6:

    Docker Host
       │
       ├── API Container
       │       │
       │       └── FastAPI
       │
       └── PostgreSQL Container

---

# Why this chapter uses `apps/api`

The application created during repository setup is now
treated as an actual workload.

We are intentionally NOT creating another toy application.

This demonstrates an important cloud engineering principle:

    application
        ↓
    package
        ↓
    deployable workload

---

# `container_model.py`

Provides a Python simulation of:

- container
- container host
- CPU allocation
- memory allocation
- container lifecycle

This allows the conceptual model to be understood before
using Docker.

---

# `image_model.py`

Models container images as a collection of layers.

Example:

    Python base layer
          ↓
    dependency layer
          ↓
    application layer

The image can then be instantiated as a container.

---

# `docker-compose.yml`

This is the real implementation.

It runs:

- FastAPI
- PostgreSQL

inside separate containers.

The API container communicates with PostgreSQL through
the Docker network.

---

# Run simulation

```bash
python -m experiments.ch06_containerization.demo
```

Run the tests from repository root:

```bash
pytest experiments/ch06_containerization
```

Run the real Docker Compose environment:

```bash
docker compose -f experiments/ch06_containerization/docker-compose.yml up --build
```
