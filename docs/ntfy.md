<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Deploying ntfy with Docker Compose
description: ntfy is a simple and flexible notification service that allows you to send notifications to devices via web, email, or apps. This guide details deploying ntfy using Docker Compose, including configuration settings and health checks.
---

# Deploying ntfy with Docker Compose

## Introduction to ntfy

ntfy is a simple and flexible notification service that allows you to send notifications to devices via web, email, or apps. It can be self-hosted to give you control over your notification system. This guide walks you through deploying ntfy using Docker Compose, including optional settings for timezone, user permissions, and health checks.

## Docker Compose Configuration for ntfy

Below is the Docker Compose file used to deploy ntfy, with a breakdown of the components involved.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: "2.3"

services:
  ntfy:
    image: binwiederhier/ntfy                          # Specifies the ntfy Docker image.
    container_name: ntfy                               # Names the container for easier management.
    command:
      - serve                                          # Runs the ntfy server.
    environment:
      - TZ=UTC                                         # Optional: Sets the timezone. Change as needed.
    user: UID:GID                                      # Optional: Replace with your user/group or UID/GID.
    volumes:
      - /var/cache/ntfy:/var/cache/ntfy                # Persists cache data.
      - /etc/ntfy:/etc/ntfy                            # Stores ntfy configuration files.
    ports:
      - 80:80                                          # Exposes ntfy on port 80.
    healthcheck:                                       # Optional: Health check to ensure ntfy is running properly.
        test: ["CMD-SHELL", "wget -q --tries=1 http://localhost:80/v1/health -O - | grep -Eo '\"healthy\"\\s*:\\s*true' || exit 1"]
        interval: 60s                                  # Runs the health check every 60 seconds.
        timeout: 10s                                   # Timeout for the health check is 10 seconds.
        retries: 3                                     # If the health check fails, retries 3 times.
        start_period: 40s                              # Waits 40 seconds before starting the first check.
    restart: unless-stopped                            # Ensures ntfy restarts unless manually stopped.
```

### Explanation of Key Components

- **Image**: Uses the `binwiederhier/ntfy` Docker image, which is the official ntfy image.
- **Command**: Runs the ntfy server with the `serve` command.
- **Environment Variables**: 
  - **TZ**: Sets the timezone for the ntfy container. This can be adjusted to your local timezone.
- **User**: Optionally specify a user ID and group ID (UID:GID) for running the container. Replace `UID:GID` with your specific values.
- **Volumes**:
  - `/var/cache/ntfy`: This volume stores cache data, helping to persist information between container restarts.
  - `/etc/ntfy`: This volume is used for storing configuration files for ntfy.
  > **Note**: These are the recommended volume locations (`/var/cache/ntfy` and `/etc/ntfy`) because they are standard locations for cache and configuration files, respectively, making it easier to manage and back up data. However, you can modify the volume bindings to point to any directory on your system that fits your organizational structure or storage requirements. Just make sure the paths are valid and accessible to Docker.
- **Ports**: Maps port `80` on the host to port `80` in the container, making ntfy accessible via HTTP on the host machine.
- **Healthcheck**: This optional setting ensures that ntfy is running correctly by checking the health endpoint (`/v1/health`). It retries 3 times with a 10-second timeout if the health check fails.
- **Restart**: Ensures that the ntfy service will restart automatically unless it is manually stopped.

## Preparing for Deployment

Before deploying ntfy, ensure that the necessary directories for volumes are created on the host:

```bash
mkdir -p /var/cache/ntfy
mkdir -p /etc/ntfy
```

These directories will store ntfy’s cache data and configuration files, ensuring they persist between container restarts. If you choose to modify the volume paths, adjust the commands above to match your desired directory structure.

## Deployment

To deploy ntfy, navigate to the directory containing your `docker-compose.yml` file and run:

```bash
docker compose up -d
```

This command will start the ntfy service in detached mode, running it in the background.

## Accessing ntfy

After deployment, ntfy will be accessible at `http://<your-server-ip>:80`. You can use this to send notifications or configure ntfy for further integrations.

## Conclusion

Deploying ntfy with Docker Compose allows you to set up a self-hosted notification service quickly and efficiently. By following this guide, you can ensure that your ntfy instance is running with persistent data storage and optional health checks for reliability. Remember, you can adjust the volume bindings to suit your system's needs while keeping the standard structure for easier management.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
