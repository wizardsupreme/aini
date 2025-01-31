# AINI Architecture

## System Overview

AINI is an infrastructure management system that automates the deployment of AI and productivity tools. It uses Hetzner Cloud for hosting and implements a containerized microservices architecture.

## System Architecture

```mermaid
graph TB
    subgraph Internet
        User((User))
        DNS[DNS]
    end

    subgraph HetznerCloud[Hetzner Cloud]
        subgraph Server[Application Server]
            subgraph ReverseProxy[Reverse Proxy Layer]
                Traefik[Traefik]
            end

            subgraph CoreServices[Core Services]
                Consul[Consul]
                Vault[Vault]
            end

            subgraph Applications[Application Layer]
                subgraph AI[AI Services]
                    LibreChat[LibreChat]
                    N8N[N8N]
                end

                subgraph Storage[Storage Services]
                    Nextcloud[Nextcloud]
                    OnlyOffice[OnlyOffice]
                    MariaDB[(MariaDB)]
                end

                subgraph Monitoring[Monitoring Services]
                    Netdata[Netdata]
                    Watchtower[Watchtower]
                end
            end

            subgraph Data[Data Layer]
                Volumes[(Docker Volumes)]
                MongoDB[(MongoDB)]
            end
        end

        S3[(Hetzner S3)]
    end

    %% External Connections
    User --> DNS
    DNS --> Traefik

    %% Traefik Connections
    Traefik --> LibreChat
    Traefik --> N8N
    Traefik --> Nextcloud
    Traefik --> OnlyOffice
    Traefik --> Consul
    Traefik --> Vault
    Traefik --> Netdata

    %% Core Service Dependencies
    LibreChat --> MongoDB
    LibreChat --> Vault
    N8N --> Vault
    Nextcloud --> MariaDB
    Nextcloud --> OnlyOffice
    Nextcloud --> S3
    OnlyOffice --> Volumes

    %% Monitoring
    Netdata -.-> LibreChat
    Netdata -.-> N8N
    Netdata -.-> Nextcloud
    Watchtower -.-> LibreChat
    Watchtower -.-> N8N
    Watchtower -.-> Nextcloud

    %% State Management
    Consul --> Vault
    Applications --> Consul
    Applications --> Vault

    %% Styling
    classDef proxy fill:#f9f,stroke:#333,stroke-width:2px
    classDef service fill:#bbf,stroke:#333,stroke-width:1px
    classDef storage fill:#fda,stroke:#333,stroke-width:1px
    classDef monitor fill:#bfb,stroke:#333,stroke-width:1px
    classDef data fill:#feb,stroke:#333,stroke-width:1px

    class Traefik proxy
    class LibreChat,N8N,Nextcloud,OnlyOffice,Consul,Vault service
    class S3,Volumes,MongoDB,MariaDB storage
    class Netdata,Watchtower monitor
```

## Core Components

### Infrastructure Layer

1. **Hetzner Cloud Server**
   - Primary application server (configurable size)
   - Managed through Hetzner Cloud API
   - Provisioned using Ansible playbooks

2. **Docker + Docker Compose**
   - Container runtime
   - Service orchestration
   - Volume management

3. **Traefik**
   - Reverse proxy
   - SSL/TLS termination
   - Automatic certificate management
   - Service discovery

### State Management

1. **Consul**
   - Service discovery
   - Key-value store
   - Health checking
   - Configuration storage

2. **Vault**
   - Secrets management
   - API key storage
   - Credentials management
   - Encryption as a service

### Application Stack

1. **LibreChat**
   - AI chat interface
   - MongoDB backend
   - API integration capabilities

2. **N8N**
   - Workflow automation
   - AI agent orchestration
   - API integrations
   - Persistent workflow storage

3. **Nextcloud + OnlyOffice**
   - File storage and synchronization
   - Document editing
   - MariaDB backend
   - S3/Volume storage backend

4. **Supporting Services**
   - Netdata: System monitoring
   - Watchtower: Automatic updates

## Data Flow

1. **External Access**
   ```
   Internet -> Traefik -> Service
   ```

2. **Configuration Flow**
   ```
   Ansible -> Consul -> Services
   ```

3. **Secrets Flow**
   ```
   Vault -> Services (via API)
   ```

## Storage Architecture

1. **Local Storage**
   - Docker volumes for service data
   - Container filesystem for applications

2. **Remote Storage**
   - Hetzner S3 for Nextcloud backend (optional)
   - Hetzner Volumes for persistent storage (optional)

## Security Model

1. **Network Security**
   - Traefik handles SSL/TLS
   - Internal Docker network for inter-service communication
   - External access only through Traefik

2. **Authentication**
   - Basic auth for admin interfaces
   - OAuth2 for user services (where applicable)
   - API tokens managed by Vault

3. **Updates**
   - Automated through Watchtower
   - Configurable update schedules

## Deployment Process

1. **Server Provisioning**
   ```
   Ansible -> Hetzner API -> Server Creation
   ```

2. **Service Deployment**
   ```
   Ansible -> Docker Compose -> Service Startup
   ```

3. **Configuration**
   ```
   .env -> Docker Compose -> Services
   Consul -> Service Configuration
   ```

## Management Interfaces

1. **Infrastructure**
   - Traefik Dashboard: `traefik.domain.com`
   - Netdata: `netdata.domain.com`

2. **Services**
   - LibreChat: `chat.domain.com`
   - N8N: `n8n.domain.com`
   - Nextcloud: `cloud.domain.com`
   - OnlyOffice: `office.domain.com`

3. **Configuration**
   - Consul UI: `consul.domain.com`
   - Vault UI: `vault.domain.com`

## Development Setup

1. **Local Development**
   - Docker Compose for local stack
   - .env file for configuration
   - Local volume mounts

2. **Testing**
   - Pytest for Python components
   - Molecule for Ansible roles
   - Docker Compose for integration tests

## Backup Strategy

1. **Data Backups**
   - Service-specific backup procedures
   - Volume snapshots
   - S3 backups for Nextcloud

2. **Configuration Backups**
   - Consul state backups
   - Vault secrets backups
   - Docker volume backups