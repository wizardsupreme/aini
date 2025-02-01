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

3. Provision servers:
```bash
# For application servers
ansible-playbook ansible/playbooks/provision/app_servers.yml

# For GPU servers
ansible-playbook ansible/playbooks/provision/gpu_servers.yml
```

## Directory Structure

```
***REMOVED***/
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