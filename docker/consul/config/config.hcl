# Basic server configuration
data_dir = "/consul/data"
server = true
bootstrap = true
ui = true
client_addr = "0.0.0.0"
log_level = "DEBUG"
enable_debug = true

# Stability settings
performance {
  raft_multiplier = 1
}

# Ensure we're in non-dev mode
leave_on_terminate = false
skip_leave_on_interrupt = true

# Backup configuration
snapshot_agent {
  enabled = true
  log_level = "DEBUG"
  
  # Run as a daemon
  daemon = true
  daemon_json = "/consul/config/snapshot.json"
  
  snapshot {
    interval    = "1m"
    retain      = 30
    deregister_after = "8h"
  }

  aws_storage {
    access_key_id     = "ENEXTCALGCHFO75QMZOO"
    secret_access_key = "KaRg1N1oHGE49MsXn5HZUA0cFqM21lCGi9G1ED2P"
    s3_region        = "eu-north-1"
    s3_bucket        = "aini"
    s3_key_prefix    = "consul-backups/"
    s3_endpoint      = "https://hel1.your-objectstorage.com"
    enable_s3_server_side_encryption = true
  }
} 