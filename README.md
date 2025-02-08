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

## Git-Crypt Configuration

This repository uses [git-crypt](https://github.com/AGWA/git-crypt) to encrypt sensitive files. Below are instructions for setting up and managing git-crypt.

### Prerequisites
- Install git-crypt on your system:
  - **Linux (Debian/Ubuntu)**: `sudo apt-get install git-crypt`
  - **macOS (Homebrew)**: `brew install git-crypt`
  - **Windows (Chocolatey)**: `choco install git-crypt`
- Ensure you have a GPG key pair (public and private keys).

### Adding a New User
1. **Export your public key**:
   ```bash
   gpg --export --armor <YOUR_KEY_ID> > my-public-key.asc
   ```
   Share the `my-public-key.asc` file with the repository maintainer.

2. **Repository maintainer adds your key**:
   ```bash
   gpg --import my-public-key.asc
   git-crypt add-gpg-user --trusted <YOUR_KEY_ID>
   git commit -m "Added new user to git-crypt"
   git push
   ```

### Unlocking the Repository
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   ```

2. **Unlock the repository**:
   ```bash
   git-crypt unlock
   ```
   This will decrypt the files using your private GPG key.

### Managing Encrypted Files
- **Encrypt new files**: Add the file pattern to `.gitattributes`. For example:
  ```plaintext
  *.secret filter=git-crypt diff=git-crypt
  ```
- **Check encryption status**:
  ```bash
  git-crypt status
  ```

### Troubleshooting
- **Can't unlock the repository?**
  - Ensure your private GPG key is imported: `gpg --import your-private-key.asc`
  - Verify your key is in the keyring: `git-crypt ls-gpg-users`
- **Files still encrypted?**
  - Ensure you pulled the latest changes: `git pull`
  - Confirm the files are encrypted: `git-crypt status`

For more details, refer to the [git-crypt documentation](https://github.com/AGWA/git-crypt).

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

# AI-Powered Infrastructure Stack

## Core Components

### 1. Authentication & Database
- **Supabase** (self-hosted)
  - PostgreSQL database
  - Auth management
  - Resource needs:
    - 2-4 CPU cores
    - 4-8GB RAM
    - 20GB SSD

### 2. Document Management
- **Nextcloud**
  - File storage
  - Mail interface
  - Calendar/Contacts
  - Resource needs:
    - 2 CPU cores
    - 4GB RAM
  - Dependencies:
    - MariaDB
    - Redis

### 3. Document Editing
- **OnlyOffice** (self-hosted)
  - Document server
  - Resource needs:
    - 2 CPU cores
    - 2GB RAM
    - 4GB storage

### 4. Vector Database
- **Milvus**
  - Knowledge storage
  - Vector search
  - Resource needs:
    - 4-8 CPU cores
    - 8-16GB RAM
    - NVMe SSD recommended

### 5. Email System
- **Zoho Mail** (external service)
  - Free tier
  - 5 users
  - 5GB per user
  - SMTP/IMAP for Nextcloud

### 6. AI Agent Interface
- **LibreChat**
  - Web interface
  - API access
  - Resource needs:
    - 2 CPU cores
    - 4GB RAM

### 7. Automation
- **n8n**
  - Workflow automation
  - Resource needs:
    - 1-2 CPU cores
    - 2GB RAM

### 8. Reverse Proxy
- **Traefik**
  - SSL termination
  - Routing
  - Resource needs:
    - 1 CPU core
    - 1GB RAM

## Server Requirements

### Minimum Total Resources
- CPU: 16-24 cores total
- RAM: 32-48GB total
- Storage: 100GB+ NVMe SSD
- Network: 1Gbps

### Recommended Hetzner Setup
1. **Primary Server** (AX41-NVMe)
   - 8 cores
   - 32GB RAM
   - 2x512GB NVMe
   - Cost: ~€44.90/month

2. **Secondary Server** (CPX31)
   - 4 cores
   - 8GB RAM
   - 160GB SSD
   - Cost: ~€13.90/month

## Domain Requirements
- Primary domain for services
- DNS configuration for:
  - Nextcloud
  - OnlyOffice
  - LibreChat
  - Email (Zoho)
  - Other services

## Cost Breakdown
### Monthly Infrastructure
- Hetzner AX41: €44.90
- Hetzner CPX31: €13.90
- Domain: ~€1-2
- Zoho Mail: Free tier
- All other services: Self-hosted/Free

**Total Monthly: ~€60-65**

## Maintenance Requirements
- Regular backups
- Security updates
- Performance monitoring
- SSL certificate renewal (automated)
- Storage management

## AI Agent Management
- Email monitoring/responses
- Document organization
- Workflow automation
- System health monitoring
- User support

## Adding New Application Stacks

When requesting AI assistance to add new application stacks to this Ansible configuration, provide the following details in your prompt:

1. Application name and Docker image details
2. Required configuration variables and environment settings
3. Any persistent storage needs
4. Network requirements (ports, domains)
5. Dependencies (databases, caches, etc.)
6. Security considerations (API keys, secrets)

### Example Prompt Template

## Best Practices
- Use consistent variable naming across files
- Prefix all sensitive variables with `vault_`
- Follow existing network configuration patterns
- Use standard Docker Compose v2 syntax
- Include appropriate tags for selective deployment
- Document any special requirements or dependencies

## Database Management

### PgAdmin Role

The `apps/pgadmin` role serves two purposes:
1. Deploys a pgAdmin web interface for database management
2. Handles automated database and user creation

#### Database Configuration

Databases are defined in `vars/dev2/postgres_manager.yml`:

```yaml
postgres_databases:
  myapp: {}  # Uses default public schema only
  analytics:
    schemas:  # Specify additional schemas if needed
      - reporting
      - metrics
```

Each database:
- Gets its own user with the same name as the database
- Has its password defined in `vars/dev2/secrets.yml` as `vault_<dbname>_db_password`
- Automatically gets a public schema with full privileges
- Can have additional schemas specified if needed

#### How It Works

1. **Database Creation**
   - Uses a temporary PostgreSQL client container
   - Connects as postgres superuser
   - Creates users, databases, and schemas
   - Sets proper ownership and privileges

2. **PgAdmin Web Interface**
   - Provides web-based database management at `pgadmin.<domain>`
   - Credentials configured in secrets.yml:
     - `vault_pgadmin_password`: For pgAdmin login
     - `vault_pgadmin_basic_auth_password`: For HTTP basic auth

#### Usage

To manage databases:
```bash
# Deploy pgAdmin and create/update databases
ansible-playbook playbooks/deploy.yml --tags pgadmin,db_setup

# Just deploy pgAdmin without database changes
ansible-playbook playbooks/deploy.yml --tags pgadmin

# Access web interface
https://pgadmin.<your-domain>
```

#### Security Notes

- Database passwords are stored in vault-encrypted secrets
- PgAdmin is protected by both application login and HTTP basic auth
- Database operations use temporary containers that are removed after use
