---
title: Setting Up Linkstack with Docker Compose
description: Linkstack is a web application that provides a user-friendly platform for managing and organizing web links. It is designed for ease of use and convenience in storing a collection of links.
---

# Setting Up Linkstack with Docker Compose

## Introduction to Linkstack

Linkstack is a web application that provides a user-friendly platform for managing and organizing web links. It is designed for ease of use and convenience in storing a collection of links.

## Docker Compose Configuration for Linkstack

This Docker Compose setup deploys Linkstack in a Docker container, offering a dedicated environment for link management.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  linkstack:
    image: linkstackorg/linkstack
    container_name: linkstack
    hostname: linkstack
    environment:
      #HTTP_SERVER_NAME: "www.example.xyz"
      #HTTPS_SERVER_NAME: "www.example.xyz"
      SERVER_ADMIN: "[email protected]"
      TZ: "Pacific/Auckland"
      PHP_MEMORY_LIMIT: "512M"
      UPLOAD_MAX_FILESIZE: "8M"
    ports:
      - "8099:80"
      - "8443:443"
    restart: unless-stopped
    volumes:
      - "linkstack:/htdocs"
volumes:
  linkstack:
```

## Key Components of the Configuration
### Service: Linkstack
- **Image**: `linkstackorg/linkstack` is the Docker image used for Linkstack.
- **Environment Variables**: 
  - `SERVER_ADMIN`: Email address of the server administrator.
  - `TZ`: Timezone set to "Pacific/Auckland".
  - `PHP_MEMORY_LIMIT`: PHP memory limit set to "512M".
  - `UPLOAD_MAX_FILESIZE`: Maximum file upload size set to "8M".
  - `HTTP_SERVER_NAME` and `HTTPS_SERVER_NAME` are commented out and can be set as needed.
- **Ports**: 
  - `8099:80` maps HTTP traffic from port 8099 on the host to port 80 in the container.
  - `8443:443` maps HTTPS traffic from port 8443 on the host to port 443 in the container.
- **Volumes**: 
  - `linkstack:/htdocs` provides persistent storage for Linkstack's data.
- **Restart Policy**: `unless-stopped` ensures that Linkstack restarts automatically unless explicitly stopped.

## Deploying Linkstack

1. Save the Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start Linkstack in detached mode.
3. Access Linkstack's web interface via `http://<host-ip>:8099`.

## Configuring and Using Linkstack

After deployment, configure Linkstack through its web interface to start organizing and managing your web links.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/bHNNSFoMuAI?si=eOYtfpNEpnTvDJNY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
