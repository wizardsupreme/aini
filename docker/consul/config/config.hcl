# Basic server configuration
data_dir = "/consul/data"
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
    access_key_id     = "***REMOVED***"
    secret_access_key = "***REMOVED***"
    s3_region        = "eu-north-1"
    s3_bucket        = "***REMOVED***"
    s3_key_prefix    = "consul-backups/"
    s3_endpoint      = "https://***REMOVED***"
    enable_s3_server_side_encryption = true
  }
} 