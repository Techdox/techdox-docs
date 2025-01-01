---
title: Setting Up Filebrowser with Docker Compose
description: Filebrowser is a self-hosted file managing interface that allows you to manage files and directories through a web interface. It's a simple and convenient way to access, upload, and manage your files remotely.
---


# Setting Up Filebrowser with Docker Compose

## Introduction to Filebrowser

Filebrowser is a self-hosted file managing interface that allows you to manage files and directories through a web interface. It's a simple and convenient way to access, upload, and manage your files remotely.

## Docker Compose Configuration for Filebrowser

This Docker Compose setup deploys Filebrowser in a Docker container, providing an easy-to-use web interface for file management.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3'
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    volumes:
      - /home:/srv #Change to match your directory
      - /home/techdox/docker/filebrowser/filebrowser.db:/database/filebrowser.db #Change to match your directory
      - /home/techdox/docker/filebrowser/settings.json:/config/settings.json #Change to match your directory
    environment:
      - PUID=$(id -u)
      - PGID=$(id -g)
    ports:
      - 8095:80 #Change the port if needed
```

## Key Components of the Configuration
### Service: Filebrowser
- **Image**: `filebrowser/filebrowser:s6` is the Docker image used for Filebrowser.
- **Volumes**: 
  - `/home:/srv`: Maps a local directory to the server directory in the container.
  - `/home/techdox/docker/filebrowser/filebrowser.db:/database/filebrowser.db`: Persistent storage for Filebrowser's database.
  - `/home/techdox/docker/filebrowser/settings.json:/config/settings.json`: Stores configuration settings for Filebrowser.
- **Environment Variables**: 
  - `PUID=$(id -u)` and `PGID=$(id -g)`: Sets the user and group ID for file permissions.
- **Ports**: 
  - `8095:80`: Maps port 8095 on the host to port 80 in the container, where Filebrowser's web interface is accessible.

## Deploying Filebrowser

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Replace the volume paths with your actual directory paths.
3. Manually create the filebrowser.db and settings.json by running `touch filebrowser.db` `touch settings.json` in the compose directory, if you do not do this you will get permission errors.
3. Run `docker compose up -d` to start Filebrowser in detached mode.
4. Access Filebrowser by navigating to `http://<host-ip>:8095`.
5. Default login is `admin` `admin`
## Configuring and Using Filebrowser

After deployment, use the Filebrowser web interface to manage your files. You can upload, download, and organize files, as well as customize settings according to your needs.


## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/V6kHXWKwzn8?si=Fq1n_uyzK24v9VVx" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise a PR on [GitHub](https://github.com/Techdox/techdox-docs).
