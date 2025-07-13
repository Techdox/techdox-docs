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

## Docker Compose Configuration for Dockpeek

Below is the recommended Docker Compose setup to run Dockpeek on your main host, along with a socket proxy. Additional hosts only need the socket proxy component.

### Main Host - `docker-compose.yml`

```yaml
services:
  dockpeek:
    image: ghcr.io/dockpeek/dockpeek:latest
    container_name: dockpeek
    environment:
      - SECRET_KEY=my_secret_key         # Change this to a secure random value
      - USERNAME=admin                   # Set your preferred username
      - PASSWORD=admin                   # Set your preferred password

      # Optional: Configure remote Docker hosts here
      - DOCKER_HOST_1_URL=tcp://192.168.68.113:2375 # Change to your host IP
      - DOCKER_HOST_1_NAME=ElitronCloud # Change for your host name

      - DOCKER_HOST_2_URL=tcp://192.168.68.128:2375 # Change to your host IP
      - DOCKER_HOST_2_NAME=Sandbox # Change for your host name
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

Additional Hosts - Socket Proxy Only

On each additional host you want Dockpeek to monitor, run just the socket proxy:
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
Environment Variable Notes
	•	SECRET_KEY: Required. Used to secure the session cookies. Set a strong random string.
	•	USERNAME and PASSWORD: Default login credentials. Change these before deploying.
	•	DOCKER_HOST_X_URL: Remote Docker socket URL.
	•	DOCKER_HOST_X_NAME: Display name in the UI.
	•	DOCKER_HOST_X_PUBLIC_HOSTNAME: Optional. If omitted, inferred from the socket URL.

You can add more hosts by increasing the number (DOCKER_HOST_3_URL, etc.).

Deployment Steps
	1.	Prepare Docker Compose Files
Set up the main host with both dockpeek and dockpeek-socket-proxy, and ensure remote hosts are running the socket proxy.
	2.	Run Docker Compose
From your compose directory:

docker compose up -d


	3.	Access the Web UI
Open your browser and navigate to:

http://<your-server-ip>:3420


	4.	Login and Configure
Use the username and password you set via environment variables. You’ll see the connected hosts listed on the left.

Conclusion

Dockpeek makes it easy to manage and monitor multiple Docker hosts from one sleek interface. With just a few containers and environment variables, you can get visibility into your entire Docker ecosystem.



⸻

If there is an issue with this guide or you wish to suggest changes, please raise an issue on GitHub.

Let me know if you'd like a thumbnail or summary for the video to go with it.