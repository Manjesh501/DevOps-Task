#!/bin/bash

# Deployment validation script
# This script checks if the deployment was successful

set -e

echo "Validating deployment..."

# Check if containers are running
echo "Checking container status..."
if docker-compose ps | grep -q "Up"; then
    echo "✓ Containers are running"
else
    echo "✗ Containers are not running"
    exit 1
fi

# Test backend endpoint
echo "Testing backend endpoint..."
if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    echo "✓ Backend is responding"
else
    echo "✗ Backend is not responding"
    exit 1
fi

# Test frontend endpoint
echo "Testing frontend endpoint..."
if curl -f http://localhost:80/ > /dev/null 2>&1; then
    echo "✓ Frontend is responding"
else
    echo "✗ Frontend is not responding"
    exit 1
fi

# Test nginx reverse proxy
echo "Testing nginx reverse proxy..."
if curl -f http://localhost:8080/api/status > /dev/null 2>&1; then
    echo "✓ Nginx reverse proxy is working"
else
    echo "✗ Nginx reverse proxy is not working"
    exit 1
fi

echo "All deployment tests passed! ✓"