---
title: Setting Up Excalidraw with Docker Compose
description: Excalidraw is a virtual collaborative whiteboard tool that lets you easily sketch diagrams with a hand-drawn feel. It's designed to be simple, intuitive, and to allow rapid collaboration.
---

# Setting Up Excalidraw with Docker Compose

## Introduction to Excalidraw

Excalidraw is a virtual collaborative whiteboard tool that lets you easily sketch diagrams with a hand-drawn feel. It's designed to be simple, intuitive, and to allow rapid collaboration.

## Docker Compose Configuration for Excalidraw

This Docker Compose setup deploys Excalidraw in a Docker container, offering an isolated environment for your sketching and collaboration needs.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "3.8"

services:
  excalidraw:
    container_name: excalidraw
    image: excalidraw/excalidraw:latest
    ports:
      - "3030:80"
    restart: on-failure
```

## Key Components of the Configuration
### Service: Excalidraw
- **Image**: `excalidraw/excalidraw:latest` is the Docker image used for Excalidraw.
- **Ports**: 
  - `3030:80` maps port 3030 on the host to port 80 in the container, where Excalidraw's web interface is accessible.
- **Restart Policy**: `on-failure` ensures that the Excalidraw service restarts automatically in case of failure.

## Deploying Excalidraw

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Excalidraw in detached mode.
3. Access Excalidraw by navigating to `http://<host-ip>:3030`.

## Configuring and Using Excalidraw

After deployment, Excalidraw is ready to use through its web interface, providing a collaborative platform for sketching and diagramming.


## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/yk5bBo8JAG4?si=8MztGs2h7a3i9ubE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise a PR on [GitHub](https://github.com/Techdox/techdox-docs).
