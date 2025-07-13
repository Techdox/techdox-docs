---
title: Deploying Dockpeek with Docker Compose
description: Dockpeek is a self-hosted web UI for monitoring multiple Docker hosts in one place. This guide shows how to deploy Dockpeek using Docker Compose with optional remote host support.
---
<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Deploying Dockpeek with Docker Compose

## Introduction to Dockpeek

[Dockpeek](https://github.com/dockpeek/dockpeek) is an open-source, self-hosted Docker dashboard that lets you monitor and manage multiple Docker hosts from a single web interface. It supports connecting to remote Docker hosts via socket proxies, giving you visibility into all your containers across different systems.

## Docker Compose Configuration

Below is the recommended Docker Compose configuration for Dockpeek:

### Main Host (`docker-compose.yml`)

```yaml
services:
  dockpeek:
    image: ghcr.io/dockpeek/dockpeek:latest
    container_name: dockpeek
    environment:
      - SECRET_KEY=my_secret_key  # Set to a secure random value
      - USERNAME=admin            # Set your preferred username
      - PASSWORD=admin            # Set your preferred password

      # Optional: Configure additional Docker hosts
      - DOCKER_HOST_1_URL=tcp://192.168.68.113:2375
      - DOCKER_HOST_1_NAME=ElitronCloud

      - DOCKER_HOST_2_URL=tcp://192.168.68.128:2375
      - DOCKER_HOST_2_NAME=Sandbox

    ports:
      - "3420:8000"
    depends_on:
      - dockpeek-socket-proxy
    restart: unless-stopped

  dockpeek-socket-proxy:
    image: lscr.io/linuxserver/socket-proxy:latest
    container_name: dockpeek-socket-proxy
    environment:
      - CONTAINERS=1
      - IMAGES=1
      - PING=1
      - VERSION=1
      - LOG_LEVEL=info
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    read_only: true
    tmpfs:
      - /run
    ports:
      - "2375:2375"
    restart: unless-stopped
```

### Additional Hosts (Socket Proxy Only)

Run this configuration on each additional host:

```yaml
services:
  dockpeek-socket-proxy:
    image: lscr.io/linuxserver/socket-proxy:latest
    container_name: dockpeek-socket-proxy
    environment:
      - CONTAINERS=1
      - IMAGES=1
      - PING=1
      - VERSION=1
      - LOG_LEVEL=info
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    read_only: true
    tmpfs:
      - /run
    ports:
      - "2375:2375"
    restart: unless-stopped
```

## Environment Variable Notes

* **SECRET\_KEY**: Required. Set a strong, random string.
* **USERNAME/PASSWORD**: Set your preferred login credentials.
* **DOCKER\_HOST\_X\_URL**: URL of remote Docker socket.
* **DOCKER\_HOST\_X\_NAME**: Display name in the Dockpeek UI.
* **DOCKER\_HOST\_X\_PUBLIC\_HOSTNAME**: Optional, inferred from socket URL if omitted.

Add more hosts incrementally (`DOCKER_HOST_3_URL`, etc.).

## Deployment Steps

1. **Prepare Docker Compose Files**
   Ensure your `docker-compose.yml` is correctly configured on your main host, and deploy the socket proxy configuration on additional hosts.

2. **Launch Dockpeek**

```bash
docker compose up -d
```

3. **Access Dockpeek Web UI**
   Visit the following URL in your browser:

```
http://<your-server-ip>:3420
```

4. **Login and Manage Docker Hosts**
   Log in using your configured username and password. All connected Docker hosts will be listed.

## Conclusion

Dockpeek simplifies Docker management, providing clear visibility across multiple Docker hosts through a clean and intuitive interface.

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
