# AWS Architecture

## Overview

The local architecture is:

    FastAPI
       |
       +-- PostgreSQL
       +-- Storage
       +-- Queue
       +-- Worker
       +-- Monitoring

The AWS architecture maps these components to managed
AWS services.

---

## API

Local:

    FastAPI

AWS:

    API Gateway
        |
        v
    Lambda

---

## Database

Local:

    PostgreSQL

AWS:

    RDS PostgreSQL

---

## Object Storage

Local:

    LocalStorageProvider

AWS:

    S3

---

## Queue

Local:

    LocalQueue

AWS:

    SQS

---

## Worker

Local:

    MetricsWorker

AWS:

    Lambda

---

## Monitoring

Local:

    MetricRepository

AWS:

    CloudWatch

---

## Architecture

                 Internet
                    |
                    v
              API Gateway
                    |
                    v
                 Lambda
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
       RDS          S3          SQS
                                |
                                v
                              Lambda
                                |
                                v
                           CloudWatch