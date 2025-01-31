#!/bin/bash
set -e

# Stop containers
docker compose down

# Clean up state directory
rm -rf docker/consul/data

# Create fresh state directory
mkdir -p docker/consul/data

# Start containers
docker compose up -d 