# Chapter 10 — Cloud Security and Cybersecurity Access-Oriented Mechanisms

## Objective

Chapter 10 adds security mechanisms that protect the cloud
infrastructure and runtime mechanisms implemented in previous chapters.

The main idea is:

    Chapter 8
        Infrastructure
             |
             v
    Chapter 9
        Runtime mechanisms
             |
             v
    Chapter 10
        Security mechanisms

---

## Mechanisms implemented

1. Encryption
2. Hashing
3. Digital Signature
4. Cloud-Based Security Group
5. PKI
6. SSO
7. Hardened Virtual Server Image
8. Firewall
9. VPN
10. Biometric Scanner
11. MFA
12. IAM
13. Intrusion Detection System
14. Penetration Testing Tool
15. User Behavior Analytics
16. Third-Party Software Update Utility
17. Network Intrusion Monitor
18. Authentication Log Monitor
19. VPN Monitor

---

# Encryption

File:

    encryption.py

Demonstrates symmetric encryption.

Concept:

    plaintext
        |
        v
    encryption
        |
        v
    ciphertext

The laboratory uses Fernet from the Python cryptography
library rather than implementing cryptographic algorithms manually.

---

# Hashing

File:

    hashing.py

Hashing is one-way.

    password
        |
        v
    SHA-256
        |
        v
    digest

Unlike encryption, a hash is not decrypted.

---

# Digital Signature

File:

    digital_signature.py

Digital signatures demonstrate:

    integrity
    authenticity

A signature created using a private key can be verified
using the corresponding public key.

---

# Security Groups

File:

    security_group.py

The security group controls access to resources.

Example:

    TCP 443
        ALLOW

    TCP 22 from Internet
        DENY

This mechanism is conceptually similar to AWS Security Groups.

---

# IAM

File:

    iam.py

IAM separates:

    User
      |
      v
    Role
      |
      v
    Permission

Example:

    developer
        |
        +-- server:read
        +-- server:start

The developer cannot automatically perform:

    server:delete

---

# MFA

File:

    mfa.py

MFA introduces a second authentication factor.

    Password
        +
    MFA code
        |
        v
    Authentication

---

# SSO

File:

    sso.py

SSO allows a user to establish one authenticated session
and reuse that session across services.

---

# Firewall

File:

    firewall.py

Firewall rules operate at the network traffic layer.

Security Group and Firewall are deliberately implemented
as separate mechanisms.

---

# VPN

File:

    vpn.py

The VPN mechanism creates a logical tunnel between a client
and a cloud gateway.

The laboratory implementation does not create a real
network tunnel.

It models the state and lifecycle of the mechanism.

---

# Hardened Virtual Server Image

File:

    hardened_image.py

A hardened image starts from a base image and applies
security configuration before a virtual server is created.

Example:

    base image
        |
        +-- disable telnet
        +-- disable ftp
        +-- install security patches
        +-- expose only required ports
        |
        v
    hardened image

---

# Intrusion Detection

File:

    intrusion_detection.py

The IDS analyzes security events and generates alerts.

Example:

    12 failed authentication attempts
        |
        v
    HIGH severity alert

---

# Penetration Testing

File:

    penetration_testing.py

The lab performs safe configuration analysis.

It detects dangerous exposed services such as:

    Telnet
    FTP

The implementation intentionally does not perform
real offensive network attacks.

---

# User Behavior Analytics

File:

    uba.py

UBA detects abnormal user behavior.

Example:

    normal user:
        2 failed logins

    suspicious user:
        15 failed logins

The second behavior can trigger an anomaly.

---

# Monitoring

The following mechanisms monitor security state:

    network_intrusion_monitor.py
    authentication_log_monitor.py
    vpn_monitor.py

These mechanisms demonstrate that security is not only
about prevention.

Cloud security also requires:

    prevention
    detection
    monitoring
    response

---

# Main Security Flow

The main conceptual flow is:

    User
      |
      v
    SSO
      |
      v
    MFA
      |
      v
    IAM
      |
      v
    Security Group
      |
      v
    Firewall
      |
      v
    VPN
      |
      v
    Cloud Resource

---

# Relationship with previous chapters

Chapter 7:

    Security concepts
    Authentication
    Authorization
    Tenant isolation

Chapter 8:

    Virtual Server
    Container
    Storage
    Network

Chapter 9:

    Scaling
    Load Balancing
    Failover
    Monitoring
    State Management

Chapter 10:

    Encryption
    IAM
    MFA
    Security Groups
    Firewall
    VPN
    IDS
    Security Monitoring

Therefore Chapter 10 is not an isolated security demo.

It protects the infrastructure and runtime mechanisms
created by previous chapters.

---

# AWS Mapping

| Laboratory mechanism | AWS concept |
|---|---|
| IAM | AWS IAM |
| Security Group | EC2 Security Group |
| Firewall | AWS Network Firewall / host firewall |
| Encryption | KMS / application encryption |
| Hashing | application-level hashing |
| Digital Signature | AWS KMS / certificate-based signing |
| PKI | AWS Private CA |
| SSO | IAM Identity Center |
| MFA | IAM MFA |
| VPN | AWS Site-to-Site VPN / Client VPN |
| IDS | Amazon GuardDuty / IDS concepts |
| Monitoring | CloudWatch / security monitoring |
| Audit | CloudTrail |

The laboratory does not attempt to reproduce AWS internally.

The objective is to understand the mechanisms behind cloud
security services.

---

# Run

From repository root:

    python -m experiments.ch10_security_mechanisms.demo

Run tests:

    pytest experiments/ch10_security_mechanisms -v