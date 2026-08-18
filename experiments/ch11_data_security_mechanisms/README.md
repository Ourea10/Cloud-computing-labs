# Chapter 11 — Cloud Security and Cybersecurity Data-Oriented Mechanisms

## Objective

Chapter 10 focused on access-oriented security.

Chapter 11 focuses on protecting the data itself.

The implemented mechanisms are:

1. Digital Virus Scanning and Decryption System
2. Malicious Code Analysis System
3. Data Loss Prevention System
4. Trusted Platform Module
5. Data Backup and Recovery System
6. Activity Log Monitor
7. Traffic Monitor
8. Data Loss Protection Monitor

---

# Security Model

The Chapter 11 security pipeline is:

    Data
      |
      v
    Decryption
      |
      v
    Virus Scanning
      |
      v
    Malicious Code Analysis
      |
      v
    DLP
      |
      v
    Storage
      |
      +---- Backup
      |
      +---- Activity Logging
      |
      +---- Traffic Monitoring
      |
      +---- Data Loss Monitoring

---

# 1. Digital Virus Scanning

File:

    virus_scanner.py

The system scans files for known malicious signatures.

This laboratory uses a synthetic test signature instead
of real malware.

---

# 2. Malicious Code Analysis

File:

    malicious_code_analyzer.py

The analyzer detects suspicious code patterns.

Example:

    os.system()
    subprocess
    eval()
    exec()
    file deletion

The goal is to demonstrate behavior-oriented analysis.

---

# 3. Data Loss Prevention

File:

    dlp.py

DLP evaluates whether data can be transferred to a destination.

Example:

    confidential data
          |
          v
    external destination
          |
          v
        BLOCK

DLP is a preventive mechanism.

---

# 4. Trusted Platform Module

File:

    tpm.py

The TPM implementation models a hardware-backed
cryptographic root of trust.

The implementation is conceptual and does not emulate
real TPM hardware.

---

# 5. Backup and Recovery

File:

    backup_recovery.py

The system creates snapshots of cloud resources.

The snapshot contains:

    resource ID
    timestamp
    data
    checksum

Recovery verifies the checksum before restoring data.

---

# 6. Activity Log Monitor

File:

    activity_log_monitor.py

Records data-related activity:

    upload
    download
    read
    delete

This differs from the authentication log monitor
implemented in Chapter 10.

---

# 7. Traffic Monitor

File:

    traffic_monitor.py

Records network traffic metadata:

    source
    destination
    port
    protocol
    bytes transferred

The monitor focuses on traffic observation rather than
intrusion detection.

---

# 8. Data Loss Protection Monitor

File:

    data_loss_protection.py

Detects suspicious data transfer volume.

Example:

    normal transfer
        10 MB

    suspicious transfer
        500 MB

The monitor can generate a data-loss event.

---

# Integration

The mechanisms are combined into SecureDataService.

    Client
       |
       v
    Decryption
       |
       v
    Virus Scanner
       |
       v
    Code Analysis
       |
       v
    DLP
       |
       v
    Storage
       |
       +---- Backup
       |
       +---- Activity Log
       |
       +---- Traffic Monitor
       |
       +---- Data Loss Monitor

---

# Relationship with Chapter 10

Chapter 10:

    Who can access the data?

Chapter 11:

    What happens to the data?

Therefore:

    Chapter 10
        IAM
        MFA
        SSO
        Security Groups
        Firewall
        VPN
             |
             v
    Chapter 11
        Virus Scanning
        DLP
        Backup
        Monitoring
        Data Loss Detection

---

# AWS Mapping

| Laboratory | AWS |
|---|---|
| Virus Scanner | GuardDuty / malware scanning concepts |
| Malicious Code Analysis | GuardDuty / security analysis concepts |
| DLP | Macie / DLP concepts |
| TPM | Nitro / hardware-rooted trust concepts |
| Backup | AWS Backup |
| Activity Log | CloudTrail |
| Traffic Monitor | VPC Flow Logs / CloudWatch |
| Data Loss Monitor | Macie / GuardDuty / CloudWatch concepts |

The laboratory does not attempt to clone AWS services.

It models the underlying cloud security mechanisms.

---

# Why this matters

The important architectural distinction is:

    Authentication
        !=
    Data protection

A correctly authenticated user can still:

    accidentally upload malware
    download confidential data
    delete important files
    transfer excessive data
    leak sensitive information

Therefore cloud security requires multiple layers.

---

# Run

    python -m experiments.ch11_data_security_mechanisms.demo

Run tests:

    pytest experiments/ch11_data_security_mechanisms -v