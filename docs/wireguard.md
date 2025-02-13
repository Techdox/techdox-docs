---
title: Setting Up Wireguard and Wireguard UI with Docker Compose
description: Wireguard is a modern VPN (Virtual Private Network) software that provides fast and secure connections. The Wireguard UI is a web interface that makes it easier to manage your Wireguard setup.
---
<a href="https://my.racknerd.com/aff.php?aff=5792ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Setting Up Wireguard and Wireguard UI with Docker Compose

## Introduction to Wireguard and Wireguard UI

Wireguard is a modern VPN (Virtual Private Network) software that provides fast and secure connections. The Wireguard UI is a web interface that makes it easier to manage your Wireguard setup.

## Docker Compose Configuration for Wireguard and Wireguard UI

This Docker Compose setup deploys both Wireguard and Wireguard UI in Docker containers, ensuring a secure, isolated environment for your VPN needs.

### Docker Compose File (`docker-compose.yml`)

!!! warning "Issue with latest image"

    There is an issue with the latest image it seems, please make sure you use the image in the example compose below. If you use latest, the steps in this guide will not work.

```yaml
version: "3"

services:

  wireguard:
    image: linuxserver/wireguard:v1.0.20210914-ls7 #Use this image, latest seems to have issues
    container_name: wireguard
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config:/config
    ports:
      - "5000:5000"
      - "51820:51820/udp"

  wireguard-ui:
    image: ngoduykhanh/wireguard-ui:latest
    container_name: wireguard-ui
    depends_on:
      - wireguard
    cap_add:
      - NET_ADMIN
    network_mode: service:wireguard
    environment:
      - SENDGRID_API_KEY
      - EMAIL_FROM_ADDRESS
      - EMAIL_FROM_NAME
      - SESSION_SECRET
      - WGUI_USERNAME=admin
      - WGUI_PASSWORD=password
      - WG_CONF_TEMPLATE
      - WGUI_MANAGE_START=true
      - WGUI_MANAGE_RESTART=true
    logging:
      driver: json-file
      options:
        max-size: 50m
    volumes:
      - ./db:/app/db
      - ./config:/etc/wireguard
```

## Key Components of the Configuration
### Wireguard Service
- **Image**: `linuxserver/wireguard:v1.0.20210914-ls7`.
- **Capabilities**: `NET_ADMIN` for network management.
- **Volumes**: Maps `./config` to `/config` in the container for configuration storage.
- **Ports**: Exposes port `5000` for web interface and `51820` for UDP traffic.

### Wireguard UI Service
- **Image**: `ngoduykhanh/wireguard-ui:latest`.
- **Dependence**: Depends on the `wireguard` service.
- **Capabilities**: `NET_ADMIN` for network management.
- **Network Mode**: Uses the network of the `wireguard` service.
- **Environment Variables**: Configuration for email notifications, session management, and Wireguard UI settings.
- **Logging**: Configures log file size and format.
- **Volumes**: Maps `./db` for database storage and `./config` for Wireguard configuration.

## Deploying Wireguard and Wireguard UI

1. Save the above Docker Compose configuration in a `docker-compose.yml` file.
2. Run `docker compose up -d` to start the containers in detached mode.
3. Access Wireguard UI via `http://<host-ip>:5000` and configure your VPN.

## Configuring and Using Wireguard and Wireguard UI

After deployment, use the Wireguard UI to manage your Wireguard VPN settings, including adding and configuring VPN clients.


### Post Up

```bash
iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Post Down

```bash
iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

The "Post Up" command and the "Post Down" command are used in the configuration of WireGuard to set up and tear down network routing rules for the WireGuard interface.

The "Post Up" command performs the following actions:

1. It adds a rule to the FORWARD chain of the iptables firewall to accept incoming traffic on the WireGuard interface (wg0). This allows packets to be forwarded between the WireGuard network and other networks.
2. It adds a rule to the POSTROUTING chain of the iptables NAT (Network Address Translation) table to perform MASQUERADE on outgoing packets from the WireGuard interface (wg0) before they are sent out through the eth0 interface. MASQUERADE modifies the source IP address of the packets to match the IP address of the eth0 interface, allowing the response packets to be correctly routed back to the WireGuard network.

The "Post Down" command reverses the actions performed by the "Post Up" command:

1. It deletes the rule from the FORWARD chain of the iptables firewall that accepts incoming traffic on the WireGuard interface (wg0).
2. It deletes the rule from the POSTROUTING chain of the iptables NAT table that performs MASQUERADE on outgoing packets from the WireGuard interface (wg0).

These commands are typically used when configuring a WireGuard VPN server in scenarios where Network Address Translation (NAT) is involved, such as when the server is behind a router performing NAT.

## Youtube Video

<iframe width="560" height="315" src="https://www.youtube.com/embed/QLL5lT0SDoQ?si=Q45zvQMTCsu-7tc-" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
