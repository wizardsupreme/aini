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

AINI can be run either via Docker (recommended) or directly on your system.

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/***REMOVED***.git
cd ***REMOVED***

# Create your environment file from the example
cp .env.example .env

# Edit the .env file and add your credentials
# Required variables to set:
# - HCLOUD_TOKEN (your Hetzner Cloud API token)
# - S3_ACCESS_KEY (if S3_ENABLED=true)
# - S3_SECRET_KEY (if S3_ENABLED=true)
# - S3_BUCKET (if S3_ENABLED=true)
# - S3_ENDPOINT (if S3_ENABLED=true)

# Start the infrastructure
docker compose up -d

# Initialize the infrastructure
docker compose exec control ansible-playbook ansible/playbooks/operations/init_infrastructure.yml -v

# Use AINI CLI
docker compose exec control ***REMOVED*** --help
```

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/***REMOVED***.git
cd ***REMOVED***

# Create and configure your environment
cp .env.example .env
# Edit .env with your credentials

# Install Ansible requirements
ansible-galaxy collection install -r ansible/requirements.yml

# Load environment variables
set -a; source .env; set +a

# Initialize the infrastructure
ansible-playbook ansible/playbooks/operations/init_infrastructure.yml -v

# Use AINI CLI directly
./cli/***REMOVED*** --help
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
docker-compose exec ***REMOVED***-control ***REMOVED*** status

# Start servers
docker-compose exec ***REMOVED***-control ***REMOVED*** start app  # Start application server
docker-compose exec ***REMOVED***-control ***REMOVED*** start gpu  # Start GPU server

# Stop servers
docker-compose exec ***REMOVED***-control ***REMOVED*** stop app
docker-compose exec ***REMOVED***-control ***REMOVED*** stop gpu

# Deploy services
docker-compose exec ***REMOVED***-control ***REMOVED*** deploy nextcloud
docker-compose exec ***REMOVED***-control ***REMOVED*** deploy ml-stack
```

### Configuration

All configuration is managed through Consul and persisted in Wasabi:

```bash
# Configure cloud provider
docker-compose exec ***REMOVED***-control ***REMOVED*** configure provider

# Configure storage
docker-compose exec ***REMOVED***-control ***REMOVED*** configure storage

# Configure services
docker-compose exec ***REMOVED***-control ***REMOVED*** configure services
```

### Monitoring & Dashboards

Access these interfaces through your **application server's** IP/DNS:

- **Consul Dashboard**: `http://<app-server-ip>:8500`
  - View and manage service configurations
  - Monitor service health
  - Access key-value store
  
- **Traefik Dashboard**: `http://<app-server-ip>:8080`
- **Netdata Monitoring**: `http://<app-server-ip>:19999`

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
docker-compose exec control ***REMOVED*** test
```

### Building Documentation
```bash
docker-compose exec control ***REMOVED*** docs build
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

## Troubleshooting

If you get "container not running" errors:

1. Verify the control container is running:
```bash
docker-compose ps
```

2. Check container logs:
```bash
docker-compose logs control
```

3. If needed, restart the stack:
```bash
docker-compose down && docker-compose up -d
```

## Dashboard

AINI provides a REST API for managing your infrastructure. The API is built with FastAPI and provides:
- Server status monitoring
- Server lifecycle management
- Infrastructure control endpoints

### API Endpoints

The API server runs on port 3000 and provides these endpoints:

```bash
GET /api/status              # Get infrastructure status
POST /api/start/{app|gpu}    # Start a server
POST /api/stop/{app|gpu}     # Stop a server
```

You can also access the auto-generated API documentation at:
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

### Running the API Server

The API server is automatically started when you run:
```bash
docker-compose up -d
```

### Testing the API

You can test the API using curl:

```bash
# Get status
curl http://localhost:3000/api/status

# Start app server
curl -X POST http://localhost:3000/api/start/app

# Stop app server
curl -X POST http://localhost:3000/api/stop/app

# Start GPU server
curl -X POST http://localhost:3000/api/start/gpu

# Stop GPU server
curl -X POST http://localhost:3000/api/stop/gpu
```

### Development

For API development:

1. Install Python dependencies:
```bash
pip install fastapi uvicorn
```

2. Run the API server in development mode:
```bash
python cli/api.py
```

The API will be available at `http://localhost:3000`