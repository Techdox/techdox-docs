---
title: Deploying Pocket ID with Docker Compose
description: Pocket ID is a self-hosted, privacy-focused identity management solution. This guide provides step-by-step instructions for deploying Pocket ID using Docker Compose, including the required Docker Compose configuration and environment variables.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Deploying Pocket ID with Docker Compose

## Introduction to Pocket ID

[Pocket ID](https://pocket-id.org/) is an open-source, self-hosted identity management service designed for privacy and simplicity. Pocket ID allows users to securely manage identities and authentication for various applications. This guide provides the steps required to deploy Pocket ID using Docker Compose.

## Docker Compose Configuration for Pocket ID

Below is the Docker Compose file necessary for deploying Pocket ID, including explanations of key components.

### Docker Compose File (`docker-compose.yml`)

```yaml
services:
  pocket-id:
    image: ghcr.io/pocket-id/pocket-id
    restart: unless-stopped
    env_file: .env
    ports:
      - 3055:1411
    volumes:
      - "./data:/app/data"
    # Optional healthcheck
    healthcheck:
      test: "curl -f http://localhost:1411/healthz"
      interval: 1m30s
      timeout: 5s
      retries: 2
      start_period: 10s
```

## Explanation of Key Components

### Service

- **pocket-id**: Runs the Pocket ID application.
- **Image**: Pulls the latest image from the Pocket ID GitHub Container Registry.
- **Ports**: Maps port 3055 on the host to port 80 in the container, making Pocket ID accessible via `http://<your-server-ip>:3055`.
- **Volumes**:
  - `./data:/app/backend/data`: Mounts the local data directory for persistent storage.
- **Healthcheck**: Ensures the container is running properly and provides automated health monitoring.

## Environment Configuration File

Pocket ID requires environment variables for proper configuration. These settings must be provided in the `.env` file.

### Example `.env` File

```env
# Documentation: https://pocket-id.org/docs/configuration/environment-variables
APP_URL=https://pocket.techdox.nz         # Public URL for your Pocket ID instance
TRUST_PROXY=true                          # Enables reverse proxy support
MAXMIND_LICENSE_KEY=                      # (Optional) License key for GeoIP features
PUID=1000                                 # User ID for file permission management
PGID=1000                                 # Group ID for file permission management
```

**Note**:
- Replace the placeholder values with your specific configuration.
- For detailed explanations, visit the [Pocket ID environment variables documentation](https://pocket-id.org/docs/configuration/environment-variables).

## Deployment Steps

To deploy Pocket ID, follow these steps:

1. **Create the `.env` Configuration File**: Ensure the `.env` file is created with your desired settings.
2. **Run Docker Compose**: In the directory containing your `docker-compose.yml` file, start Pocket ID with:
   ```bash
   docker compose up -d
   ```
   This command starts the Pocket ID container in detached mode.

3. **Verify Deployment**: Confirm Pocket ID is running correctly by accessing:
   ```bash
   http://<your-server-ip>:3055
   ```

4. **Setup Admin Account**: To set up your admin account, navigate to:
   ```bash
   http://<your-server-ip>:3055/login/setup
   ```
   You can now sign in with the admin account and begin managing your identities.

5. **Restarting the Service**: After changes to `.env`, restart the container:
   ```bash
   docker compose restart pocket-id
   ```

## Conclusion

By following this guide, you have successfully deployed Pocket ID using Docker Compose. You can now securely manage identities for your applications in a self-hosted and privacy-focused environment.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).

