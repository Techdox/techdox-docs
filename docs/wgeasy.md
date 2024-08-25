---
title: Deploying WG-Easy with Docker Compose
description: WG-Easy is a simple, web-based management interface for WireGuard VPN, which si>
---

# Deploying WG-Easy with Docker Compose

## Introduction to WG-Easy

WG-Easy is a simple, web-based management interface for WireGuard VPN, which simplifies the configuration and management of VPN connections. It provides a user-friendly web interface to configure your VPN without the need for complex command-line tools.

## Docker Compose Configuration

Here's how to deploy WG-Easy using Docker Compose, detailing each component of the configuration to ensure clarity and proper setup.

### Docker Compose File (`docker-compose.yml`)

```yaml
version: '3.8'
services:
  wg-easy:
    image: ghcr.io/wg-easy/wg-easy  # The Docker image to use.
    container_name: wg-easy         # Name of the container.
    environment:                    # Environment variables to configure the instance.
      - LANG=en                     # Language settings.
      - WG_HOST=<Your IP/Domain>    # Public IP or domain name where WG-Easy is accessible.
      - PASSWORD=<Your Password>    # Password for accessing the WG-Easy web interface.
      - PORT=51821                  # Port for the web interface.
      - WG_PORT=51820               # WireGuard port for VPN traffic.
    volumes:
      - ./wg-easy/:/etc/wireguard   # Volume mapping for WireGuard configuration files.
    ports:
      - "51820:51820/udp"           # UDP port used by WireGuard.
      - "51821:51821/tcp"           # TCP port for accessing the web interface.
    cap_add:                        # Capabilities required for managing networking features.
      - NET_ADMIN
      - SYS_MODULE
    sysctls:                        # Kernel parameters that need to be set for WireGuard.
      - net.ipv4.conf.all.src_valid_mark=1
      - net.ipv4.ip_forward=1
    restart: unless-stopped         # Ensures the container restarts automatically unless manually stopped.
```

### Key Configuration Details

- **Environment Variables**:
  - `LANG`: Supports: en, ua, ru, tr, no, pl, fr, de, ca, es, ko, vi, nl, is, pt, chs, cht, it, th, hi
  - `WG_HOST`: Specifies the public IP or DNS name where the WireGuard server can be accessed.
  - `PASSWORD`: Sets a password to secure access to the WG-Easy web interface.
  - `PORT` and `WG_PORT`: Define the ports for the web interface and WireGuard respectively.
- **Volumes**: Maps a local directory (`wg-easy/`) to the container's configuration directory (`/etc/wireguard`). This is where WG-Easy will store its configuration files.
- **Capabilities (`cap_add`)**: `NET_ADMIN` and `SYS_MODULE` are necessary for WG-Easy to manage network interfaces and routes effectively within the container.
- **Sysctls**: Settings like `net.ipv4.ip_forward` enable IP forwarding, which is crucial for routing packets through the VPN.

## Preparing for Deployment

Before running the Docker Compose file, ensure that the local directory (`wg-easy/`) exists on your host machine:

```bash
mkdir -p wg-easy
```

This command creates the directory, avoiding permission issues and ensuring that WireGuard's configuration files are stored persistently.

## Deployment

Deploy WG-Easy using Docker Compose with the following command:

```bash
docker compose up -d
```

This command starts the WG-Easy service in detached mode, running in the background.

## Accessing WG-Easy

Once deployed, access the WG-Easy web interface through `http://your-server-ip:51821`. You'll need to enter the password specified in the `PASSWORD` environment variable to manage your VPN settings.

## Conclusion

Deploying WG-Easy with Docker Compose simplifies the setup of a WireGuard VPN server, providing an accessible and secure way to manage VPN connections through a web-based interface. This setup ensures that your VPN is robustly configured and easily manageable, even for those with minimal technical background.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>
