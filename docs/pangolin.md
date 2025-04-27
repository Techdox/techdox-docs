---
title: Self-Hosting Pangolin with Installer
description: Learn how to deploy Pangolin, a secure and self-hosted alternative to Cloudflare Tunnels, using the official installer.
---

<a href="https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz" target="_blank">
    <img src="https://racknerd.com/banners/728x90.gif" alt="RackNerd Hosting Deals">
</a>

# Self-Hosting Pangolin with the Official Installer

## Introduction

[Pangolin](https://github.com/fosrl/pangolin) is a self-hosted tunneling solution, providing secure access to your internal services and serving as an alternative to Cloudflare Tunnels. It features built-in authentication, role-based access control, and automatic SSL provisioning via Let's Encrypt.

If you're looking for an affordable VPS, consider [RackNerd](https://my.racknerd.com/aff.php?aff=5792&ref=techdox.nz).

## Prerequisites

- Linux system with root access and public IP (Ubuntu/Debian recommended)
- Domain pointing to server IP (including a wildcard A record for service subdomains)
- TCP ports 80, 443, and UDP port 51820 open
- Email address for Let's Encrypt SSL certificate registration
- (Optional) SMTP server details for transactional emails

## Installation Steps

### 1. Download and Run the Installer

Download the installer for your system:

```bash
wget -O installer "https://github.com/fosrl/pangolin/releases/download/1.2.0/installer_linux_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')" && chmod +x ./installer
```

Run the installer with root privileges:

```bash
sudo ./installer
```

### 2. Basic Configuration

Provide the following when prompted:

- **Base Domain Name:** Your main domain (e.g., `example.com`)
- **Dashboard Domain Name:** Domain or subdomain for accessing Pangolin (e.g., `pangolin.example.com`)
- **Let's Encrypt Email:** Your email for SSL registration
- **Tunneling:** Choose whether to install Gerbil tunneling or run Pangolin as a standard reverse proxy

### 3. Admin User Setup

Configure your initial admin user credentials:

- **Admin Email:** Custom or default (e.g., `admin@example.com`)
- **Admin Password:** Must include:
  - At least 8 characters
  - One uppercase letter
  - One lowercase letter
  - One digit
  - One special character

### 4. Security Settings

Choose security options:

- **Signup Without Invite:** Disable recommended for private setups
- **Organization Creation:** Enable or disable as needed

### 5. Email Configuration

Configure SMTP settings for transactional emails (optional):

- SMTP host
- SMTP port (default 587)
- SMTP username/password
- No-reply email address

### 6. Docker Installation

If Docker isn't installed, the installer will automatically set up Docker for your distribution.

### 7. Container Deployment

The installer automatically pulls necessary Docker containers, creates directories, generates config files, and deploys the containers via Docker Compose.

## Post-Installation

Once completed:

- Access Pangolin at your dashboard domain
- Log in using the configured admin credentials

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>


## Feedback

For any issues or suggestions, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).

