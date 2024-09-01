---
title: Deploying Beszel with Docker Compose
description: Beszel is a self-hosted web application designed to provide a chat interface for various platforms. This guide details deploying Beszel using Docker Compose, including configuration settings for optimized performance.
---

# Deploying Beszel with Docker Compose

## Introduction to Beszel

Beszel is a self-hosted web application designed to provide a chat interface for various platforms. This guide details deploying Beszel using Docker Compose, including configuration settings for optimized performance.

## Docker Compose Configuration for Beszel

Here's how to set up Beszel using Docker Compose, explaining each component of the configuration.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  beszel:
    image: 'henrygd/beszel'        # Specifies the Beszel Docker image.
    container_name: 'beszel'       # Names the container for easier management.
    restart: unless-stopped        # Ensures the container restarts automatically unless stopped.
    ports:
      - '8090:8090'                # Maps port 8090 on the host to port 8090 in the container.
    volumes:
      - ./beszel_data:/beszel_data # Persists data in a bind mount.
```

### Explanation of Key Components

- **Image**: Specifies the Docker image for Beszel, ensuring consistency and compatibility.
- **Ports**: Maps the host port to the container port where Beszel is accessible. Port `8090` is used for both the host and the container.
- **Volumes**: Uses a bind mount (`./beszel_data:/beszel_data`) to store persistent data. This is crucial for maintaining data across container restarts or updates.

## Preparing for Deployment

Ensure that the volume directory exists or Docker will create it at runtime:

```bash
mkdir -p ./beszel_data
```

This command prepares a dedicated storage space for Beszel's data, avoiding data loss during updates or restarts.

## Deployment

To deploy Beszel, navigate to the directory containing your `docker-compose.yml` and run:

```bash
docker compose up -d
```

This command starts the Beszel service in detached mode, running in the background.

## Accessing Beszel

After deployment, Beszel will be accessible at `http://<your-server-ip>:8090` based on your port configuration. This setup ensures that Beszel is ready for chat interface management from your self-hosted environment.

## Conclusion

Deploying Beszel with Docker Compose allows for straightforward setup and management of a self-hosted chat interface. The configuration ensures optimal use of system resources while providing robust data persistence and easy accessibility.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
