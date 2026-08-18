# AWS Deployment Lab

This directory contains the AWS implementation of
Chapter 17.

The purpose is educational.

The infrastructure should be created, tested,
observed, and destroyed.

---

# Architecture

    Internet
       |
       v
    API Gateway
       |
       v
    Lambda
       |
       +----------+
       |          |
       v          v
      RDS         S3
       |
       |
       v
      SQS
       |
       v
    Worker Lambda
       |
       v
    CloudWatch

---

# Local vs AWS

| Local | AWS |
|---|---|
| FastAPI | Lambda |
| LocalComputeProvider | Lambda |
| LocalStorageProvider | S3 |
| LocalQueue | SQS |
| PostgreSQL | RDS |
| MonitoringService | CloudWatch |
| LocalNetworkProvider | VPC |

---

# Deployment Order

The recommended deployment order is:

1. IAM
2. Network
3. Storage
4. Queue
5. Database
6. Lambda
7. API Gateway
8. Monitoring

Do not deploy everything at once.

The purpose is to understand each dependency.

---

# Deployment

Run:

    ./scripts/deploy.sh

Verify:

    aws cloudformation describe-stacks \
        --stack-name cloud-learning-ch17

---

# Testing

Health check:

    GET /health

Then test:

    POST /auth/register
    POST /auth/login
    POST /projects
    POST /resources
    POST /monitoring/{resource_id}/metrics

---

# Monitoring

Check:

- Lambda invocation count
- Lambda errors
- Lambda duration
- SQS messages
- S3 objects
- API Gateway requests

---

# Cleanup

After completing the experiment:

    ./scripts/destroy.sh

Verify that the stack has been deleted.

---

# Cost Safety

This project is educational.

Do not leave AWS resources running unnecessarily.

Especially check:

- NAT Gateway
- RDS
- Load Balancers
- EC2
- Elastic IP
- CloudWatch resources

before ending the experiment.