# AINI - AI Infrastructure Management Tool

AINI provides automated deployment of AI and productivity infrastructure using Docker and Ansible.

## Features

- Automated server provisioning on Hetzner Cloud
- Complete application stack:
  - Traefik (reverse proxy + SSL)
  - LibreChat (AI frontend)
  - N8N (workflow automation)
  - Consul + Vault (configuration/secrets)
  - Nextcloud + OnlyOffice (file storage/editing)
  - Netdata (monitoring)
  - Watchtower (automatic updates)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/***REMOVED***.git
cd ***REMOVED***
```

2. Copy and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start the infrastructure:
```bash
# Initialize Hetzner server
ansible-playbook ansible/playbooks/operations/init_infrastructure.yml

# Deploy application stack
ansible-playbook ansible/playbooks/configure/apps.yml
```

## Directory Structure

```
***REMOVED***/
├── ansible/
│   ├── inventory/                # Server inventory
│   │   ├── group_vars/          # Group variables
│   │   │   ├── all.yml
│   │   │   ├── app_servers.yml
│   │   │   └── gpu_servers.yml
│   │   └── hosts.yml
│   ├── playbooks/
│   │   ├── configure/           # Service configuration
│   │   │   ├── apps.yml        # Application stack setup
│   │   │   ├── base.yml        # Base configuration
│   │   │   └── ml.yml          # ML stack setup
│   │   ├── operations/         # Server operations
│   │   │   ├── backup.yml
│   │   │   ├── init_infrastructure.yml
│   │   │   ├── start.yml
│   │   │   └── stop.yml
│   │   └── provision/          # Server provisioning
│   │       ├── app_servers.yml
│   │       └── gpu_servers.yml
│   └── roles/                  # Ansible roles
├── docker/                     # Docker configurations
│   ├── traefik/               # Traefik configuration
│   ├── nextcloud/             # Nextcloud configuration
│   ├── vault/                 # Vault configuration
│   └── consul/                # Consul configuration
├── docs/                      # Documentation
│   ├── architecture.md        # System architecture
│   └── development.md         # Development guide
├── tests/                     # Test scripts
├── scripts/                   # Utility scripts
├── docker-compose.yml         # Main stack definition
├── .env.example              # Environment template
└── README.md                 # This file
```

## Configuration

Required environment variables:
- `HCLOUD_TOKEN`: Hetzner Cloud API token
- `DOMAIN`: Your domain name
- `ACME_EMAIL`: Email for Let's Encrypt
- Service credentials (see .env.example)

## Development

1. Install dependencies:
```bash
pip install -r requirements.txt
ansible-galaxy install -r ansible/requirements.yml
```

2. Run tests:
```bash
pytest tests/
```

## Documentation

- [Architecture](docs/architecture.md) - System components and design
- [Development](docs/development.md) - Development guide

## License

MIT