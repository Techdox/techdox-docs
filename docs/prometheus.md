<a href="https://my.racknerd.com/aff.php?aff=5792ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Setting Up Prometheus with Docker Compose
description: Prometheus is an open-source monitoring and alerting toolkit, widely used for its powerful querying language, efficient storage, and ease of integration with various metrics sources.
---

# Setting Up Prometheus with Docker Compose

## Introduction to Prometheus

Prometheus is an open-source monitoring and alerting toolkit, widely used for its powerful querying language, efficient storage, and ease of integration with various metrics sources.

## Docker Compose Configuration for Prometheus

This Docker Compose setup deploys Prometheus in a Docker container, along with a specified configuration file for custom monitoring settings.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'
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
volumes:
  prom_data:
```

## Prometheus Configuration File (`prometheus.yml`)

```yaml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s
alerting:
  alertmanagers:
    - static_configs:
      - targets: []
      scheme: http
      timeout: 10s
      api_version: v1
scrape_configs:
  - job_name: prometheus
    honor_timestamps: true
    scrape_interval: 15s
    scrape_timeout: 10s
    metrics_path: /metrics
    scheme: http
    static_configs:
      - targets:
        - localhost:9090
  - job_name: elzim # Change to whatever you like
    static_configs:
      - targets: ['192.168.68.109:9100'] #Change this to your server's IP
```

## Key Components of the Configuration
### Service: Prometheus
- **Image**: `prom/prometheus` is the Docker image used for Prometheus.
- **Command**: `--config.file=/etc/prometheus/prometheus.yml` specifies the configuration file used by Prometheus.
- **Ports**: 
  - `9090:9090` maps port 9090 on the host to port 9090 in the container, where Prometheus's web interface is accessible.
- **Volumes**: 
  - `./prometheus:/etc/prometheus` mounts the local Prometheus configuration directory to the container.
  - `prom_data:/prometheus` provides persistent storage for Prometheus data.
- **Restart Policy**: `unless-stopped` ensures that Prometheus restarts automatically unless explicitly stopped.

### Prometheus Configuration
- **Global Settings**: Defines the global scrape interval, timeout, and evaluation interval.
- **Alerting**: Configuration for alert managers.
- **Scrape Configs**: Defines the jobs and targets for Prometheus to scrape metrics from.

## Deploying Prometheus

1. Save the Docker Compose configuration in a `docker-compose.yml` file and the Prometheus configuration in a `prometheus.yml` file.
2. Run `docker compose up -d` to start Prometheus in detached mode.
3. Access Prometheus's web interface via `http://<host-ip>:9090`.

## Configuring and Using Prometheus

After deployment, you can modify the `prometheus.yml` file to add new targets and change scrape intervals as needed. Prometheus provides a versatile platform for monitoring your infrastructure.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
