<a href="https://my.racknerd.com/aff.php?aff=5792ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Setting Up Logitech Media Server with Docker Compose
description: Logitech Media Server (LMS) is a software that powers audio streaming to Logitech Squeezebox players.
---


# Setting Up Logitech Media Server with Docker Compose

## Introduction to Logitech Media Server

Logitech Media Server (LMS) is a software that powers audio streaming to Logitech Squeezebox players. It allows you to listen to your music collection anywhere in your home, controlling it with a mobile device or computer.

## Docker Compose Configuration for LMS

This Docker Compose setup deploys Logitech Media Server in a Docker container, ensuring a reliable and dedicated environment for your music streaming needs.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3'
services:
  lms:
    container_name: lms
    image: lmscommunity/logitechmediaserver
    volumes:
      - /<somewhere>:/config:rw
      - /<somewhere>:/music:ro
      - /<somewhere>:/playlist:rw
      - /etc/localtime:/etc/localtime:ro
      - /etc/timezone:/etc/timezone:ro
    ports:
      - 9000:9000/tcp
      - 9090:9090/tcp
      - 3483:3483/tcp
      - 3483:3483/udp
    restart: always
```

## Key Components of the Configuration

### Volumes
- `/<somewhere>:/config:rw`: Maps the local configuration directory to the container's configuration directory.
- `/<somewhere>:/music:ro`: Maps the local music directory to the container, read-only.
- `/<somewhere>:/playlist:rw`: Maps the local playlist directory to the container.
- `/etc/localtime:/etc/localtime:ro`: Maps the local time setting for correct time display.
- `/etc/timezone:/etc/timezone:ro`: Ensures the container uses the correct timezone.

### Ports
- `9000:9000/tcp`: Web interface.
- `9090:9090/tcp`: CLI port.
- `3483:3483/tcp` and `3483:3483/udp`: Used for streaming and device discovery.

### Restart Policy
- `always`: Ensures LMS restarts automatically unless manually stopped.

## Deploying LMS

1. Replace `/<somewhere>` with your actual directory paths in the Docker Compose file.
2. Save the configuration in a `docker-compose.yml` file.
3. Run `docker compose up -d` to start the LMS container in detached mode.
4. Access the LMS web interface via `http://<host-ip>:9000`.

## Configuring and Using LMS

After deployment, configure your music libraries, playlists, and settings via the LMS web interface. Connect your Squeezebox devices or compatible software players to start streaming your music.


<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
