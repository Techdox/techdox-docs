---
title: Setting Up Jellyfin with Docker Compose
description: Jellyfin is a free and open-source media solution that allows you to organize, manage, and share your media files.
tags:
  - docker
  - media
---

# Setting Up Jellyfin with Docker Compose

## Introduction to Jellyfin

Jellyfin is a free and open-source media solution that allows you to organize, manage, and share your media files. It is an alternative to services like Plex or Emby, offering no subscription fees and a completely customizable and private experience.

## Docker Compose Configuration for Jellyfin

This Docker Compose setup deploys Jellyfin in a Docker container, ensuring a consistent and isolated environment. The configuration includes custom volume paths and environment settings.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "2.1"
services:
  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Pacific/Auckland
    volumes:
      - /home/server/jellyfin/library:/config
      - /home/server/jellyfin/tvseries:/data/tvshows
      - /home/server/jellyfin/movies:/data/movies
    ports:
      - 8096:8096
      - 8920:8920 #optional
      - 7359:7359/udp #optional
      - 1900:1900/udp #optional
    restart: unless-stopped
```

!!! tip "Set your timezone"
    Replace `Pacific/Auckland` with your own timezone. Find valid TZ identifiers at [Wikipedia's TZ database list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

## Key Components of the Configuration

### Environment Variables
- **PUID=1000 and PGID=1000**: Set user and group IDs for file permissions.
- **TZ=Pacific/Auckland**: Sets the container's timezone.

### Volumes
- **/home/server/jellyfin/library:/config**: Configuration and data storage.
- **/home/server/jellyfin/tvseries:/data/tvshows**: TV series library.
- **/home/server/jellyfin/movies:/data/movies**: Movies library.

### Ports
- **8096:8096**: Main access port for Jellyfin's web interface.
- **8920:8920**: Optional port for HTTPS access.
- **7359:7359/udp**: Optional port for live TV and DVR features.
- **1900:1900/udp**: Optional port for DLNA.

### Restart Policy
- **unless-stopped**: The container restarts automatically after a crash, except when it has been explicitly stopped.

## Deploying Jellyfin

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Jellyfin in detached mode.
3. Access Jellyfin's web interface via `http://<host-ip>:8096`.

## Configuring and Using Jellyfin

After navigating to `http://<your-server-ip>:8096`:

1. Complete the **setup wizard** — create an admin account and set your preferred language/metadata
2. Add your media libraries by pointing Jellyfin to the directories mounted in the compose file
3. Create additional user accounts under **Dashboard → Users** if needed
4. For hardware-accelerated transcoding, see **Dashboard → Playback** and enable your GPU's acceleration method (Intel QSV, NVIDIA NVENC, etc.)

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/BICNCAQRPbc?si=YVGT1UL7h_HRbqbi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Updating Jellyfin

```bash
docker compose pull
docker compose up -d
```

!!! tip "Back up before updating"
    Your data lives in the `/home/server/jellyfin/library`, `/home/server/jellyfin/tvseries`, and `/home/server/jellyfin/movies` host directories. Back these up before major version updates.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
