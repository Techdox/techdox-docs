---
title: Deploying Loki and Promtail with Docker Compose
description: Loki is a log aggregation system and Promtail is an agent that ships the logs to Loki. This guide details deploying Loki and Promtail using Docker Compose, including the steps to download necessary configuration files and set up additional hosts.
---

# Deploying Loki and Promtail with Docker Compose

## Introduction to Loki and Promtail

Loki is a log aggregation system that integrates seamlessly with Prometheus, and Promtail is an agent that ships the logs to Loki. This guide walks you through deploying Loki and Promtail using Docker Compose, including configuration, setup, and adding additional hosts.

## Docker Compose Configuration for Loki and Promtail

Here's how to set up Loki and Promtail using Docker Compose, explaining each component of the configuration.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  loki:
    image: grafana/loki:3.0.0                       # Specifies the Loki Docker image and version.
    container_name: loki                            # Names the container for easier management.
    volumes:
      - ./loki-config.yaml:/mnt/config/loki-config.yaml # Mounts the Loki configuration file.
      - ./data:/tmp
    ports:
      - "3100:3100"                                 # Maps port 3100 on the host to port 3100 in the container.
    command: -config.file=/mnt/config/loki-config.yaml # Runs Loki with the specified configuration file.

  promtail:
    image: grafana/promtail:3.0.0                   # Specifies the Promtail Docker image and version.
    container_name: promtail                        # Names the container for easier management.
    volumes:
      - ./promtail-config.yaml:/mnt/config/promtail-config.yaml # Mounts the Promtail configuration file.
      - /var/log:/var/log                           # Mounts the host's log directory.
    depends_on:
      - loki                                       # Ensures Promtail starts after Loki.
    command: -config.file=/mnt/config/promtail-config.yaml # Runs Promtail with the specified configuration file.
```

### Explanation of Key Components

- **Loki Service**:
  - **Image**: Specifies the Docker image for Loki, ensuring the correct version is used.
  - **Ports**: Exposes port `3100` on the host, which is used by Loki to receive and query logs.
  - **Volumes**: Mounts the Loki configuration file from the host to the container and a folder to saving the logs persistent
  - **Command**: Instructs Loki to use the specified configuration file.
  
- **Promtail Service**:
  - **Image**: Specifies the Docker image for Promtail.
  - **Volumes**: Mounts the Promtail configuration file and the host's log directory.
  - **Depends_on**: Ensures Promtail starts only after Loki is up and running.
  - **Command**: Instructs Promtail to use the specified configuration file.

## Preparing for Deployment

Before deploying, you need to download the necessary configuration files for Loki and Promtail:

```bash
wget https://raw.githubusercontent.com/grafana/loki/v3.0.0/cmd/loki/loki-local-config.yaml -O loki-config.yaml
wget https://raw.githubusercontent.com/grafana/loki/v3.0.0/clients/cmd/promtail/promtail-docker-config.yaml -O promtail-config.yaml
```

These commands download the configuration files and rename them appropriately for use in your Docker Compose setup.

## Deployment

To deploy Loki and Promtail, navigate to the directory containing your `docker-compose.yml` and run:

```bash
docker compose up -d
```

This command starts the Loki and Promtail services in detached mode, running in the background.

## Adding Additional Hosts with Promtail

To add additional hosts for log shipping with Promtail, you can use the following steps:

1. Deploy Promtail on the additional host with the following `docker-compose.yml`:

    ```yaml
    version: '3.8'

    services:
      promtail:
        image: grafana/promtail:3.0.0
        container_name: promtail
        volumes:
          - ./promtail-config.yaml:/mnt/config/promtail-config.yaml
          - /var/log:/var/log
        command: -config.file=/mnt/config/promtail-config.yaml
    ```

2. Make sure to update the `promtail-config.yaml` on the additional host to point to the Loki instance's IP address.

## Conclusion

Deploying Loki and Promtail with Docker Compose allows for an efficient log aggregation and monitoring setup. By following the steps above, you can ensure your logs are managed effectively across multiple hosts in your self-hosted environment.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
