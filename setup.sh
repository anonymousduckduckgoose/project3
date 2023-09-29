#!/bin/bash

# Update package manager
sudo apt update

# Install Docker
sudo apt install -y docker

# Navigate to your Dockerfile directory
cd ./build

# Build & run your Docker image via compose
docker-compose up --build