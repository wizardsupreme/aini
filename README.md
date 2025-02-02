# AINI - AI Infrastructure Management Tool

AINI provides automated deployment of AI and productivity infrastructure using Docker and Ansible.

## Features

- Automated server provisioning on Hetzner Cloud
- IPv6-first networking
- Automatic UFW firewall configuration
- Docker with IPv6 support
- Complete application stack:
  - Traefik (reverse proxy + SSL)
  - Netdata + cAdvisor (system and container monitoring)
  - Consul + Vault (configuration/secrets)
  - AFFiNE (Notion-like workspace, knowledge base)
  - Nextcloud (file storage/sync with Hetzner Storage Box)
  - NocoDB (Airtable alternative)
  - Watchtower (automatic updates)
  - LibreChat (AI frontend)
  - N8N (workflow automation)

## Prerequisites

- Python 3.11 or higher
- uv (Python package installer)
- SSH key pair
- Hetzner Cloud account
- Supabase account
- git-crypt installed

## Directory Structure
ansible/
├── inventory/
│   └── group_vars/        # Group variables
├── playbooks/
│   ├── deploy.yml         # Main deployment playbook
│   └── includes/
│       ├── apps.yml       # Application deployments
│       └── load_vars.yml  # Variable loading
├── roles/
│   ├── infrastructure/    # Infrastructure roles
│   │   ├── app_server/
│   │   └── ssh_key/
│   └── apps/             # Application roles
│       ├── traefik/
│       ├── netdata/
│       ├── affine/
│       ├── nextcloud/
│       └── ... other apps
└── vars/
    └── dev2/             # Environment specific vars
        └── secrets.yml   # Encrypted secrets

## Resource Management

### System Resources (CAX11 - 4GB RAM)
Core Services:
  - Traefik: ~50MB
  - Netdata: ~200MB
  - cAdvisor: ~128MB
Main Applications:
  - AFFiNE: ~500MB
  - Nextcloud + MariaDB: ~800MB
  - NocoDB: ~150MB
Infrastructure:
  - Consul: ~250MB
  - Vault: ~100MB
  - n8n: ~200MB
  - LibreChat: ~300MB

### External Services
- Supabase:
  - Authentication
  - Database backend for AFFiNE, NocoDB, n8n
  - Real-time collaboration
- Hetzner Storage Box:
  - SFTP storage for Nextcloud
  - Backup storage

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
uv venv
source .venv/bin/activate
```

3. Install project dependencies:
```bash
uv pip install -r requirements.txt
```

## Git-Crypt Setup

1. Install git-crypt:
```bash
# macOS
brew install git-crypt

# Ubuntu/Debian
apt-get install git-crypt
```

2. Initialize git-crypt in your repository:
```bash
git-crypt init
```

3. Configure .gitattributes:
```
ansible/vars/dev2/secrets.yml filter=git-crypt diff=git-crypt
```

4. Add trusted GPG keys:
```bash
git-crypt add-gpg-user USER_ID
```

5. Unlock repository after cloning:
```bash
git-crypt unlock
```

## Supabase Setup

1. Create a Supabase project
2. Configure environment variables in secrets.yml:
```yaml
supabase_url: "your-project-url"
supabase_anon_key: "your-anon-key"
supabase_service_role_key: "your-service-role-key"
```

## Quick Start

1. Initialize SSH key in Hetzner:
```bash
ansible-playbook playbooks/deploy.yml --tags "ssh_key"
```

2. Deploy core infrastructure:
```bash
ansible-playbook playbooks/deploy.yml --tags "apps,traefik,netdata"
```

3. Deploy applications:
```bash
# Deploy all apps
ansible-playbook playbooks/deploy.yml --tags "apps"

# Deploy specific apps
ansible-playbook playbooks/deploy.yml --tags "apps,affine,nextcloud,nocodb"
```

## Security

- All sensitive files are encrypted using git-crypt
- Ensure your GPG key is secure
- Never commit unencrypted sensitive files
- Check .gitattributes for encrypted files

## Documentation

- [Architecture](docs/architecture.md)
- [Development](docs/development.md)

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
