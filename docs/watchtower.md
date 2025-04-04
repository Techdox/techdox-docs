---
title: Setting Up Watchtower with Docker Compose
description: Watchtower is an application that automatically updates your running Docker containers to the latest images. It monitors all containers and updates them in real-time whenever a new image is released.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Setting Up Watchtower with Docker Compose

## Introduction to Watchtower

Watchtower is an application that automatically updates your running Docker containers to the latest images. It monitors all containers and updates them in real-time whenever a new image is released.

## Docker Compose Configuration for Watchtower

This Docker Compose setup deploys Watchtower in a Docker container, ensuring your other containers are always up-to-date with the least amount of hassle.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3'
services:
  watchtower:
    image: containrrr/watchtower
    command:
      - --cleanup=true
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

## Key Components of the Configuration

### Image
- `containrrr/watchtower`: The Docker image used for Watchtower.

### Command
- `--cleanup=true`: Enables cleanup of old images after updating.

### Restart Policy
- `always`: Ensures the Watchtower container restarts automatically after a crash or reboot.

### Volumes
- `/var/run/docker.sock:/var/run/docker.sock`: Mounts the Docker socket so Watchtower can interact with the Docker daemon.

## Deploying Watchtower

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Watchtower in detached mode.

## How Watchtower Works

Once deployed, Watchtower automatically checks for updates to the images of all running containers at the specified interval. If a new image is found, Watchtower updates the container without downtime.

Remember to ensure that your containers are configured to handle updates gracefully!

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/DNfMuDLDq7k?si=QNVlRz2U0jnmseSQ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
