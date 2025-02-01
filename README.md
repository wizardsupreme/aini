# AINI - AI Infrastructure Management Tool

AINI provides automated deployment of AI and productivity infrastructure using Docker and Ansible.

## Features

- Automated server provisioning on Hetzner Cloud
- IPv6-first networking
- Automatic UFW firewall configuration
- Docker with IPv6 support
- Complete application stack:
  - Traefik (reverse proxy + SSL)
  - Netdata (monitoring)
  - Consul + Vault (configuration/secrets)
  - Nextcloud + OnlyOffice (file storage/editing)
  - Watchtower (automatic updates)
  - LibreChat (AI frontend)
  - N8N (workflow automation)

## Prerequisites

- Python 3.11 or higher
- uv (Python package installer)
- SSH key pair
- Hetzner Cloud account

## Local Development Setup

1. Install uv:
```bash
# On macOS
brew install uv

# On Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create and activate a virtual environment:
```bash
# Create a new venv in the project directory
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install project dependencies:
```bash
uv pip install -r requirements.txt
```

4. Install Ansible dependencies (these will be installed in the project's ansible/roles and ansible/collections directories):
```bash
# Install roles to ansible/roles
ansible-galaxy install -r ansible/requirements.yml --roles-path ansible/roles

# Install collections to ansible/collections
ansible-galaxy collection install -r ansible/requirements.yml --collections-path ansible/collections
```

5. Configure secrets:
```bash
# Copy the example secrets file
cp ansible/vars/secrets.example.yml ansible/vars/secrets.yml

# Create a vault password file (keep this secure and never commit it)
echo "your-secure-password" > .vault_pass
chmod 600 .vault_pass

# Edit your secrets
ansible-vault edit ansible/vars/secrets.yml
```

6. Configure required variables in secrets.yml:
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
this doesnt currently work as we are using hetzner storage which doesnt seem to work with api calls.
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
ansible-playbook ansible/playbooks/deploy.yml -e "action=create" --tags app

# For GPU servers
ansible-playbook ansible/playbooks/deploy.yml -e "action=create" --tags gpu

# For deletion
ansible-playbook ansible/playbooks/deploy.yml -e "action=delete" --tags app

# For base configuration
ansible-playbook ansible/playbooks/configure/base.yml
```

## Directory Structure

```
aini/
├── ansible/
│   ├── collections/            # Ansible collections (gitignored)
│   ├── inventory/             # Server inventory
│   ├── playbooks/            # Playbook files
│   ├── roles/                # Ansible roles (gitignored)
│   │   └── requirements.yml  # Role requirements specification
│   └── vars/                 # Variable files
│       ├── secrets.yml       # Encrypted secrets (do not commit unencrypted)
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

## Monitoring and Troubleshooting

### Remote Docker Management

#### Note on docker compose vs docker-compose
There are two different commands for Docker Compose:
- `docker compose` (new, recommended, part of Docker CLI)
- `docker-compose` (legacy standalone binary)

The new `docker compose` command supports contexts natively, while `docker-compose` requires environment variables:

```bash
# For docker compose (recommended):
docker --context aini-apps-server compose -f /opt/aini/traefik/docker-compose.yml ps

# For docker-compose (legacy):
export DOCKER_HOST="ssh://root@your-server-ip"
docker-compose -f /opt/aini/traefik/docker-compose.yml ps
```

We recommend using `docker compose` (without hyphen) as it's the newer standard and has better integration with Docker contexts.

You can manage Docker on the remote server directly from your local machine using Docker contexts:

```bash
# Create a new context
docker context create aini-apps-server --docker "host=ssh://root@your-server-ip"

# Switch to the context
docker context use aini-apps-server

# Switch back to local Docker
docker context use default

# Or use for a single command
docker --context aini-apps-server ps
```

### Using docker compose with contexts
You can create aliases in your shell to make this easier:

```bash
# Add these to your ~/.bashrc or ~/.zshrc
alias dps='docker --context aini-apps-server ps'
alias dc='docker --context aini-apps-server compose -f /opt/aini/traefik/docker-compose.yml'

# Then you can use:
dc ps
dc logs
dc up -d
```

Or use environment variables:
```bash
# Set these before running docker compose commands
export DOCKER_CONTEXT=aini-apps-server
export COMPOSE_FILE=/opt/aini/traefik/docker-compose.yml

# Then you can just use:
docker compose ps
docker compose logs
```

### Access Services:
- Traefik Dashboard: https://traefik.yourdomain.com
  - Login with credentials from your secrets.yml

### Common Issues

1. Check if ports are properly exposed:
```bash
docker --context aini-apps-server port traefik
```

2. Verify network connectivity:
```bash
# Test HTTPS endpoint
curl -I https://traefik.yourdomain.com
```

3. View detailed container information:
```bash
docker --context aini-apps-server inspect traefik
```

4. Check container health:
```bash
docker --context aini-apps-server ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"
```

### Security Note
- Ensure your SSH keys are properly configured
- Keep your Docker contexts secure
- Never expose Docker daemon ports directly to the internet
- Always use SSH for remote Docker management
