---
title: Setting Up Pairdrop with Docker Compose
description: Pairdrop is an application designed for simple and secure file sharing. It's a self-hosted solution that allows easy file transfers within a network.
tags:
  - docker
  - file-management
---

# Setting Up Pairdrop with Docker Compose

## Introduction to Pairdrop

Pairdrop is an application designed for simple and secure file sharing. It's a self-hosted solution that allows easy file transfers within a network.

## Docker Compose Configuration for Pairdrop

This Docker Compose setup deploys Pairdrop in a Docker container, providing a secure and isolated environment for file sharing.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "2.1"
services:
  pairdrop:
    image: lscr.io/linuxserver/pairdrop:latest
    container_name: pairdrop
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
      - RATE_LIMIT=false #optional
      - WS_FALLBACK=false #optional
      - RTC_CONFIG= #optional
      - DEBUG_MODE=false #optional
    ports:
      - 3000:3000
    restart: unless-stopped
```

## Key Components of the Configuration
### Environment Variables
- `PUID=1000` and `PGID=1000`: Sets user and group IDs for file permissions.
- `TZ=Etc/UTC`: Configures the container's timezone.
- `RATE_LIMIT=false`: (Optional) Disables rate limiting.
- `WS_FALLBACK=false`: (Optional) Disables WebSocket fallback.
- `RTC_CONFIG`: (Optional) WebRTC configuration.
- `DEBUG_MODE=false`: (Optional) Disables debug mode.

### Ports
- `3000:3000`: Maps port 3000 of the host to port 3000 of the container, enabling web access to Pairdrop.

### Restart Policy
- `unless-stopped`: Ensures the container restarts automatically unless explicitly stopped.

## Deploying Pairdrop

```bash
docker compose up -d
```

Once running, open `http://<your-server-ip>:3000` in a browser on each device you want to transfer files between. Both devices must be on the **same subnet** for automatic peer discovery to work.

!!! note "Cross-network transfers"
    If devices are on different VLANs or networks, set the `RTC_CONFIG` environment variable to point to a TURN server for relayed connections.

## Updating Pairdrop

```bash
docker compose pull
docker compose up -d
```

!!! tip "Back up before updating"
    This compose file defines no persistent volumes — Pairdrop transfers files directly between devices and stores no data on disk, so there is nothing to back up before updating.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
