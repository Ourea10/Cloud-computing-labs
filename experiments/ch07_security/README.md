# Chapter 7 — Understanding Cloud Security and Cybersecurity

## Objective

This chapter converts cloud security concepts into
executable security models and applies them to the
Cloud Lab API.

The chapter is based on:

- security properties
- security controls
- security policies
- threats
- vulnerabilities
- exploits
- threat agents
- attack vectors
- risk management
- cloud-specific threats

---

# System before Chapter 7

Before security was introduced:

    Cloud Environment
          |
          +-- Tenant A
          +-- Tenant B
          |
          +-- Resource Pool
          |
          +-- Virtualization
          |
          +-- Containers
                 |
                 +-- FastAPI
                 +-- PostgreSQL

Chapter 7 adds:

    Authentication
    Authorization
    Rate Limiting
    Audit Logging
    Threat Modeling
    Risk Assessment

---

# 7.1 Security Terminology

The implementation is in:

    security_models.py

The model includes:

- Confidentiality
- Integrity
- Availability
- Authenticity
- Security Controls
- Security Policies

---

# 7.2 Threat Terminology

The implementation is in:

    threat_models.py

The important distinction is:

    Threat
       |
       v
    Vulnerability
       |
       v
    Exploit
       |
       v
    Attack
       |
       v
    Impact

A threat is not the same thing as a vulnerability.

A vulnerability is a weakness.

An exploit is a way to abuse the weakness.

---

# 7.3 Threat Agents

Threat agents are represented by:

    ThreatAgent

Current agents:

- anonymous attacker
- malicious service agent
- trusted attacker
- malicious insider

---

# 7.4 Common Threats

The threat catalog is stored in:

    threat_catalog.json

It contains examples including:

- traffic eavesdropping
- malicious intermediary
- denial of service
- insufficient authorization
- virtualization attack
- overlapping trust boundaries
- containerization attack
- malware
- insider threat
- social engineering
- botnet
- privilege escalation
- brute force
- remote code execution
- SQL injection
- tunneling
- advanced persistent threat

The catalog is loaded by:

    threat_catalog.py

---

# Risk Assessment

Risk is represented as:

    Risk = Likelihood x Impact

Likelihood:

    1 - 5

Impact:

    1 - 5

Risk levels:

    1-5     LOW
    6-11    MEDIUM
    12-19   HIGH
    20-25   CRITICAL

---

# Cloud Lab Risk Register

The current system is evaluated in:

    case_study.json

The main assets are:

- API
- PostgreSQL
- Tenant resources

Important trust boundaries:

    Internet -> API
    API -> PostgreSQL
    Tenant A -> Tenant B
    Container -> Host

---

# Security Controls

Implemented in:

    security_controls.py

Current controls:

- Authentication
- Authorization
- Rate Limiting
- Audit Logging
- Input Validation

---

# Authorization Experiment

The most important practical experiment is tenant isolation.

Alice:

    tenant-a

Resource A:

    tenant-a

Resource B:

    tenant-b

Expected:

    Alice -> Resource A = ALLOWED

    Alice -> Resource B = DENIED

This demonstrates the security consequence of
multitenancy from Chapter 4.

---

# API Integration

The security model is integrated into:

    apps/api/app/security.py
    apps/api/app/security_store.py
    apps/api/app/security_routes.py

The API now implements:

    Authentication
        |
        v
    Identity
        |
        v
    Authorization
        |
        v
    Resource Access

---

# Authentication

The lab uses a simple HMAC-signed bearer token.

This implementation is intentionally educational.

It is NOT a production authentication system.

Production systems should use established identity
and token mechanisms.

---

# Run the conceptual experiment

From repository root:

```bash
python -m experiments.ch07_security.demo