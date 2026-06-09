---
title: Setting Up IT Tools with Docker Compose
description: IT Tools Docker container using Docker Compose. IT Tools is a utility container providing various information technology tools.
---

# Deploying IT Tools with Docker Compose

## Deployment of IT Tools

This section guides you through setting up the IT Tools Docker container using Docker Compose. IT Tools is a utility container providing various information technology tools.

### Docker Compose Configuration

Below is the Docker Compose file necessary for deploying the IT Tools service. Save this configuration as `docker-compose.yml` in your project directory.

```yaml
version: '3.9'
services:
  it-tools:
    image: 'corentinth/it-tools:latest'  # The Docker image to use.
    ports:
      - '8080:80'  # Maps port 80 inside the container to port 8080 on the host.
    restart: unless-stopped  # Ensures the container restarts unless it is explicitly stopped.
    container_name: it-tools  # Custom name for the container.
```

### Instructions

1. **Prepare the Environment**:
   Ensure Docker and Docker Compose are installed on your host machine.

2. **Create a Docker Compose File**:
   Create a new file named `docker-compose.yml` and copy the above content into this file.

3. **Start the Container**:
   Run the following command in the directory where your `docker-compose.yml` is located:
   ```bash
   docker compose up -d
   ```
   This command starts the IT Tools container in detached mode.

4. **Accessing IT Tools**:
   Open a web browser and navigate to `http://<host-ip>:8080` to access the IT Tools interface.

By following these steps, you can easily deploy and manage the IT Tools container, which provides a suite of utilities for IT management and troubleshooting.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
