# AINI - AI Infrastructure Management Tool

AINI provides automated deployment of AI and productivity infrastructure using Docker and Ansible.

## Features

- Automated server provisioning on Hetzner Cloud
- IPv6-first networking
- Automatic UFW firewall configuration
- Docker with IPv6 support
- Complete application stack:
  - Traefik (reverse proxy + SSL)
  - LibreChat (AI frontend)
  - N8N (workflow automation)
  - Consul + Vault (configuration/secrets)
  - Nextcloud + OnlyOffice (file storage/editing)
  - Netdata (monitoring)
  - Watchtower (automatic updates)

## Prerequisites

- Ansible 2.9 or higher
- Python 3.6 or higher
- Hetzner Cloud account
- SSH key pair

## Setup

1. Install Ansible dependencies:
```bash
ansible-galaxy install -r ansible/requirements.yml
ansible-galaxy collection install -r ansible/requirements.yml
```

2. Configure secrets:
```bash
# Copy the example secrets file
cp ansible/vars/secrets.example.yml ansible/vars/secrets.yml

# Create a vault password file (keep this secure and never commit it)
echo "your-secure-password" > .vault_pass
chmod 600 .vault_pass

# Edit your secrets
ansible-vault edit ansible/vars/secrets.yml
```

3. Configure required variables in secrets.yml:
   - `hetzner_token`: Your Hetzner Cloud API token
   - `hetzner_ssh_key_name`: Name for your SSH key in Hetzner
   - `project_name`: Your project name (used for server naming)
   - `app_server_type`: Hetzner server type (e.g., "cx11")
   - Optional variables:
     - `server_image`: Server OS image (default: "ubuntu-24.04")
     - `server_location`: Hetzner datacenter location (default: "fsn1")
   - Other configuration variables as needed

## Quick Start

1. Initialize SSH key in Hetzner:
```bash
ansible-playbook ansible/playbooks/configure/ssh_key.yml
```

2. Create S3 storage bucket:
```bash
ansible-playbook ansible/playbooks/configure/storage.yml
```

3. Manage servers:
```bash
# Create application servers
ansible-playbook ansible/playbooks/provision/app_servers.yml -e "state=present"

# Configure base system and applications
ansible-playbook ansible/playbooks/configure/base.yml
ansible-playbook ansible/playbooks/configure/apps.yml

# Delete application servers
ansible-playbook ansible/playbooks/provision/app_servers.yml -e "state=absent"
```

4. Or use the deploy playbook for full infrastructure management:
```bash
# Create all infrastructure
ansible-playbook ansible/playbooks/deploy.yml -e "action=create"

# Delete all infrastructure
ansible-playbook ansible/playbooks/deploy.yml -e "action=delete"

# Deploy specific components using tags
ansible-playbook ansible/playbooks/deploy.yml --tags "servers,storage,app"

# For app servers
ansible-playbook deploy.yml -e "action=create" --tags app

# For GPU servers
ansible-playbook deploy.yml -e "action=create" --tags gpu

# For deletion
ansible-playbook deploy.yml -e "action=delete" --tags app

# For base configuration
ansible-playbook ansible/playbooks/configure/base.yml
```

## Directory Structure

```
aini/
├── ansible/
│   ├── inventory/                # Server inventory
│   ├── playbooks/               # Playbook files
│   ├── roles/                   # Ansible roles
│   └── vars/                    # Variable files
│       ├── secrets.yml          # Encrypted secrets (do not commit unencrypted)
│       └── secrets.example.yml  # Example secrets file
├── docker/                      # Docker configurations
├── docs/                        # Documentation
├── tests/                       # Test scripts
├── scripts/                     # Utility scripts
└── README.md                    # This file
```

## Security

- All sensitive information is encrypted using Ansible Vault
- Never commit the `.vault_pass` file
- Keep your vault password secure

## Development

1. Install dependencies:
```bash
pip install -r requirements.txt
ansible-galaxy install -r ansible/requirements.yml
```

2. Set up your secrets as described in the Setup section

## Documentation

- [Architecture](docs/architecture.md) - System components and design
- [Development](docs/development.md) - Development guide

## License

MIT

## Infrastructure Management

### Server Management
- Servers can be created and deleted using the provision playbooks
- Use the `state` variable to control server lifecycle:
  - `present`: Creates the server
  - `absent`: Deletes the server
- Server information is automatically managed in the inventory
- Servers are configured with IPv6 by default
- The inventory uses IPv6 addresses for connectivity

### Available Tags
- `infrastructure`: All infrastructure tasks
- `ssh_key`: SSH key management
- `storage`: Storage management
- `servers`: Server management
- `configure`: Configuration tasks
- `always`: Tasks that run regardless of tags

### Networking
- Primary connectivity is via IPv6
- UFW firewall configured for both IPv4 and IPv6
- Docker configured with IPv6 support
- All services accessible via IPv6