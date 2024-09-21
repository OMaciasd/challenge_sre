#!/bin/bash

cd ../terraform || { echo "Failed to change directory to ../terraform"; exit 1; }

terraform init
terraform plan
terraform apply --auto-approve
