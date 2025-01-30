#!/bin/bash
set -e

# Create necessary directories if they don't exist
mkdir -p /***REMOVED***/.***REMOVED***-state/consul
mkdir -p /***REMOVED***/dashboard/assets

# Initialize Homer config if it doesn't exist
if [ ! -f /***REMOVED***/dashboard/config.yml ]; then
    mkdir -p /***REMOVED***/dashboard
    cat > /***REMOVED***/dashboard/config.yml << EOL
---
title: "AINI Dashboard"
subtitle: "AI Nomad Infrastructure"
logo: "assets/logo.svg"
header: true
footer: '<p>AINI - AI Nomad Infrastructure</p>'

services:
  - name: "Infrastructure"
    icon: "fas fa-server"
    items:
      - name: "Consul"
        subtitle: "Service Discovery & State Management"
        url: "http://localhost:8500"
        target: "_blank"
EOL
fi

# Create default .env if it doesn't exist
if [ ! -f /***REMOVED***/.env ]; then
    cp /***REMOVED***/.env.example /***REMOVED***/.env 2>/dev/null || :
fi

# Start the API server if running in container
if [ -f /***REMOVED***/cli/api.py ]; then
    python /***REMOVED***/cli/api.py &
fi

# Execute the command passed to docker
exec "$@"