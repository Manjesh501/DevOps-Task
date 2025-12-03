#!/bin/bash

# Simple frontend test script
# Checks if required files exist

echo "Running frontend tests..."

# Check if index.html exists
if [ -f "index.html" ]; then
    echo "✓ index.html exists"
else
    echo "✗ index.html not found"
    exit 1
fi

# Check if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "✓ Dockerfile exists"
else
    echo "✗ Dockerfile not found"
    exit 1
fi

# Check if nginx.conf exists
if [ -f "nginx.conf" ]; then
    echo "✓ nginx.conf exists"
else
    echo "✗ nginx.conf not found"
    exit 1
fi

echo "All frontend tests passed! ✓"