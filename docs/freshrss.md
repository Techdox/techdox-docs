<a href="https://my.racknerd.com/aff.php?aff=5792ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Setting Up FreshRSS with Docker Compose
description: FreshRSS is a self-hosted RSS feed aggregator. It is lightweight, easy to work with, and allows you to keep all your favorite news feeds and blogs organized in one place.
---


# Setting Up FreshRSS with Docker Compose

## Introduction to FreshRSS

FreshRSS is a self-hosted RSS feed aggregator. It is lightweight, easy to work with, and allows you to keep all your favorite news feeds and blogs organized in one place.

## Docker Compose Configuration for FreshRSS

This Docker Compose setup deploys FreshRSS in a Docker container, providing an isolated and efficient environment for managing your RSS feeds.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "2.1"
services:
  freshrss:
    image: lscr.io/linuxserver/freshrss:latest
    container_name: freshrss
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Etc/UTC
    volumes:
      - /path/to/data:/config 
    ports:
      - 80:80 
    restart: unless-stopped
```

## Key Components of the Configuration

### Environment Variables
- **PUID=1000 and PGID=1000**: Set user and group IDs for file permissions.
- **TZ=Etc/UTC**: Sets the container's timezone.

### Volumes
- **/path/to/data:/config**: Maps the local data directory to the container's configuration directory.

### Ports
- **80:80**: Maps port 80 of the host to port 80 of the container, allowing web access to FreshRSS.

### Restart Policy
- **unless-stopped**: Ensures the container restarts automatically unless explicitly stopped.

## Deploying FreshRSS

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Replace `/path/to/data` with your desired local directory path.
3. Run `docker compose up -d` to start FreshRSS in detached mode.
4. Access FreshRSS via `http://<host-ip>`.

## Configuring and Using FreshRSS

After deployment, access the FreshRSS web interface to configure your feeds, categories, and reading preferences. Ensure you manage user accounts and settings as required.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/W0jRuq4v810?si=7l-yHBnQ6g9TGFYm" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
