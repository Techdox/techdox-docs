---
title: Migrating to OPNsense on Zimaboard 2
description: How to replace a consumer mesh router with OPNsense running on a Zimaboard 2, covering hardware, install, DHCP with Dnsmasq, host overrides, and the physical cutover.
---

# Migrating to OPNsense on Zimaboard 2

I replaced a TP-Link Deco mesh system with OPNsense running on a Zimaboard 2. The Deco now runs purely as Wi-Fi access points — routing, DNS, DHCP, firewall, and VPN all moved to OPNsense. This guide walks through the full process, including the gotchas that most OPNsense guides skip.

## Prerequisites

- Zimaboard 2 (or similar x86_64 SBC with dual NICs)
- USB stick (4 GB or larger)
- Monitor and keyboard for the initial install
- A spare computer for flashing the USB
- [Balena Etcher](https://etcher.balena.io/) installed
- Your current network documented (see Pre-cutover prep below)

---

## Hardware: Zimaboard 2

The [Zimaboard 2](https://www.zimaboard.com/) is a single-board server with dual 2.5GbE NICs, an x86_64 Intel processor, and onboard eMMC storage. It's a solid choice for a home router:

- **Dual 2.5GbE** — one WAN, one LAN (connect to your switch or AP)
- **x86_64** — full OPNsense compatibility, including Suricata IDS
- **Passive cooling** — no fan, no noise
- **Low power** — suitable for always-on use

---

## Pre-Cutover Preparation

Before pulling the plug on your existing router, document your current setup. You'll need this to recreate it in OPNsense.

- [ ] WAN connection type (most home connections are DHCP from the ISP — no PPPoE needed)
- [ ] Your current LAN subnet (e.g., `192.168.1.0/24`)
- [ ] DHCP range your router is using
- [ ] Any static/reserved IPs (hostname, IP, MAC address for each)
- [ ] Any port forwards you need to recreate
- [ ] Your current DNS config (what upstream DNS servers are set)

!!! tip
    If you're migrating to Pi-hole + Unbound (see [DNS Stack](dns-stack.md)), note your Pi-hole's IP now — you'll point OPNsense's DHCP at it during setup.

---

## Installation

### 1. Download OPNsense

Go to [opnsense.org/download](https://opnsense.org/download/) and download:

- **Architecture**: amd64
- **Image type**: vga (not serial)
- **Format**: `.img.bz2`

### 2. Decompress and Flash

On macOS, double-clicking the `.img.bz2` decompresses it automatically. Then flash to your USB stick with Balena Etcher.

!!! warning
    Etcher will erase the USB stick. Make sure you select the correct drive.

### 3. Boot the Zimaboard from USB

Connect monitor, keyboard, and USB stick to the Zimaboard. Power it on and boot from USB (you may need to press `F11` or `Del` during POST to select the boot device).

### 4. Run the Installer

At the login prompt:

```text
Username: installer
Password: opnsense
```

When the installer starts:

1. Accept the default keymap (or select yours)
2. Choose **Install (ZFS)** — more resilient than UFS for flash storage
3. Stripe layout (no RAID — single device)
4. Select the **internal eMMC** as the install target — **not your USB stick**
5. Set a root password when prompted

!!! warning "Keyboard layout during install"
    If you change the keymap during install, make sure you type your root password using that layout. Mismatches here cause login failures later and are hard to debug remotely.

### 5. Remove USB and Reboot

Once the install completes, remove the USB stick and let the Zimaboard reboot into OPNsense.

---

## Initial Configuration

OPNsense defaults to `192.168.1.1` on the LAN interface. Connect a laptop or Raspberry Pi directly to the LAN port via Ethernet and browse to `https://192.168.1.1`.

Default credentials: `root` / the password you set during install.

### Run the Setup Wizard

The wizard runs on first login. Work through each step:

**General**

- Hostname: whatever you want (e.g., `router`)
- Domain: `local` or `localdomain`
- Primary DNS: your Pi-hole IP (e.g., `192.168.1.x`) — you'll update this after cutover
- Uncheck **Override DNS**

**WAN Interface**

- Type: **DHCP** (for most home broadband connections)
- MTU: 1500
- Enable **Block private networks** and **Block bogon networks**

**LAN Interface**

- Change the IP to match your existing subnet (e.g., `192.168.1.1/24`)
- Reconnect at the new IP after the wizard saves

!!! tip
    If you're keeping your existing subnet (e.g., `192.168.1.0/24`), your devices won't need to renew leases after cutover.

---

## DHCP Configuration (Dnsmasq)

!!! note "OPNsense v26 uses Dnsmasq by default"
    OPNsense 26.x switched to **Dnsmasq** as the default DHCP server, replacing Kea. Most older guides and forum posts reference Kea or ISC DHCP — ignore those settings. Look for **Services → Dnsmasq DNS & DHCP**.

Navigate to **Services → Dnsmasq DNS & DHCP → General** and configure:

- **DHCP Range**: Set a start and end IP that leaves room for your static reservations outside the pool. Example: `192.168.1.100` to `192.168.1.250`
- **DHCP Option 6** (DNS server): Point this at your Pi-hole IP. This tells every DHCP client to use Pi-hole for DNS.

```text
Option: 6 (dns-server)
Value: 192.168.1.x    ← your Pi-hole's IP
```

- **Dnsmasq DNS listen port**: Leave at `53053` — this avoids conflicting with Pi-hole on port 53 if they're on the same host. Since Pi-hole is on a separate machine, this doesn't matter, but leaving it non-standard avoids confusion.

!!! warning "Disable Unbound DNS to avoid port conflicts"
    If you leave Unbound running alongside Pi-hole, both will compete for port 53, causing DNS resolution failures that are difficult to diagnose. Disable Unbound in OPNsense before pointing clients to Pi-hole.

- **Disable Unbound DNS**: Go to **Services → Unbound DNS** and disable it. Pi-hole owns DNS in this setup; you don't want Unbound competing.

---

## Host Overrides — DHCP Reservations + Local DNS in One

This is one of the most useful features of Dnsmasq that most guides underexplain. Under **Services → Dnsmasq DNS & DHCP → Hosts**, you can add entries that serve two purposes simultaneously:

1. **DHCP reservation** — the device always gets the same IP via MAC address
2. **Local DNS record** — the hostname resolves on your LAN without needing Pi-hole local DNS records

For each server or device that needs a stable IP:

| Field | Value |
|-------|-------|
| Host | `pihole-host` |
| Domain | `local` |
| IP address | `192.168.1.x` |
| MAC address | `aa:bb:cc:dd:ee:ff` |
| Tick **Local** | ✅ |

With **Local** ticked, `pihole-host.local` resolves to that IP from any device on the network — no separate Pi-hole local DNS record needed for LAN hosts.

!!! tip
    Set up all your reservations here before cutover so devices get the right IPs from the first DHCP lease.

---

## The Physical Cutover

Once OPNsense is configured and you've verified it boots and accepts your login:

1. **Switch your Deco (or other mesh AP) to Access Point mode** — in the Deco app: More → Advanced → Operating Mode → Access Point. This disables its DHCP server and routing.
2. Unplug the fibre/coax cable from your old router's WAN port
3. Plug it into the Zimaboard's WAN port
4. Plug the Zimaboard's LAN port into your switch or directly into the main Deco/AP
5. Wait ~60 seconds for the WAN DHCP lease to come up
6. Test from a connected device — you should have internet within a minute

---

## Verification

```bash
# Check you're getting DNS from Pi-hole
cat /etc/resolv.conf           # should show your Pi-hole IP

# Test internet
ping -c 3 1.1.1.1

# Check DNS works
dig google.com @192.168.1.x    # replace with Pi-hole IP
```

From the OPNsense dashboard: **Lobby → Dashboard** should show WAN with an IP from your ISP.

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Changes not taking effect | Forgot to click **Apply** | Every change in OPNsense requires the Apply button |
| No internet after cutover | ISP MAC binding (rare) | Clone your old router's MAC under Interfaces → WAN |
| Can't log in after install | Keyboard layout mismatch during password entry | Console reset via physical access |
| DHCP not working | Dnsmasq not enabled | Services → Dnsmasq DNS & DHCP → General → Enable |
| Devices not resolving local hostnames | Local tick not checked on host override | Edit each host override, tick Local, apply |

---

## Related Pages

- [Pi-hole + Unbound DNS Stack](dns-stack.md) — configure DNS after OPNsense is running
- [WireGuard VPN](wireguard-vpn.md) — add VPN to your OPNsense router
- [Internal Hostnames](internal-hostnames.md) — serving internal services with proper TLS

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
