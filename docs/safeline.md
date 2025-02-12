<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Deploying Safeline with Docker Compose
description: Safeline is a web application firewall that provides advanced protection against web threats. This guide provides steps for deploying Safeline using Docker Compose, setting up the required `.env` file, and breaking down the provided Compose configuration.
---

# Deploying Safeline with Docker Compose

## Introduction to Safeline

[Safeline](https://waf.chaitin.com/) is a powerful open-source web application firewall designed to protect web applications from a variety of security threats. This guide walks you through deploying Safeline using Docker Compose, configuring its environment file (`.env`), and running the required command to retrieve admin account login details after deployment.

## Directory Setup

Before deploying Safeline, you need to set up a directory to store its configuration and resources. Replace `<user>` with your actual system username.

```bash
mkdir -p /home/<user>/docker/safeline
cd /home/<user>/docker/safeline
```

For example, if your username is `techdox`:

```bash
mkdir -p /home/techdox/docker/safeline
cd /home/techdox/docker/safeline
```

## Fetching the Docker Compose File

Download the Safeline Docker Compose file:

```bash
wget "https://waf.chaitin.com/release/latest/compose.yaml"
```

This file does not need editing, but you must create a `.env` file for the deployment.

## `.env` File Configuration

Create a `.env` file in the same directory as the Compose file. Below is an example `.env` file:

```ini
SAFELINE_DIR=/home/<user>/docker/safeline
IMAGE_TAG=latest
MGT_PORT=9443
POSTGRES_PASSWORD=testing
SUBNET_PREFIX=172.22.222
IMAGE_PREFIX=chaitin
ARCH_SUFFIX=
RELEASE=
```

### Explanation of Variables

- **`SAFELINE_DIR`**: Path to the Safeline directory. Replace `<user>` with your username.
- **`IMAGE_TAG`**: Specifies the image version. Use `latest` for the most recent version.
- **`MGT_PORT`**: Port for the Safeline Management service.
- **`POSTGRES_PASSWORD`**: Password for the PostgreSQL database. Replace with a strong password.
- **`SUBNET_PREFIX`**: Subnet prefix for the Docker network. Adjust as needed to avoid conflicts with existing networks.
- **`IMAGE_PREFIX`**: Docker image prefix (default: `chaitin`).
- **`ARCH_SUFFIX`**: Architecture-specific suffix (leave empty for default).
- **`RELEASE`**: Release version (leave empty for stable).

## Docker Compose Configuration Breakdown

Below is a breakdown of key components in the Docker Compose file.

### Networks

```yaml
networks:
  safeline-ce:
    name: safeline-ce
    driver: bridge
    ipam:
      driver: default
      config:
        - gateway: ${SUBNET_PREFIX:?SUBNET_PREFIX required}.1
          subnet: ${SUBNET_PREFIX}.0/24
    driver_opts:
      com.docker.network.bridge.name: safeline-ce
```

- **`name`**: Defines the network name.
- **`driver`**: Specifies the bridge network driver.
- **`ipam`**: Configures IP allocation for the network.
  - **`gateway`**: The gateway address for the network.
  - **`subnet`**: Defines the subnet (e.g., `172.22.222.0/24`).
- **`driver_opts`**: Sets advanced driver options (e.g., bridge name).

### Services

#### PostgreSQL

```yaml
services:
  postgres:
    container_name: safeline-pg
    restart: always
    image: ${IMAGE_PREFIX}/safeline-postgres${ARCH_SUFFIX}:15.2
    volumes:
      - ${SAFELINE_DIR}/resources/postgres/data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=safeline-ce
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:?postgres password required}
    networks:
      safeline-ce:
        ipv4_address: ${SUBNET_PREFIX}.2
    command: [postgres, -c, max_connections=600]
    healthcheck:
      test: pg_isready -U safeline-ce -d safeline-ce
```

- **`POSTGRES_PASSWORD`**: Password for the database.
- **`volumes`**: Stores persistent PostgreSQL data.
- **`networks`**: Assigns the service a static IP address (`${SUBNET_PREFIX}.2`).

#### Management Service

```yaml
  mgt:
    container_name: safeline-mgt
    restart: always
    image: ${IMAGE_PREFIX}/safeline-mgt-g${ARCH_SUFFIX}${RELEASE}:${IMAGE_TAG:?image tag required}
    ports:
      - ${MGT_PORT:-9443}:1443
    volumes:
      - ${SAFELINE_DIR}/resources/mgt:/app/data
    healthcheck:
      test: curl -k -f https://localhost:1443/api/open/health
    depends_on:
      - postgres
      - fvm
    networks:
      safeline-ce:
        ipv4_address: ${SUBNET_PREFIX}.4
```

- **`ports`**: Exposes the management service on the host at port `9443` by default.
- **`depends_on`**: Ensures the `postgres` and `fvm` services start first.

#### Detector Service

```yaml
  detect:
    container_name: safeline-detector
    restart: always
    image: ${IMAGE_PREFIX}/safeline-detector-g${ARCH_SUFFIX}${RELEASE}:${IMAGE_TAG}
    volumes:
      - ${SAFELINE_DIR}/resources/detector:/resources/detector
    environment:
      - LOG_DIR=/logs/detector
    networks:
      safeline-ce:
        ipv4_address: ${SUBNET_PREFIX}.5
```

- **`volumes`**: Mounts logs and detector resources.

#### Other Services

- **`tengine`**: Handles traffic and communicates with `detector`.
- **`luigi`**: Supports management services.
- **`fvm`**: File version management.
- **`chaos`**: Adds chaos testing features.

## Deployment Steps

1. **Prepare the Directory and Files**:
   - Create the directory: `/home/<user>/docker/safeline`.
   - Create a `.env` file based on the example above.

2. **Fetch the Docker Compose File**:
   ```bash
   wget "https://waf.chaitin.com/release/latest/compose.yaml"
   ```

3. **Deploy Safeline**:
   ```bash
   docker compose up -d
   ```

4. **Retrieve Admin Login Details**:
   After deployment, run the following command to retrieve the admin account details:

   ```bash
   docker exec safeline-mgt resetadmin
   ```

   This command will display the admin username and password.

## Conclusion

By following this guide, you have successfully deployed Safeline using Docker Compose. You can now access the Safeline management service via the port specified in the `.env` file (default: `9443`).

---

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
