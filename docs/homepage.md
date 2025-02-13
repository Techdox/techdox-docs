---
title: Setting Up Homepage with Docker Compose
description: Homepage is a customizable start page or dashboard for your browser, designed to provide quick access to your frequently used websites, services, and tools.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Setting Up Homepage with Docker Compose

## Introduction to Homepage

Homepage is a customizable start page or dashboard for your browser, designed to provide quick access to your frequently used websites, services, and tools.

## Docker Compose Configuration for Homepage

This Docker Compose setup deploys the Homepage application in a Docker container, allowing you to have a personalized start page for your browsing experience.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "3.3"
services:
  homepage:
    image: ghcr.io/benphelps/homepage:latest
    container_name: homepage
    ports:
      - 3000:3000
    volumes:
      - ./config:/app/config # Make sure your local config directory exists
      - /var/run/docker.sock:/var/run/docker.sock:ro # (optional) For docker integrations
```

##Key Components of the Configuration
### Service: Homepage
- **Image**: `ghcr.io/benphelps/homepage:latest` is the Docker image used for Homepage.
- **Ports**: 
  - `3000:3000` maps port 3000 on the host to port 3000 in the container, where the Homepage web interface is accessible.
- **Volumes**: 
  - `./config:/app/config`: Maps a local configuration directory to the container's configuration directory.
  - `/var/run/docker.sock:/var/run/docker.sock:ro`: (Optional) Allows Homepage to integrate with Docker, provided read-only.

## Deploying Homepage

1. Ensure that the local `./config` directory exists and contains your configuration files.
2. Save the Docker Compose configuration in a `docker-compose.yml` file.
3. Run `docker compose up -d` to start Homepage in detached mode.
4. Access Homepage by navigating to `http://<host-ip>:3000`.

## Configuring and Using Homepage

After deployment, you can customize Homepage through the configuration files in your local `./config` directory. This allows you to personalize the start page with your preferred links and services.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/a5-4u0qFKaE?si=lRG-wceSVlKYPkUM" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
