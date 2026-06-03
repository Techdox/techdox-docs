---
title: Cloudflare Tunnels for Public Services
description: Expose self-hosted services to the internet without opening a single port. Cloudflare Tunnels create an outbound-only connection from cloudflared to Cloudflare's edge.
---

# Cloudflare Tunnels for Public Services

Port forwarding is the traditional way to expose a home service publicly. It works, but it exposes your real IP, requires managing firewall rules, and puts you one misconfiguration away from an exposed service. Cloudflare Tunnels take the opposite approach: your server makes an outbound connection to Cloudflare's edge, and all inbound traffic comes through that tunnel. No open ports, no exposed IP.

## Prerequisites

- A domain registered and managed with Cloudflare DNS
- A free Cloudflare account (tunnels are included at no cost)
- A host running your service (VM, container, bare metal)
- Docker or the ability to install `cloudflared` as a binary or systemd service

---

## Why Cloudflare Tunnels Over Port Forwarding

| Feature | Port Forwarding | Cloudflare Tunnels |
|---------|----------------|-------------------|
| Open ports on router | ✅ Required | ❌ None |
| Real IP exposed | ✅ Yes | ❌ Hidden |
| DDoS protection | ❌ None | ✅ Cloudflare edge |
| Free SSL | ❌ Manual setup | ✅ Automatic |
| Access control layer | ❌ Manual | ✅ Cloudflare Access (optional) |
| Works behind CGNAT | ❌ No | ✅ Yes |

The last point is important for mobile broadband or ISPs using Carrier-Grade NAT (CGNAT) — you literally can't port forward in those situations. Tunnels work regardless.

---

## How It Works

```
Your service (e.g., port 8080 on your server)
    ↑
cloudflared daemon (running on your server or network)
    ↓ (outbound QUIC/HTTP2 connection to Cloudflare)
Cloudflare edge
    ↑
Public user requests service.yourdomain.com
```

The `cloudflared` process maintains a persistent outbound connection to Cloudflare. When a user visits your domain, traffic flows in through Cloudflare and back through the tunnel to your service. Your server never needs an inbound firewall rule.

---

## Setup Overview

For detailed first-time setup, follow [Cloudflare's official tunnel documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/). The steps below assume you're familiar with the basics.

### 1. Install cloudflared

**Docker Compose (recommended for homelab)**:

```yaml
services:
  cloudflared:
    image: cloudflare/cloudflared:latest
    restart: unless-stopped
    command: tunnel --no-autoupdate run
    environment:
      - TUNNEL_TOKEN=your_tunnel_token_here
```

**Or as a binary on the host**:

```bash
# Debian/Ubuntu
curl -L https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg > /dev/null
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main' | sudo tee /etc/apt/sources.list.d/cloudflared.list
sudo apt update && sudo apt install cloudflared
```

### 2. Authenticate and Create a Tunnel

```bash
cloudflared tunnel login
cloudflared tunnel create my-homelab
```

### 3. Configure Ingress Rules

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: <your-tunnel-id>
credentials-file: /root/.cloudflared/<tunnel-id>.json

ingress:
  - hostname: service1.yourdomain.com
    service: http://localhost:8080
  - hostname: service2.yourdomain.com
    service: http://192.168.1.x:3000
  - service: http_status:404
```

Each `hostname` entry maps a public domain to a local service by IP/port.

### 4. Add DNS Routes

```bash
cloudflared tunnel route dns my-homelab service1.yourdomain.com
cloudflared tunnel route dns my-homelab service2.yourdomain.com
```

This creates `CNAME` records in Cloudflare DNS pointing each subdomain at the tunnel.

### 5. Run the Tunnel

```bash
cloudflared tunnel run my-homelab
# Or as a systemd service:
sudo cloudflared service install
sudo systemctl start cloudflared
```

---

## Integrating with Internal Services

For a homelab running both public and internal services on the same domain:

| Access path | How it works |
|-------------|--------------|
| Public (`service.yourdomain.com` from internet) | Cloudflare Tunnel → service |
| Internal (`service.yourdomain.com` from LAN) | Pi-hole local DNS record → Nginx Proxy Manager → service |

The same domain resolves differently depending on where the client is. Internal clients get the NPM IP from Pi-hole's local DNS; external clients go through Cloudflare. See [Internal Hostnames](internal-hostnames.md) for the internal side of this setup.

---

## Optional: Cloudflare Access (Zero-Trust Auth Layer)

Cloudflare Access adds an authentication layer in front of any tunnelled service. Users must authenticate (via email OTP, Google, GitHub, etc.) before they can even reach your service.

Useful for:
- Admin panels you don't want publicly accessible
- Services without their own authentication
- Adding MFA without modifying the service

Configure in **Cloudflare Zero Trust → Access → Applications**.

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Tunnel connects but service unreachable | Ingress rule IP/port wrong | Check service is listening on the specified address |
| `502 Bad Gateway` | Service not running or wrong port | Verify with `curl http://localhost:<port>` on the host |
| DNS not resolving | CNAME not created | Run `cloudflared tunnel route dns` for the hostname |
| Tunnel drops frequently | Old cloudflared version | Update to latest: `apt upgrade cloudflared` |
| Large file uploads failing | Cloudflare's 100MB upload limit on free plan | Use a paid plan or serve large uploads internally only |

---

## Related Pages

- [Internal Hostnames](internal-hostnames.md) — the internal counterpart to this guide
- [OPNsense on Zimaboard 2](opnsense-zimaboard.md) — no firewall rules needed for tunnels, but useful context

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
