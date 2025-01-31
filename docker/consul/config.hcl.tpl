# Basic server configuration
data_dir = "${CONSUL_DATA_DIR}"
server = true
bootstrap = true
ui = true
client_addr = "0.0.0.0"

# Stability settings
performance {
  raft_multiplier = 1
}

# Ensure we're in non-dev mode
leave_on_terminate = false
skip_leave_on_interrupt = true
log_level = "DEBUG"  # Add this at the top

enable_debug = true
# Backup configuration
snapshot_agent {
  enabled = true
  snapshot {
    interval    = "15m"  # More frequent backups
    retain      = 30
    deregister_after = "8h"
  }

  aws_storage {
    access_key_id     = "${S3_ACCESS_KEY}"
    secret_access_key = "${S3_SECRET_KEY}"
    s3_region        = "${S3_REGION}"
    s3_bucket        = "${S3_BUCKET}"
    s3_key_prefix    = "consul-backups/"
    s3_endpoint      = "${S3_ENDPOINT}"
    enable_s3_server_side_encryption = true
  }
} 