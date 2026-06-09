---
title: Setting Up Uptime Kuma with Docker Compose
description: Uptime Kuma is a self-hosted monitoring tool similar to "Uptime Robot." It monitors your websites, services, and applications and provides uptime notifications.
---

# Setting Up Uptime Kuma with Docker Compose

## Introduction to Uptime Kuma

Uptime Kuma is a self-hosted monitoring tool similar to "Uptime Robot." It monitors your websites, services, and applications and provides uptime notifications.

## Docker Compose Configuration for Uptime Kuma

This Docker Compose setup deploys Uptime Kuma in a Docker container, providing a reliable environment for monitoring your services.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: always
    ports:
      - "3010:3001"
    volumes:
      - uptime-kuma:/app/data
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  uptime-kuma:
```

## Key Components of the Configuration

### Service: Uptime Kuma
- **Image**: `louislam/uptime-kuma:1` is the Docker image for Uptime Kuma.
- **Ports**: 
  - `3010:3001` maps port 3010 on the host to port 3001 in the container, where Uptime Kuma's web interface is accessible.
- **Volumes**: 
  - `uptime-kuma:/app/data` is used for persistent storage of Uptime Kuma data.
  - `/var/run/docker.sock:/var/run/docker.sock` allows Uptime Kuma to monitor Docker containers.
- **Restart Policy**: `always` ensures that Uptime Kuma restarts automatically after a crash or reboot.

## Deploying Uptime Kuma

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Uptime Kuma in detached mode.
3. Access Uptime Kuma's web interface via `http://<host-ip>:3010`.

## Configuring and Using Uptime Kuma

After deployment, you can configure Uptime Kuma through its web interface to monitor your websites and services, set up notifications, and track uptime and response times.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/mR6r8uIotyQ?si=_lF9mM4213LPLUdl" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
