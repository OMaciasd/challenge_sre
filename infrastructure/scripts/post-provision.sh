#!/bin/bash

mkdir -p /home/vagrant/terraform

cp -r /home/vagrant/src/ /home/vagrant/terraform/

source /home/vagrant/.bashrc

echo "Checking Docker..."
if command -v docker &> /dev/null
then
    docker --version
else
    echo "Docker no está instalado."
    exit 1
fi

echo "Checking Minikube..."
if command -v minikube &> /dev/null
then
    minikube version
else
    echo "Minikube no está instalado."
    exit 1
fi

echo "Checking kubectl..."
if command -v kubectl &> /dev/null
then
    kubectl version --client
else
    echo "kubectl no está instalado."
    exit 1
fi
