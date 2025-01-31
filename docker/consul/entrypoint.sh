#!/bin/sh
set -e

# Create data directory if it doesn't exist
mkdir -p ${CONSUL_DATA_DIR}

# Process the template
envsubst < /consul/config/config.hcl.tpl > /consul/config/config.hcl

# Start Consul in background
consul agent -config-file=/consul/config/config.hcl &

# Wait for Consul to be ready
until consul members > /dev/null 2>&1; do
  echo "Waiting for Consul to start..."
  sleep 1
done

# Store environment variables in Consul KV
consul kv put ***REMOVED***/config/environment/s3 "{
  \"access_key\": \"${S3_ACCESS_KEY}\",
  \"secret_key\": \"${S3_SECRET_KEY}\",
  \"bucket\": \"${S3_BUCKET}\",
  \"endpoint\": \"${S3_ENDPOINT}\",
  \"region\": \"${S3_REGION}\"
}"

consul kv put ***REMOVED***/config/environment/hcloud "{
  \"token\": \"${HCLOUD_TOKEN}\",
  \"app_server_type\": \"${APP_SERVER_TYPE}\",
  \"gpu_server_type\": \"${GPU_SERVER_TYPE}\"
}"

consul kv put ***REMOVED***/config/environment/debug "{
  \"enabled\": \"${DEBUG:-false}\"
}"

# Keep container running
wait 