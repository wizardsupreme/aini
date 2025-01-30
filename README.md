# AINI (AI Nomad Infrastructure)

AINI is an open-source infrastructure management system designed for AI development teams who need flexible, cost-efficient cloud resources. It enables you to spin up and down both application and GPU servers as needed, maint***REMOVED***ng configurations and data while only paying for actual usage.

<img src="assets/logo.svg" alt="AINI Logo" width="200"/>

## Logo Design

The AINI logo represents the core concepts of our infrastructure management system:

- **Circular Path**: The dashed circular outline represents the nomadic and flexible nature of the infrastructure, suggesting movement and adaptability.

- **Network Nodes**: The four colored nodes symbolize different aspects of the infrastructure:
  - Blue Node: Reliability and stability of the system
  - Green Node: Sustainability and resource efficiency
  - Orange Node: Adaptability and flexibility
  - Red Node: Processing power and performance

- **Connecting Lines**: The lines between nodes represent the interconnected nature of the infrastructure components and seamless communication between services.

- **Central AI Emblem**: The "Ai" at the center emphasizes our focus on AI infrastructure, presented in a clean, modern style.

The color scheme was chosen to reflect both professionalism and innovation, with a dark slate base representing enterprise-grade reliability.

## Why AINI?

- **Cost Optimization**: Pay only for the infrastructure you use, when you use it
- **AI-Ready**: Pre-configured for both application hosting and GPU-accelerated workloads
- **Provider Flexible**: Not locked into any specific cloud provider
- **State Persistent**: Maintains configurations and data between server lifecycles
- **Production Ready**: Built on battle-tested tools (Ansible, Docker, Consul)

## Quick Start

The fastest way to get started with AINI is using Docker:

```bash
# Clone the repository
git clone https://github.com/yourusername/***REMOVED***.git
cd ***REMOVED***

# Configure your credentials
cat > .env << EOL
WASABI_ACCESS_KEY=your_key
WASABI_SECRET_KEY=your_secret
WASABI_BUCKET=your_bucket
HCLOUD_TOKEN=your_hetzner_token
EOL

# Start AINI
docker compose up -d

# Use AINI CLI
docker exec ***REMOVED***-control ***REMOVED*** --help
```

## Infrastructure Components

AINI manages two types of servers:

### Application Server
- Service hosting:
  - Traefik (reverse proxy)
  - Nextcloud + OnlyOffice
  - n8n (automation)
  - LibreChat
  - Netdata (monitoring)
  - Watchtower (updates)

### GPU Server
- ML model deployment
- GPU resource management
- Performance monitoring
- Model artifact storage

## Usage

### Basic Commands

```bash
# View status
docker exec ***REMOVED***-control ***REMOVED*** status

# Start servers
docker exec ***REMOVED***-control ***REMOVED*** start app  # Start application server
docker exec ***REMOVED***-control ***REMOVED*** start gpu  # Start GPU server

# Stop servers
docker exec ***REMOVED***-control ***REMOVED*** stop app
docker exec ***REMOVED***-control ***REMOVED*** stop gpu

# Deploy services
docker exec ***REMOVED***-control ***REMOVED*** deploy nextcloud
docker exec ***REMOVED***-control ***REMOVED*** deploy ml-stack
```

### Configuration

All configuration is managed through Consul and persisted in Wasabi:

```bash
# Configure cloud provider
docker exec ***REMOVED***-control ***REMOVED*** configure provider

# Configure storage
docker exec ***REMOVED***-control ***REMOVED*** configure storage

# Configure services
docker exec ***REMOVED***-control ***REMOVED*** configure services
```

## Project Structure

```
***REMOVED***/
├── ansible/                   # Infrastructure automation
│   ├── inventory/            # Server inventory
│   ├── playbooks/           # Management playbooks
│   └── roles/               # Service roles
├── assets/                   # Project assets
│   └── logo.svg             # AINI logo
├── docker/                   # Service definitions
│   ├── app_services/        # Application services
│   └── ml_services/         # ML/GPU services
├── cli/                      # AINI CLI tool
├── docker-compose.yml        # Local development setup
└── docs/                     # Documentation
```

## Manual Installation

If you prefer not to use Docker, you can install AINI directly:

### Prerequisites
- Python 3.11+
- Ansible 2.12+
- Docker and Docker Compose
- SSH client

### Installation Steps
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Ansible requirements
ansible-galaxy install -r ansible/requirements.yml

# Add CLI to path
export PATH="$PATH:$(pwd)/cli"
```

## Features

### Core Features
- Server lifecycle management
- Configuration persistence
- Automated backups
- Cost optimization
- Multi-provider support
- GPU resource management

### Application Stack
- Full application hosting platform
- Integrated monitoring
- Automatic updates
- SSL/TLS management

### ML Stack
- CUDA setup
- Model deployment
- Resource monitoring
- Artifact management

## CLI Reference

```bash
***REMOVED*** COMMAND [OPTIONS]

Commands:
  init         Initialize AINI infrastructure
  configure    Configure providers and services
  start        Start servers (app|gpu)
  stop         Stop servers (app|gpu)
  deploy       Deploy specific services
  status       Check infrastructure status
  backup       Manage backups
  logs         View service logs
```

## Development

### Running Tests
```bash
docker exec ***REMOVED***-control ***REMOVED*** test
```

### Building Documentation
```bash
docker exec ***REMOVED***-control ***REMOVED*** docs build
```

### Local Development Setup
```bash
docker compose -f docker-compose.dev.yml up
```

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

- Secrets management via Consul
- HTTPS enforcement
- Regular security updates
- Minimal attack surface

## Support

- Documentation: [docs/](docs/)
- Issues: GitHub Issue Tracker
- Discussions: GitHub Discussions
- Wiki: Project Wiki

## License

MIT

---

**Note**: AINI is under active development. Features and APIs may change.