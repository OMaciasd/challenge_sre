#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
echo "Updating and upgrading system..."
sudo apt-get update && sudo apt-get upgrade -y
echo "Installing basic packages..."
sudo apt-get install -y curl jq
echo "Installing Docker..."
sudo apt-get install -y docker.io
echo "Starting Docker service..."
sudo systemctl enable docker && sudo systemctl start docker
echo "Setup complete."
