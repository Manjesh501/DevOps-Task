#!/bin/bash

# Idempotent deployment script for AWS EC2 with ECR
# This script authenticates with ECR, pulls latest images, stops old containers, and starts the new stack

set -e  # Exit on any error

echo "Starting deployment..."

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Authenticate with ECR
echo "Authenticating with ECR..."
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 815539056618.dkr.ecr.eu-north-1.amazonaws.com

# Pull latest images
echo "Pulling latest Docker images..."
docker-compose pull

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Start new containers
echo "Starting new containers..."
docker-compose up -d

# Wait a moment for containers to start
sleep 5

# Check container status
echo "Checking container status..."
docker-compose ps

echo "Deployment completed successfully!"

# Print container logs
echo "Printing recent logs..."
docker-compose logs --tail=20