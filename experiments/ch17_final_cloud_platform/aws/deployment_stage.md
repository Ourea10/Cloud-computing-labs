Stage 1
FastAPI
  ↓
local
Stage 2
FastAPI
  ↓
Docker
  ↓
local PostgreSQL
Stage 3
FastAPI
  ↓
AWS Lambda
Stage 4
Lambda
 ↓
RDS
Stage 5
Lambda
 ↓
S3
Stage 6
Lambda
 ↓
SQS
 ↓
Worker Lambda
Stage 7
CloudWatch
Stage 8
IAM
Stage 9
API Gateway

Finally:

                  Internet
                     │
                     ▼
                API Gateway
                     │
                     ▼
                   Lambda
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
       RDS           S3          SQS
                                  │
                                  ▼
                                Lambda
                                  │
                                  ▼
                             CloudWatch