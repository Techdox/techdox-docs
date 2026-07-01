---
title: Setting Up Dockge with Docker
description: Dockge is a self-hosted, reactive Docker stack manager, offering an easy-to-use interface for managing Docker containers and compose stacks. It's created by the same developer as Uptime-Kuma.
tags:
  - docker
  - docker-management
---

# Setting Up Dockge with Docker

## Introduction to Dockge

Dockge is a self-hosted, reactive Docker stack manager, offering an easy-to-use interface for managing Docker containers and compose stacks. It's created by the same developer as Uptime-Kuma.

## Recommended Docker Compose Setup for Dockge

Instead of directly using the setup from the project page, the following steps are recommended for a smoother setup experience:

1. **Create Dockge Directory**:
    Navigate to the directory where you keep your Docker containers. For example, if you store them in `~/Docker`, the commands would be:
     ```bash
     cd ~/Docker
     mkdir dockge && cd dockge
     ```

2. **Link Your Containers Directory**:
    Check if `/opt/stacks` exists, and if not, create and link it to your containers' location:
     ```bash
     ls /opt/stacks # Check if it exists
     sudo mkdir -p /opt/stacks
     sudo ln -s <path-to-your-containers> /opt/stacks
     # Example: sudo ln -s /Users/<username>/Docker /opt/stacks
     # Do not use ~/ in the above command
     ```
   Replace `<path-to-your-containers>` with the actual path to your Docker containers.

3. **Download and Start Dockge**:
   Download the `compose.yaml` file and start the Dockge service:
     ```bash
     curl https://raw.githubusercontent.com/louislam/dockge/master/compose.yaml --output compose.yaml
     ```
   Then start the stack:
   ```bash
   docker compose up -d
   ```

### Docker Compose File (`docker-compose.yml`)

Here's an example `docker-compose.yml` file for Dockge:

```yaml
services:
  dockge:
    image: louislam/dockge:latest
    restart: unless-stopped
    ports:
      - 5005:5001
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data:/app/data
      - /opt/stacks:/opt/stacks
    environment:
      - DOCKGE_STACKS_DIR=/opt/stacks
      # Uncomment the line below to re-enable the built-in terminal (disabled by default since v1.5)
      # - DOCKGE_ENABLE_CONSOLE=true
```

## Key Components of the Configuration
### Service: Dockge
- **Image**: `louislam/dockge:latest` is the Docker image used for Dockge.
- **Ports**: 
  - `5005:5001` maps port 5005 on the host to port 5001 in the container, where Dockge's web interface is accessible.
- **Volumes**: 
  - `/var/run/docker.sock:/var/run/docker.sock` allows Dockge to interact with the Docker daemon.
  - `./data:/app/data` provides persistent storage for Dockge's data.
  - `/opt/stacks:/opt/stacks` maps a local directory for Docker stacks.
- **Environment Variables**:
  - `DOCKGE_STACKS_DIR=/opt/stacks` sets the directory path for Docker stacks within Dockge.
  - `DOCKGE_ENABLE_CONSOLE=true` re-enables the built-in terminal, which is **disabled by default since v1.5** for security reasons.

## Deploying Dockge

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Dockge in detached mode.
3. Access Dockge's web interface by navigating to `http://<host-ip>:5005`.

## Configuring and Using Dockge

After deployment, use the Dockge web interface to manage your Docker containers, images, and stacks. The interface provides tools for monitoring, starting, stopping, and removing Docker components.

## Updating Dockge

```bash
docker compose pull
docker compose up -d
```

!!! tip "Back up before updating"
    Your data lives in the `./data` directory (Dockge's application data) and the `/opt/stacks` directory (your compose stacks). Back these up before major version updates.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/ephiayS50jM?si=oK3z6ogKzxRRqC9D" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Acknowledgments

**Shoutout to Archigos** for their awesome tips and insights that helped shape this guide! 🌟

---


<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
