---
title: Setting Up Syncthing with Docker Compose
description: Syncthing is an open-source continuous file synchronization program. It synchronizes files between two or more computers in real time, safely and efficiently.
---
# Setting Up Syncthing with Docker Compose

## Introduction to Syncthing

Syncthing is an open-source continuous file synchronization program. It synchronizes files between two or more computers in real time, safely and efficiently.

## Docker Compose Configuration for Syncthing

This Docker Compose setup deploys Syncthing in a Docker container, ensuring a secure and isolated environment for file synchronization.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "2.1"
services:
  syncthing:
    image: lscr.io/linuxserver/syncthing:latest
    container_name: syncthing
    hostname: syncthing #optional
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - /path/to/appdata/config:/config
      - /path/to/data1:/data1
      - /path/to/data2:/data2
    ports:
      - 8384:8384
      - 22000:22000/tcp
      - 22000:22000/udp
      - 21027:21027/udp
    restart: unless-stopped
```

## Key Components of the Configuration
### Environment Variables
- `PUID=1000` and `PGID=1000`: Sets user and group IDs for file permissions.
- `TZ=Etc/UTC`: Sets the container's timezone.

### Volumes
- `/path/to/appdata/config:/config`: Maps the local config directory to the container's config directory.
- `/path/to/data1:/data1`: Maps the first local data directory to the container.
- `/path/to/data2:/data2`: Maps the second local data directory to the container.

### Ports
- `8384:8384`: Web GUI.
- `22000:22000/tcp` and `22000:22000/udp`: Device communication.
- `21027:21027/udp`: Local network discovery.

### Restart Policy
- `unless-stopped`: Ensures the container restarts automatically unless explicitly stopped.


<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
