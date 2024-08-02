---
title: Setting Up Authentik with Docker Compose
description: Authentik is an open-source Identity Provider (IdP) designed to be flexible and versatile. It offers a robust solution for authentication, authorization, and federation, enabling secure access management across your applications.
---

# Setting Up Authentik with Docker Compose

!!! note
    This documentation is using the steps from the offical Authentik documentation, you can find it here [Authentik Installation with Docker Compose](https://goauthentik.io/docs/installation/docker-compose) This link provides additional details on configuration options and advanced setup instructions.

## Introduction to Authentik

Authentik is an open-source Identity Provider (IdP) designed to be flexible and versatile. It offers a robust solution for authentication, authorization, and federation, enabling secure access management across your applications.

## Prerequisites

Before you start the installation of Authentik with Docker Compose, make sure you meet the following prerequisites:

- **Docker** installed on your system (version 20.10.0 or higher recommended).
- **Docker Compose** installed (version 1.27.0 or higher recommended).
- Basic understanding of Docker and containerization concepts.
- Access to a terminal or command-line interface.
- (Optional) Basic knowledge of networking and email configuration for advanced setup options.

## Why Choose Authentik?

Authentik stands out as an open-source Identity Provider (IdP) for its flexibility, versatility, and comprehensive feature set. It's designed to cater to both small and large-scale deployments, offering:

- **Robust Authentication and Authorization**: Streamline access to your applications with support for various authentication methods.
- **Federation Capabilities**: Easily federate with other IdPs, expanding your authentication ecosystem.
- **User-friendly Interface**: Manage your authentication flows, users, and applications through a clean and intuitive dashboard.
- **Extensibility**: Customize Authentik to fit your specific needs with its flexible policy engine and extensive API.

## Security Best Practices

To ensure a secure Authentik deployment, consider the following best practices:

- **Use HTTPS**: Configure Authentik to serve content over HTTPS. For development purposes, Authentik can run over HTTP, but production deployments should always use HTTPS.
- **Secure Database Connection**: Ensure your database connections are secure and encrypted.
- **Regularly Update**: Keep Authentik, Docker, and all dependencies up to date to mitigate security vulnerabilities.


## Recommended Setup Steps for Authentik

To ensure a smooth and secure Authentik deployment, follow these recommended steps, which include preparation, environment configuration, and final startup.

### Preparation

1. **Download the Latest `docker-compose.yml`**:
   - Navigate to your preferred directory and download the official `docker-compose.yml`:
     ```shell
     wget https://goauthentik.io/docker-compose.yml
     ```

2. **Generate Password and Secret Key**:
   - Install `pwgen` for password generation (or use `openssl` as an alternative):
     ```shell
     sudo apt-get install -y pwgen
     ```
   - Generate and write a database password and Authentik secret key to your `.env` file:
     ```shell
     echo "PG_PASS=$(pwgen -s 40 1)" >> .env
     echo "AUTHENTIK_SECRET_KEY=$(pwgen -s 50 1)" >> .env
     ```

3. **Enable Error Reporting** (Optional):
   - To help diagnose issues, enable error reporting:
     ```shell
     echo "AUTHENTIK_ERROR_REPORTING__ENABLED=true" >> .env
     ```

### Email Configuration (Optional but Recommended)

Configuring global email credentials allows Authentik to send notifications and verification emails:

- Append the following block to your `.env` file, replacing placeholders with your SMTP details:
  ```shell
  AUTHENTIK_EMAIL__HOST=localhost
  AUTHENTIK_EMAIL__PORT=25
  AUTHENTIK_EMAIL__USERNAME=
  AUTHENTIK_EMAIL__PASSWORD=
  AUTHENTIK_EMAIL__USE_TLS=false
  AUTHENTIK_EMAIL__USE_SSL=false
  AUTHENTIK_EMAIL__TIMEOUT=10
  AUTHENTIK_EMAIL__FROM=authentik@localhost
  ```

### Configure for Ports 80/443

By default, authentik listens internally on port 9000 for HTTP and 9443 for HTTPS.

- To expose Authentik on standard web ports, adjust the port variables in your `.env` file:
  ```shell
  COMPOSE_PORT_HTTP=80
  COMPOSE_PORT_HTTPS=443
  ```
- Remember to run `docker compose up -d` after any changes to rebuild with the new settings.

### Startup and Final Steps

- **Important Note**: Authentik is designed to operate with its internal timezone set to UTC. Avoid altering timezone settings within the containers to prevent authentication issues.
- Start Authentik:
  ```shell
  docker compose pull
  docker compose up -d
  ```
To start the initial setup, navigate to http://your server's IP or hostname:9000/if/flow/initial-setup/.


## Post-Installation Steps

After successfully installing Authentik, consider the following next steps to enhance your setup:

1. **Configure Applications**: Add your applications to Authentik for centralized authentication management.
2. **Set Up Policies**: Define authentication policies for different applications and user groups.
3. **User Management**: Start adding users, either manually or through integrations with external directories.
4. **Audit and Logging**: Review Authentik's audit logs regularly to monitor access and identify potential security incidents.


By following these steps, you'll have Authentik up and running, ready to manage authentication and authorization for your applications securely.

## Docker Compose Breakdown

!!! note

    Don't use this compose file, this is just a break down of the file you downloaded and are using.

# Docker Compose Configuration for Authentik

## Docker Compose File (`docker-compose.yml`)

```yaml
version: "3.4"

services:
  postgresql:
    image: docker.io/library/postgres:12-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}"]
      start_period: 20s
      interval: 30s
      retries: 5
      timeout: 5s
    volumes:
      - database:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${PG_PASS:?database password required}
      POSTGRES_USER: ${PG_USER:-authentik}
      POSTGRES_DB: ${PG_DB:-authentik}
    env_file:
      - .env
  redis:
    image: docker.io/library/redis:alpine
    command: --save 60 1 --loglevel warning
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping | grep PONG"]
      start_period: 20s
      interval: 30s
      retries: 5
      timeout: 3s
    volumes:
      - redis:/data
  server:
    image: ${AUTHENTIK_IMAGE:-ghcr.io/goauthentik/server}:${AUTHENTIK_TAG:-2023.10.7}
    restart: unless-stopped
    command: server
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: ${PG_USER:-authentik}
      AUTHENTIK_POSTGRESQL__NAME: ${PG_DB:-authentik}
      AUTHENTIK_POSTGRESQL__PASSWORD: ${PG_PASS}
    volumes:
      - ./media:/media
      - ./custom-templates:/templates
    env_file:
      - .env
    ports:
      - "${COMPOSE_PORT_HTTP:-9000}:9000"
      - "${COMPOSE_PORT_HTTPS:-9443}:9443"
    depends_on:
      - postgresql
      - redis
  worker:
    image: ${AUTHENTIK_IMAGE:-ghcr.io/goauthentik/server}:${AUTHENTIK_TAG:-2023.10.7}
    restart: unless-stopped
    command: worker
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: ${PG_USER:-authentik}
      AUTHENTIK_POSTGRESQL__NAME: ${PG_DB:-authentik}
      AUTHENTIK_POSTGRESQL__PASSWORD: ${PG_PASS}
    user: root
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./media:/media
      - ./certs:/certs
      - ./custom-templates:/templates
    env_file:
      - .env
    depends_on:
      - postgresql
      - redis

volumes:
  database:
    driver: local
  redis:
    driver: local
```

## Key Components of the Configuration

### PostgreSQL Service
- **Image**: Uses PostgreSQL 12 on Alpine for the database.
- **Healthcheck**: Ensures the database is ready before other services start.
- **Environment**: Configures database credentials, which must be set in the `.env` file.

### Redis Service
- **Image**: Alpine-based Redis for caching.
- **Command & Healthcheck**: Configures Redis and checks its availability.

### Server Service
- **Image**: Specifies the Authentik server image and tag.
- **Ports**: Exposes Authentik on specified HTTP and HTTPS ports.
- **Volumes**: For media files and custom templates.
- **Environment**: Connects to Redis and PostgreSQL using credentials from `.env`.

### Worker Service
- **Image**: Utilizes the same image as the server for background tasks.
- **User**: Optionally runs as root to manage Docker integrations.
- **Volumes**: Similar to the server, for media, certificates, and templates.

### Volumes
- **Persistent Storage**: Defined for PostgreSQL (`database`) and Redis (`redis`).

## Notes
- **Environment Variables**: Required to be set in the `.env` file, including database credentials (`PG_PASS`, `PG_USER`, `PG_DB`) and optionally Authentik image version (`AUTHENTIK_IMAGE`, `AUTHENTIK_TAG`).
- **Manual Preparation**: Prior to deployment, manually create necessary directories for volumes to avoid permission issues.
- **App URL**: For public deployments, ensure the app URL is defined correctly to match  your domain or IP address.

