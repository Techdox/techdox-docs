<a href="https://my.racknerd.com/aff.php?aff=5792ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

---
title: Duplicati - Docker Setup
description: Duplicati is a free and open-source backup software that allows you to securely store backups online in various standard protocols and services.
---

# Duplicati - Docker Setup

# Setting Up Duplicati with Docker Compose

**Introduction to Duplicati:** Duplicati is a free and open-source backup software that allows you to securely store backups online in various standard protocols and services. It's known for its versatility and ease of use, providing features like encryption, compression, and scheduling.

**Docker Compose Configuration for Duplicati:**

The following Docker Compose configuration will help you set up Duplicati in a Docker environment. This ensures a consistent and isolated setup for your backup needs.

**Docker Compose File (docker-compose.yml):**

```yaml
version: "2.1"
services:
  duplicati:
    image: lscr.io/linuxserver/duplicati:latest
    container_name: duplicati
    environment:
      - PUID=0
      - PGID=0
      - TZ=Etc/UTC
      - CLI_ARGS= #optional
    volumes:
      - ./config:/config
      - ./backups:/backups
      - /:/source
    ports:
      - 8200:8200
    restart: unless-stopped

```

**Key Components of the Configuration:**

- **Image:** Utilizes the `lscr.io/linuxserver/duplicati:latest` image, ensuring you have the latest version of Duplicati.
- **Container Name:** Sets the container's name to `duplicati` for easy identification and management.
- **Environment Variables:**
    - `PUID` and `PGID`: Sets user/group ID (here both are set to `0` for root).
    - `TZ`: Timezone configuration, set to `Etc/UTC`.
    - `CLI_ARGS`: Optional field for additional command-line arguments.
- **Volumes:**
    - `./config:/config`: Mounts the local `config` directory to store Duplicati's configuration files.
    - `./backups:/backups`: Designated local directory for storing backups.
    - `/:/source`: Mounts the root directory of the host to the container, allowing access to all files for backup.
- **Ports:** Maps port `8200` of the host to port `8200` of the container, facilitating access to the Duplicati web interface.
- **Restart Policy:** The `unless-stopped` policy ensures that the container restarts automatically unless explicitly stopped.

**Deploying Duplicati:**

1. Save the above Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` in the directory containing this file to start Duplicati in detached mode.
3. Once running, access the Duplicati web interface via `http://<host-ip>:8200`.

**Configuring and Using Duplicati:** After deployment, you can configure backup jobs, schedules, and destinations through the Duplicati web interface. Ensure to properly set up encryption and choose a reliable backup destination to secure your data.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/rchFalToyRA?si=fjyqnjUNE_Hqw1E7" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
