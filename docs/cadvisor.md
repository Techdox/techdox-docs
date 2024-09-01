---
title: Deploying cAdvisor with Docker Compose
description: cAdvisor (Container Advisor) is a tool that provides insights into the resource usage and performance characteristics of running containers. This guide details deploying cAdvisor alongside Prometheus and Redis using Docker Compose, including setup instructions for monitoring container metrics.
---

# Deploying cAdvisor with Docker Compose

## Introduction to cAdvisor

cAdvisor (Container Advisor) is a tool developed by Google that provides real-time monitoring of resource usage and performance characteristics for running containers. It collects, aggregates, processes, and exports information about running containers, which can be used by Prometheus for monitoring.

In this guide, we'll walk through deploying cAdvisor using Docker Compose, along with Prometheus and Redis for a complete monitoring setup. If you already have Prometheus running, you can add cAdvisor and Redis services to your existing setup.

> **Note:** For more detailed information on deploying Prometheus, please refer to the [Prometheus deployment guide](https://docs.techdox.nz/prometheus/). This guide will focus primarily on setting up cAdvisor.
> 
> If you already have Prometheus installed, click [here](https://docs.techdox.nz/cadvisor/#adding-cadvisor-to-an-existing-prometheus-setup) to jump to the section on adding cAdvisor to your existing setup.


## Docker Compose Configuration for cAdvisor

Here's how to set up cAdvisor using Docker Compose, including Prometheus and Redis, to monitor container metrics.

### Complete Docker Compose File (`docker-compose.yml`)

Below is an example of a complete deployment with Prometheus, cAdvisor, and Redis:

```yaml
services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    ports:
      - 9090:9090
    restart: unless-stopped
    volumes:
      - ./prometheus:/etc/prometheus
      - prom_data:/prometheus
    depends_on:
    - cadvisor
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
    - 8083:8080
    volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:rw
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
    depends_on:
    - redis
  redis:
    image: redis:latest
    container_name: redis
    ports:
    - 6379:6379

volumes:
  prom_data:                                    # Exposes Redis on port 6379.
```

### Explanation of Key Components

- **Prometheus Service**:
  - **Image**: Specifies the Docker image for Prometheus.
  - **Ports**: Exposes Prometheus on port `9090` for web access and data scraping.
  - **Volumes**: Mounts the Prometheus configuration file (`prometheus.yml`).
  - **Depends_on**: Ensures Prometheus starts after cAdvisor to ensure metrics are available.

- **cAdvisor Service**:
  - **Image**: Specifies the Docker image for cAdvisor.
  - **Ports**: Exposes cAdvisor on port `8080` for accessing metrics and monitoring data.
  - **Volumes**: Mounts necessary directories for cAdvisor to access container runtime information.
  - **Depends_on**: Ensures cAdvisor starts after Redis, which it uses for caching and storing data.

- **Redis Service**:
  - **Image**: Specifies the Docker image for Redis, used for caching and supporting cAdvisor.
  - **Ports**: Exposes Redis on port `6379` for use by cAdvisor.

## Modifying the Prometheus Configuration

To have Prometheus scrape metrics from cAdvisor, you'll need to add the following `scrape_configs` section to your Prometheus configuration file (`prometheus.yml`):

```yaml
scrape_configs:
  - job_name: cadvisor
    scrape_interval: 5s
    static_configs:
      - targets:
        - cadvisor:8080 #IP:Port of your Host running cAdvisor
```

This configuration tells Prometheus to scrape metrics from cAdvisor every 5 seconds.

### Updating `prometheus.yml`

1. **Edit your `prometheus.yml`** file to include the above `scrape_configs`:

    ```yaml
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    scrape_configs:
      - job_name: 'prometheus'
        static_configs:
          - targets: ['localhost:9090']

      - job_name: cadvisor
        scrape_interval: 5s
        static_configs:
          - targets:
            - cadvisor:8080
    ```

2. **Restart Prometheus** to apply the changes:

    ```bash
    docker compose restart prometheus
    ```

## Adding cAdvisor to an Existing Prometheus Setup

If you already have Prometheus running, you can simply add the cAdvisor and Redis services to your existing `docker-compose.yml`:

```yaml
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    ports:
      - 8080:8080
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:rw
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    depends_on:
      - redis

  redis:
    image: redis:latest
    container_name: redis
    ports:
      - 6379:6379
```

After updating your `docker-compose.yml`, redeploy your services:

```bash
docker compose up -d
```

## Conclusion

Deploying cAdvisor with Docker Compose, alongside Prometheus and Redis, allows for comprehensive monitoring of containerized applications. Whether you're starting from scratch or adding cAdvisor to an existing setup, this guide provides the steps needed to get your monitoring environment up and running quickly.

For more detailed information on deploying Prometheus, please refer to the [Prometheus deployment guide](https://docs.techdox.nz/prometheus/).

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
