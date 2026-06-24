---
title: Internal Hostnames with NPM and Pi-hole
description: Serve internal self-hosted services at real domain names with HTTPS using Nginx Proxy Manager and Pi-hole local DNS records. No public exposure required.
---

# Internal Hostnames with NPM and Pi-hole

Running self-hosted services at bare IPs and ports (`http://192.168.1.x:8080`) is functional but messy. This guide sets up proper domain names for internal services with HTTPS — so you can access them as `https://service.yourdomain.com` from inside your network, with a valid certificate, without exposing anything publicly.

## Prerequisites

- [Nginx Proxy Manager](../npm.md) running on your network with a static IP
- Pi-hole running with local DNS access
- A domain with Cloudflare DNS (required for DNS-01 certificate challenges on internal-only domains)
- OPNsense or any router with Dnsmasq host overrides (see [OPNsense setup](opnsense-zimaboard.md))

---

## Architecture

```text
Internal client
    ↓ (DNS query: service.yourdomain.com)
Pi-hole
    ↓ (local DNS record: service.yourdomain.com → NPM IP)
Nginx Proxy Manager (192.168.1.x)
    ↓ (proxy pass to service backend)
Service (192.168.1.y:port)
```

Pi-hole intercepts the DNS query and returns NPM's internal IP. The client connects to NPM, which terminates TLS and proxies to the backend. The certificate is valid because it was issued via DNS-01 challenge — no HTTP challenge needed, so no public exposure required.

---

## Step 1: Add a Local DNS Record in Pi-hole

For each service you want to serve internally:

1. Open Pi-hole admin → **Local DNS → DNS Records**
2. Click **Add**
3. Set **Domain** to your service hostname (e.g., `service.yourdomain.com`)
4. Set **IP Address** to your NPM host IP (e.g., `192.168.1.x`)
5. Save

!!! tip
    You can use any subdomain you own. Using your real domain (not `.local`) means you can get a valid publicly-trusted certificate via DNS-01 challenge, which `.local` domains cannot get.

---

## Step 2: Create a Proxy Host in NPM

1. Open NPM → **Proxy Hosts → Add Proxy Host**
2. Set **Domain Names** to the same hostname (e.g., `service.yourdomain.com`)
3. Set **Scheme** to `http` (or `https` if the backend uses it)
4. Set **Forward Hostname / IP** to the service's internal IP
5. Set **Forward Port** to the service's port
6. Enable **Websockets Support** if the service needs it

---

## Step 3: Request a Certificate (DNS-01)

In the **SSL** tab of the proxy host:

1. Select **Request a new SSL Certificate**
2. Enable **Force SSL**
3. Select **DNS Challenge**
4. Choose **Cloudflare** as the DNS provider
5. Enter your Cloudflare API token (needs `Zone → DNS → Edit` permissions)
6. Request the certificate

!!! warning "Use a scoped API token"
    Use a **scoped API token** with only `Zone → DNS → Edit` permission. Do not use your global Cloudflare API key — a compromised scoped token limits the blast radius.

DNS-01 challenges prove domain ownership by creating a TXT record in DNS, which Cloudflare handles automatically. Your service never needs to be publicly reachable for the certificate to issue.

!!! note "Wildcard certificate option"
    If you have many internal services on the same domain, request a wildcard certificate for `*.yourdomain.com` once and reuse it across all proxy hosts. This avoids rate limits and simplifies renewal.

---

## Step 4: Advanced — Proxying Self-Signed Backends

If the service you're proxying uses HTTPS with a self-signed certificate (some services default to this):

In NPM's **Advanced** tab for the proxy host, add:

```nginx
proxy_ssl_verify off;
```

This tells NPM not to validate the backend's certificate (since it's self-signed). The connection from client to NPM is still fully valid TLS.

---

## OPNsense Web UI Gotcha

If you're proxying OPNsense's web interface through NPM, you'll get HTTP_REFERER errors unless you tell OPNsense about the alternate hostname.

Navigate to **System → Settings → Administration → Alternate Hostnames** and add:

- Your NPM proxy hostname (e.g., `opnsense.yourdomain.com`)
- NPM's own hostname if you're also proxying NPM itself

---

## Combining Internal and Public Services

This setup pairs naturally with [Cloudflare Tunnels](cloudflare-tunnels.md). The same domain resolves differently depending on where the client is:

| Client location | DNS resolution | Path |
|----------------|----------------|------|
| Inside LAN | Pi-hole local DNS → NPM IP | NPM → service (internal TLS) |
| Outside LAN | Cloudflare public DNS → Tunnel CNAME | Cloudflare Tunnel → service |

No split DNS zones required — Pi-hole's local record overrides the public Cloudflare record for internal clients, because Pi-hole resolves before any public query leaves the network.

---

## Verification

```bash
# From inside your LAN, verify the local DNS record resolves
dig service.yourdomain.com @192.168.1.x   # replace with Pi-hole IP
# Should return NPM's internal IP

# Verify HTTPS works
curl -I https://service.yourdomain.com
# Should return HTTP 200 with valid certificate details
```

In a browser, the padlock should show a valid certificate issued by Let's Encrypt (or ZeroSSL).

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Certificate request fails | Cloudflare API token lacks DNS edit permission | Check token permissions in Cloudflare dashboard |
| Browser shows "not secure" | Certificate issued for wrong hostname | Check NPM proxy host domain matches Pi-hole record |
| `502 Bad Gateway` | Service not running or wrong IP/port | Verify backend is reachable from NPM host |
| HTTP_REFERER errors in OPNsense | Hostname not in Alternate Hostnames | Add to System → Settings → Administration |
| Internal clients still hitting public IP | Pi-hole local record missing | Add local DNS record in Pi-hole |

---

## Related Pages

- [Cloudflare Tunnels](cloudflare-tunnels.md) — the public-facing counterpart
- [Pi-hole + Unbound DNS](dns-stack.md) — Pi-hole setup and local DNS
- [OPNsense on Zimaboard 2](opnsense-zimaboard.md) — Dnsmasq host overrides as an alternative to Pi-hole local DNS for LAN hostnames

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
