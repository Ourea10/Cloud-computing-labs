# Chapter 13 — Cloud Security Mechanisms

## Objective

This chapter implements security mechanisms around the
cloud management platform from Chapter 12.

The implementation includes:

- Authentication
- Authorization
- RBAC
- Credential Management
- Encryption
- Audit Logging
- Secure API access

---

# Architecture

    Client
      |
      v
    Authentication
      |
      v
    Authorization
      |
      v
    Cloud Management API
      |
      +----------------+
      |                |
      v                v
    Resource         Billing
    Management       Management

---

# Authentication

Authentication answers:

    Who are you?

The implementation:

    username
        |
        v
    password verification
        |
        v
    access token
        |
        v
    authenticated user

Passwords are never stored as plaintext.

PBKDF2-HMAC-SHA256 is used for password hashing.

---

# Authorization

Authorization answers:

    What are you allowed to do?

The project implements RBAC.

Roles:

    admin
    customer
    auditor

Example:

    customer

        resource:read       ALLOWED
        resource:create     ALLOWED
        billing:read        ALLOWED
        security:manage     DENIED

---

# Credential Management

Credentials are not stored as plaintext.

    Secret
       |
       v
    Encryption
       |
       v
    Encrypted value
       |
       v
    Storage

The credential manager stores encrypted credentials
and decrypts them only when explicitly requested.

---

# Encryption

Fernet symmetric encryption is used for the experiment.

The purpose is to demonstrate the mechanism rather than
implement production cryptography.

In a real AWS deployment, encryption keys should be
managed through AWS KMS or another dedicated key-management
system.

---

# Audit Logging

Security-sensitive operations are recorded.

Each audit event contains:

    user
    action
    resource
    timestamp
    success
    message

Example:

    alice
    login
    SUCCESS

or:

    alice
    security:manage
    FAILED

Audit logging allows the system to answer:

    Who performed the operation?
    When?
    On which resource?
    Did it succeed?

---

# Integration with Chapter 12

Chapter 12 provides:

    Resource Management
    Remote Administration
    SLA Management
    Billing

Chapter 13 protects access to those mechanisms.

    Client
       |
       v
    Authentication
       |
       v
    Authorization
       |
       v
    Chapter 12 Cloud Manager

---

# Integration with Chapter 11

Chapter 11 focuses on protecting data.

Chapter 13 focuses on controlling access to cloud
resources and services.

Together:

    Data Security
         +
    Access Security

---

# API

Run:

    uvicorn experiments.ch13_cloud_security_mechanisms.api.app:app --reload

Swagger:

    http://localhost:8000/docs

Endpoints:

    POST /api/v1/auth/login

    GET /api/v1/me

    POST /api/v1/credentials

    GET /api/v1/audit

---

# Example Authentication Flow

    POST /auth/login

        |
        v

    username + password

        |
        v

    AuthenticationService

        |
        v

    AccessToken

        |
        v

    Authorization header

        Authorization: Bearer <token>

---

# AWS Mapping

| This project | AWS concept |
|---|---|
| Authentication | IAM / Cognito |
| Authorization | IAM policies |
| RBAC | IAM roles/policies |
| Credential Management | Secrets Manager |
| Encryption | KMS |
| Audit Logging | CloudTrail |
| API authentication | API Gateway authorizers |
| Application secrets | Secrets Manager |
| Access logs | CloudWatch |

---

# Important Design Principle

Authentication and authorization are separate concerns.

Authentication:

    Who are you?

Authorization:

    What can you do?

A user can be successfully authenticated but still
be denied access to an operation.

---

# Run Demo

    python -m experiments.ch13_cloud_security_mechanisms.demo

---

# Run Tests

    pytest experiments/ch13_cloud_security_mechanisms -v