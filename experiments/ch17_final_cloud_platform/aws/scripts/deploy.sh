#!/bin/bash

set -e

STACK_NAME="cloud-learning-ch17"

echo "Deploying CloudFormation stack..."

aws cloudformation deploy \
    --template-file \
    experiments/ch17_final_cloud_platform/aws/cloudformation/template.yaml \
    --stack-name "$STACK_NAME"

echo "Deployment completed."