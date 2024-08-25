---
title: Setting Up Grafana with Docker Compose
description: Grafana is an open-source platform for monitoring and observability. It allows you to query, visualize, alert on, and understand your metrics no matter where they are stored.
---

# Setting Up Grafana with Docker Compose

## Introduction to Grafana

Grafana is an open-source platform for monitoring and observability. It allows you to query, visualize, alert on, and understand your metrics no matter where they are stored.

## Docker Compose Configuration for Grafana

This Docker Compose setup deploys Grafana in a Docker container, providing a powerful and flexible way to visualize and analyze your data.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "3.8"
services:
  grafana:
    image: grafana/grafana
    container_name: grafana
    restart: unless-stopped
    ports:
     - '3000:3000'
    volumes:
      - grafana-storage:/var/lib/grafana
volumes:
  grafana-storage: {}
```

## Key Components of the Configuration
### Service: Grafana
- **Image**: `grafana/grafana` is the Docker image used for Grafana.
- **Ports**: 
  - `3000:3000` maps port 3000 on the host to port 3000 in the container, where Grafana's web interface is accessible.
- **Volumes**: 
  - `grafana-storage:/var/lib/grafana` provides persistent storage for Grafana's data.
- **Restart Policy**: `unless-stopped` ensures that the Grafana service restarts automatically unless explicitly stopped.

## Deploying Grafana

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Grafana in detached mode.
3. Access Grafana by navigating to `http://<host-ip>:3000`.

## Configuring and Using Grafana

After deployment, configure Grafana through its web interface to connect to your data sources, create dashboards, and set up alerts.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/yrscZ-kGc_Y?si=ORwd_C8lWCfw6tfT" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
