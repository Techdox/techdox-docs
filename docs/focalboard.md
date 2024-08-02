---
title: Setting Up Focalboard with Docker Compose
description: Focalboard is an open-source, self-hosted project management tool that's an alternative to Trello, Notion, and Asana. It's designed to help teams stay organized and aligned.
---

# Setting Up Focalboard with Docker Compose

## Introduction to Focalboard

Focalboard is an open-source, self-hosted project management tool that's an alternative to Trello, Notion, and Asana. It's designed to help teams stay organized and aligned.

## Docker Compose Configuration for Focalboard

This Docker Compose setup deploys Focalboard in a Docker container, providing a straightforward and efficient environment for project management.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "3.3"
services:
  focalboard:
    ports:
      - 8000:8000
    restart: always
    image: mattermost/focalboard
```

## Key Components of the Configuration

### Service: Focalboard
- **Image**: `mattermost/focalboard` is used to pull the latest Focalboard image.
- **Ports**: 
  - `8000:8000` exposes Focalboard on port 8000, both on the host and inside the container.
- **Restart Policy**: `always` ensures that the Focalboard service restarts automatically after a crash or reboot.

## Deploying Focalboard

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Focalboard in detached mode.
3. Access Focalboard by navigating to `http://<host-ip>:8000`.

## Configuring and Using Focalboard

After deployment, you can begin using Focalboard by creating boards, adding tasks, and managing projects directly through the web interface.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/CVpQMkBcRO4?si=-_nhWtAp2XURr-Sl" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
