---
title: Start Here - Self-Hosting from Zero
description: New to self-hosting? This guide takes you from nothing to your first running service - hardware, Ubuntu, Docker, and your first container, step by step.
tags:
  - getting-started
  - docker
  - linux
---

# Start Here — Self-Hosting from Zero

New to self-hosting? This page takes you from **nothing to your first running service**. Every other guide on this site assumes you've done the steps below — do them once and the whole site opens up.

<p class="tx-tagline"><em>Break things, start small, document everything.</em></p>

---

## Step 1 — Pick your hardware

You don't need a server rack. Any of these work:

| Option | Good for | Rough cost |
|--------|----------|-----------|
| **An old PC or laptop** | Free if you have one — the classic starting point | $0 |
| **A mini PC** (Intel N100 class) | Low power, silent, plenty fast for 10+ containers | ~$150–250 |
| **Raspberry Pi 4/5** | Tiny, low power — note some images are ARM-only quirky | ~$60–120 |
| **A cheap VPS** | No hardware at all, public IP included | ~$1–3/month — see [RackNerd deals](racknerd.md) |

!!! tip "Start with what you have"
    The best first server is the one you already own. You can always migrate later — that's half the fun.

## Step 2 — Install Ubuntu Server

The guides on this site are written against **Ubuntu Server LTS** (Debian works nearly identically).

1. Download [Ubuntu Server LTS](https://ubuntu.com/download/server)
2. Flash it to a USB stick with [balenaEtcher](https://etcher.balena.io/) or [Rufus](https://rufus.ie/)
3. Boot from the USB and follow the installer — enable **OpenSSH server** when prompted
4. Once installed, connect from your main machine: `ssh your-user@<server-ip>`

!!! tip "Give your server a static IP"
    Set a **DHCP reservation** for your server in your router settings. If the server's IP changes, everything pointing at it breaks.

## Step 3 — Install Docker

Nearly every guide on this site deploys with Docker Compose. Install Docker using the official convenience script:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Then add your user to the `docker` group so you don't need `sudo` for every command:

```bash
sudo usermod -aG docker $USER
```

Log out and back in for the group change to take effect, then verify:

```bash
docker --version
docker compose version
```

Both commands should print version numbers. That's it — Docker Compose v2 ships with Docker.

## Step 4 — Docker in five minutes

The handful of concepts that every guide on this site uses:

- **Image** — the application package, pulled from a registry (e.g. `louislam/uptime-kuma`)
- **Container** — a running instance of an image
- **Volume** — persistent storage. Containers are disposable; volumes are where your data survives. **This is what you back up.**
- **Ports** — `8080:80` means "host port 8080 → container port 80". You browse to the host port.
- **Environment variables** — per-container settings (passwords, timezones, URLs)
- **Compose file** — a `docker-compose.yml` describing all of the above, so your whole setup is one readable text file

The workflow is the same for everything you'll ever deploy:

```bash
mkdir ~/docker/<app> && cd ~/docker/<app>   # one folder per app
nano docker-compose.yml                      # paste the compose file from a guide
docker compose up -d                         # start it
docker compose logs -f                       # watch the logs (Ctrl+C to exit)
```

## Step 5 — Your first container

[Uptime Kuma](uptimekuma.md) is the perfect first deploy — a beautiful status/monitoring dashboard, one service, no database, instantly satisfying.

```bash
mkdir -p ~/docker/uptime-kuma && cd ~/docker/uptime-kuma
```

Create `docker-compose.yml`:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    volumes:
      - ./data:/app/data
    ports:
      - 3001:3001
    restart: unless-stopped
```

Start it:

```bash
docker compose up -d
```

Open `http://<server-ip>:3001`, create your admin account, and add a monitor for a website you care about.

**You are now self-hosting.** 🎉

## Step 6 — Where to go next

<div class="grid cards" markdown>

-   :material-swap-horizontal:{ .lg .middle } __A reverse proxy__

    ---

    Stop memorising ports — give every service a proper name and HTTPS with Nginx Proxy Manager.

    [:octicons-arrow-right-24: Nginx Proxy Manager](npm.md)

-   :material-dns:{ .lg .middle } __Network-wide ad blocking__

    ---

    Block ads and trackers for every device on your network with AdGuard Home.

    [:octicons-arrow-right-24: AdGuard Home](adguard.md)

-   :material-view-dashboard:{ .lg .middle } __A dashboard__

    ---

    One page for all your services with Homepage or Glance.

    [:octicons-arrow-right-24: Homepage](homepage.md)

-   :material-backup-restore:{ .lg .middle } __Backups__

    ---

    Before you host anything you care about, set up scheduled encrypted backups with Duplicati.

    [:octicons-arrow-right-24: Duplicati](duplicati.md)

-   :material-docker:{ .lg .middle } __Everything else__

    ---

    40+ guides — media servers, photo libraries, note apps, monitoring stacks, and more.

    [:octicons-arrow-right-24: Browse all guides](docker-containers.md)

-   :material-home-analytics:{ .lg .middle } __The full homelab build__

    ---

    Ready to go deeper? Follow the complete rebuild — router, DNS, VPN, hardware keys.

    [:octicons-arrow-right-24: Homelab Rebuild series](homelab-rebuild/index.md)

</div>

## The golden rules

!!! tip "Learned the hard way, so you don't have to"
    1. **One folder per app**, with its compose file and data inside — moving or backing up an app becomes copying a folder
    2. **Back up volumes before updating** — `docker compose pull` is safe, but major version jumps can migrate data irreversibly
    3. **Change every default password** — the guides flag them, take the ten seconds
    4. **Don't expose services to the internet** until you understand what that means — use [WireGuard](wireguard.md) or [Cloudflare Tunnels](homelab-rebuild/cloudflare-tunnels.md) instead of port forwarding
    5. **It's a lab.** Breaking things is the curriculum, not a failure

---

Stuck? Join the [Discord](http://discord.com/invite/8mX2KRxDw8) — the community is friendly and someone has hit your error before.

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
