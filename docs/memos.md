---
title: Setting Up Memos with Docker Compose
description: Memos is a self-hosted note-taking application that offers a convenient way to organize and store personal notes, memos, and other pieces of information.
---

# Setting Up Memos with Docker Compose

!!! warning "Disable open registration for public instances"
    Memos allows open registration by default. If your instance is accessible from the internet, go to **Settings → System** and disable **Allow user registration** after creating your account.

## Introduction to Memos

Memos is a self-hosted note-taking application that offers a convenient way to organize and store personal notes, memos, and other pieces of information.

## Docker Compose Configuration for Memos

This Docker Compose setup deploys Memos in a Docker container, providing an easy-to-manage environment for your note-taking needs.

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  memos:
    image: neosmemo/memos:latest
    container_name: memos
    volumes:
      - ~/.memos/:/var/opt/memos
    ports:
      - 5230:5230
    restart: unless-stopped
```

## Key Components of the Configuration

### Service: Memos
- **Image**: `neosmemo/memos:latest` is the Docker image used for Memos.
- **Volumes**: 
  - `~/.memos/:/var/opt/memos` maps a local directory (`~/.memos/`) to the container's data storage directory (`/var/opt/memos`). This is where Memos stores its data.

!!! tip "Use an absolute path for the data volume"
    The `~/.memos/` path may behave unexpectedly with rootless Docker or systemd-managed services. Replace it with an absolute path, e.g. `/opt/memos/data:/var/opt/memos`.

- **Ports**: 
  - `5230:5230` maps port 5230 on the host to port 5230 in the container, where Memos's web interface is accessible.

### Restart Policy
- Not specified in the Compose file, but the default is `no` which means the container does not automatically restart. It's recommended to set a restart policy like `unless-stopped`.

## Deploying Memos

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Memos in detached mode.
3. Access Memos by navigating to `http://<host-ip>:5230`.

## Configuring and Using Memos

After deployment, you can start using Memos through its web interface for creating and managing your notes.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/sUGgA991uOg?si=HQxIRtKhdymfw8T-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
