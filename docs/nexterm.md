---
title: Deploying Nexterm with Docker Compose
description: Nexterm is an open-source server management software that allows you to manage SSH, VNC, and RDP connections. This guide provides steps for deploying Nexterm using Docker Compose.
tags:
  - docker
  - utilities
---

# Deploying Nexterm with Docker Compose

## Introduction to Nexterm

Nexterm is an open-source server management software designed for handling SSH, VNC, and RDP connections. It provides a unified platform to manage remote connections securely and efficiently. This guide details how to deploy Nexterm using Docker Compose.

## Docker Compose Configuration for Nexterm

Below is the Docker Compose file used to deploy Nexterm, with an explanation of the components.

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  nexterm:
    image: germannewsmaker/nexterm:1.0.9-OPEN-PREVIEW # Specifies the Docker image for Nexterm.
    ports:
      - "6989:6989"                                   # Exposes port 6989 for accessing Nexterm's interface.
    restart: always                                   # Ensures the container restarts automatically if stopped.
    volumes:
      - nexterm:/app/data                             # Stores Nexterm's data persistently.

volumes:
  nexterm:                                             # Declares a named volume for data persistence.
```

### Explanation of Key Components

- **Image**: Specifies the Docker image `germannewsmaker/nexterm:1.0.9-OPEN-PREVIEW`. Nexterm is currently in open preview; check [releases](https://github.com/gnmyt/Nexterm/releases) for the latest tag.
- **Ports**: Maps port `6989` on the host to port `6989` inside the container, allowing access to Nexterm via `http://<your-server-ip>:6989`.
- **Volumes**: A named volume `nexterm:/app/data` is used to persist data. This volume ensures that configuration and data are retained across container restarts.
- **Restart**: Configured to `always` so the container will automatically restart in case of failures.

## Preparing for Deployment

Before deploying Nexterm, ensure that Docker and Docker Compose are installed on your system. No special preparation is required for directories since the named volume `nexterm` will be managed by Docker.

## Deployment

To deploy Nexterm, navigate to the directory where your `docker-compose.yml` file is located and run:

```bash
docker compose up -d
```

This command will start the Nexterm service in detached mode, running it in the background.

## Accessing Nexterm

After deployment, you can access the Nexterm interface by navigating to:

```text
http://<your-server-ip>:6989
```

From here, you can manage your SSH, VNC, and RDP connections using Nexterm's unified interface.

!!! tip "Check for newer releases"
    The image tag above may not be the latest version. Check the [Nexterm releases page](https://github.com/gnmyt/Nexterm/releases) and update the tag to the current release.

## Updating Nexterm

This guide pins a specific image tag, so `docker compose pull` alone will not fetch a newer version. To update, change the image tag in your `docker-compose.yml` to the latest release from the [Nexterm releases page](https://github.com/gnmyt/Nexterm/releases), then run:

```bash
docker compose up -d
```

!!! tip "Back up before updating"
    Your data lives in the `nexterm` named volume. Back this up before major version updates.

## Conclusion

Nexterm is an excellent solution for managing multiple remote connection protocols (SSH, VNC, RDP) in one place. By following this guide, you can deploy Nexterm using Docker Compose and ensure that your configuration and data are stored persistently using Docker volumes.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
