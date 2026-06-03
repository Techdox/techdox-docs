---
title: Pi-hole + Unbound DNS Stack
description: Build a fully self-contained DNS stack with Pi-hole for ad blocking and Unbound for recursive resolution. No queries leave to Cloudflare, Google, or your ISP.
---

# Pi-hole + Unbound DNS Stack

Most home networks send DNS queries to Cloudflare (1.1.1.1) or Google (8.8.8.8). Those companies log your queries, build profiles, and in Google's case, tie the data to your account. This guide builds a stack where your DNS queries never leave your network — Pi-hole blocks ads and trackers, Unbound resolves everything directly from root servers, and DNSSEC validates responses end-to-end.

## Prerequisites

- Pi-hole running on a dedicated host (Raspberry Pi, VM, or container) with a static IP
- OPNsense router (see [OPNsense on Zimaboard 2](opnsense-zimaboard.md)) — or any router that lets you configure DHCP option 6 and run Unbound
- Basic familiarity with Pi-hole's admin interface

---

## Architecture

```
Client device
    ↓ (DNS via DHCP option 6)
Pi-hole (192.168.1.x)
    ↓ (upstream: Unbound on OPNsense)
Unbound (192.168.1.1 port 53)
    ↓ (iterative query)
Root DNS servers → TLD servers → Authoritative servers
```

- Client devices receive Pi-hole's IP as their DNS server via DHCP
- Pi-hole performs ad/tracker blocking via its gravity lists
- Blocked domains return `0.0.0.0` — the client gets nothing, the ad never loads
- Unblocked queries are forwarded to Unbound on OPNsense
- Unbound resolves the query iteratively — no third-party DNS involved
- DNSSEC validation happens at the Unbound level

---

## Configuring Unbound on OPNsense

Navigate to **Services → Unbound DNS → General**:

| Setting | Value |
|---------|-------|
| Enable Unbound | ✅ |
| Listen Port | `53` |
| Network Interfaces | `LAN` only — **never** WAN |
| Enable DNSSEC Support | ✅ |
| Local Zone Type | `transparent` |

!!! warning "Never enable Unbound on the WAN interface"
    Binding Unbound to WAN makes your resolver publicly accessible, turning it into an open resolver that anyone on the internet can abuse for DNS amplification attacks. LAN only.

Save and apply. Unbound is now listening on your router's LAN IP on port 53.

---

## Configuring Pi-hole

### Point Pi-hole at Unbound

In Pi-hole's admin interface: **Settings → DNS → Upstream DNS Servers**

- Uncheck all public resolvers (Cloudflare, Google, Quad9, OpenDNS)
- Under **Custom**, enter your OPNsense LAN IP with port 53:

```
192.168.1.1#53
```

(Replace `192.168.1.1` with your OPNsense LAN IP if different.)

Save and apply. Pi-hole now sends all non-blocked queries to Unbound rather than a public resolver.

### (Optional) Enable DNSSEC in Pi-hole

Pi-hole can also display DNSSEC status in its query log. Under **Settings → DNS**:

- Enable **Use DNSSEC**

This is display-only when using Unbound as upstream — Unbound handles the actual validation — but it confirms validation status in Pi-hole's logs.

---

## Verifying the Chain

Run these checks from a device on your network:

```bash
# 1. Check Pi-hole is responding
dig @192.168.1.x google.com
# Should return A records with status: NOERROR

# 2. Check ad blocking works
dig @192.168.1.x doubleclick.net
# Should return 0.0.0.0 (blocked by Pi-hole gravity)

# 3. Check DNSSEC validation
dig @192.168.1.x dnssec-failed.org
# Should return SERVFAIL — this domain intentionally fails DNSSEC
# If you get an A record back, DNSSEC is NOT working

# 4. Trace the recursive resolution path
dig +trace google.com
# Shows the full chain: root → .com TLD → google.com authoritative
```

!!! tip
    The `dnssec-failed.org` test is the most important one. If DNSSEC is working correctly, this domain returns `SERVFAIL`. If it returns an IP address, something in your chain isn't validating signatures.

---

## Why This is Better Than Common Alternatives

| Approach | DNS data goes to | Ad blocking | DNSSEC |
|----------|-----------------|-------------|--------|
| ISP default | Your ISP | ❌ | ❌ |
| Cloudflare 1.1.1.1 | Cloudflare | ❌ | ✅ |
| Pi-hole → Cloudflare | Cloudflare | ✅ | ✅ |
| Pi-hole → Unbound (this guide) | Nobody | ✅ | ✅ |

With Pi-hole + Unbound:

- **No DNS data leaves your network** to any third party
- **Network-wide ad blocking** for all devices including phones, TVs, and IoT
- **DNSSEC validation** prevents DNS spoofing and cache poisoning
- **Local hostname resolution** via Dnsmasq host overrides on OPNsense (see [OPNsense setup](opnsense-zimaboard.md#host-overrides))

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Pi-hole showing no queries | Devices using a different DNS | Check DHCP option 6 is set to Pi-hole IP |
| `SERVFAIL` on all domains | Unbound not running, or wrong IP in Pi-hole | Verify Unbound is enabled; check the upstream IP |
| Ads still showing on some apps | App using DNS-over-HTTPS (DoH) bypassing Pi-hole | Block known DoH providers in Pi-hole, or block port 853 at the firewall |
| Local hostnames not resolving | Dnsmasq host overrides not configured | See [OPNsense host overrides](opnsense-zimaboard.md#host-overrides) |

---

## Related Pages

- [OPNsense on Zimaboard 2](opnsense-zimaboard.md) — set up DHCP option 6 and Dnsmasq host overrides
- [Internal Hostnames](internal-hostnames.md) — serve internal services with proper domain names
- [WireGuard VPN](wireguard-vpn.md) — Pi-hole filtering works through the VPN too with the right NAT rules

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
