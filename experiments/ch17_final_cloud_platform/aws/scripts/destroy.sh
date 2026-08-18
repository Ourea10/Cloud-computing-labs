#!/bin/bash

set -e

STACK_NAME="cloud-learning-ch17"

echo "Deleting stack..."

aws cloudformation delete-stack \
    --stack-name "$STACK_NAME"

echo "Delete request submitted."