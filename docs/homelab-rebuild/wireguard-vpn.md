---
title: WireGuard VPN on OPNsense
description: Set up WireGuard directly on your OPNsense router for kernel-level VPN performance, native firewall integration, and secure remote access with split or full tunnel support.
---

# WireGuard VPN on OPNsense

Running WireGuard directly on OPNsense means your VPN lives at the kernel level inside the router — not in a container or on a separate host. This gives you better performance, native firewall integration, and a cleaner architecture. Remote clients connect to your router, and routing decisions happen at the same place as all other firewall rules.

## Prerequisites

- OPNsense installed and running (see [OPNsense on Zimaboard 2](opnsense-zimaboard.md))
- WAN port with a reachable IP (static or DDNS)
- UDP port 51820 accessible from the internet (you'll add the firewall rule below)
- WireGuard client app on your devices ([iOS](https://apps.apple.com/app/wireguard/id1441195209), [Android](https://play.google.com/store/apps/details?id=com.wireguard.android), [macOS](https://apps.apple.com/app/wireguard/id1451685025))

!!! warning "CGNAT will prevent external WireGuard connections"
    WireGuard requires an inbound-reachable WAN IP. If your ISP uses CGNAT (carrier-grade NAT), external clients will not be able to connect.

    To check: compare the WAN IP shown in OPNsense with your public IP at [whatismyip.com](https://www.whatismyip.com). If they differ, you're behind CGNAT. Consider using [Cloudflare Tunnels](cloudflare-tunnels.md) as an alternative.

---

## Why WireGuard on the Router?

| Approach | Pros | Cons |
|----------|------|------|
| WireGuard on OPNsense | Kernel performance, native firewall rules, single config point | Slightly more complex initial setup |
| WireGuard in a container | Easy to set up initially | Requires port forwarding, extra NAT hop, no native firewall integration |
| WireGuard on a separate VM | Isolated | More hardware, extra management |

---

## Step 1: Create the WireGuard Server Instance

Navigate to **VPN → WireGuard → Instances → Add**:

| Field | Value |
|-------|-------|
| Name | `wg0` (or any name) |
| Listen Port | `51820` |
| Tunnel Address | `10.10.10.1/24` |
| Generate keypair | Click the generate button |

!!! warning "Tunnel subnet must not overlap with your LAN"
    If your LAN is `192.168.1.0/24`, your WireGuard tunnel must use a different subnet entirely (e.g., `10.10.10.0/24`). Overlap here causes routing failures that are annoying to diagnose.

Save the instance. Note the **public key** — you'll need it when configuring client configs.

---

## Step 2: Add Peers via the Peer Generator

The Peer Generator (**VPN → WireGuard → Peer Generator**) lets you create a peer config and QR code in one step.

For each device (phone, laptop, etc.):

| Field | Value |
|-------|-------|
| Name | Descriptive (e.g., `iphone`, `macbook`) |
| Tunnel Address | Unique IP in the tunnel subnet (e.g., `10.10.10.2/32`) |
| DNS | Your Pi-hole IP (e.g., `192.168.1.x`) |
| Pre-shared key | Generate one |
| Endpoint | `<your-wan-ip>:51820` or your DDNS hostname |
| Allowed IPs | See split vs full tunnel below |
| Keepalive | `25` |

!!! warning "Scroll down and Save before scanning the QR"
    The Peer Generator shows a QR code, but the peer is **not saved to the instance** until you scroll to the bottom and click **Save**. After saving, go to **VPN → WireGuard → Peers** and confirm your peer appears, then edit your WireGuard Instance and make sure the peer is selected in the **Peers** dropdown.

---

## Split Tunnel vs Full Tunnel

The **Allowed IPs** field on each peer controls what traffic goes through the VPN.

### Full Tunnel (phone — all traffic via VPN)

```text
Allowed IPs: 0.0.0.0/0, ::/0
```

All traffic — including regular browsing — routes through your home connection. Useful on cellular where you want Pi-hole's ad blocking everywhere.

### Split Tunnel (laptop — homelab only)

```text
Allowed IPs: 192.168.1.0/24, 10.10.10.0/24
```

Only traffic destined for your LAN or other VPN peers routes through the tunnel. General browsing uses the device's local internet. Faster for daily use, lower load on your home connection.

!!! tip
    Use full tunnel for phones (you get Pi-hole ad blocking on cellular) and split tunnel for laptops (general browsing isn't bottlenecked by your home upload speed).

---

## Step 3: Firewall Rules

Two rules are required.

### Rule 1 — Allow WireGuard traffic in on WAN

**Firewall → Rules → WAN → Add**

| Field | Value |
|-------|-------|
| Action | Pass |
| Direction | In |
| Protocol | UDP |
| Source | any |
| Destination | WAN address |
| Destination port | 51820 |

### Rule 2 — Allow traffic through the tunnel

**Firewall → Rules → WireGuard (tab) → Add**

| Field | Value |
|-------|-------|
| Action | Pass |
| Direction | In |
| Protocol | any |
| Source | any |
| Destination | any |

---

## Step 4: Outbound NAT (the part most guides miss)

This is where most WireGuard-on-OPNsense setups break. Without the correct NAT rules, VPN clients can reach LAN hosts but DNS replies from Pi-hole get silently dropped, and internet traffic doesn't route correctly.

First, set NAT mode to **Hybrid**: **Firewall → NAT → Outbound** → select **Hybrid Outbound NAT**.

Add two rules:

### NAT Rule 1 — Tunnel to Internet

| Field | Value |
|-------|-------|
| Interface | WAN |
| Source | WireGuard (Group) net |
| Translation | Interface address |

This masquerades VPN client traffic behind your WAN IP so it can reach the internet.

### NAT Rule 2 — Tunnel to LAN

| Field | Value |
|-------|-------|
| Interface | LAN |
| Source | WireGuard (Group) net |
| Translation | Interface address |

!!! warning "This rule is critical and commonly missed"
    Without this rule, VPN clients can ping LAN hosts and even open connections, but DNS responses from Pi-hole get dropped. The symptom is that DNS lookups time out or return nothing even though ping to the Pi-hole IP works. Adding this LAN NAT rule fixes it.

---

## Step 5: Client Setup

### iPhone / Android

1. Open the WireGuard app
2. Tap **+** → **Create from QR code**
3. Scan the QR from the Peer Generator
4. Enable the tunnel

### macOS

1. In OPNsense, go to **VPN → WireGuard → Peers**, click the download icon next to your peer, and save the `.conf` file. Import this file into the macOS WireGuard app.
2. Open the WireGuard app (Mac App Store)
3. Click **+** → **Add Empty Tunnel**
4. Paste your peer config directly (copy from OPNsense peer view)

Alternatively, export the config file and drag it into the WireGuard app.

---

## Verification

```bash
# From a device on cellular with VPN enabled
curl -I https://google.com
# Should return HTTP headers — internet routing works

ping -c 3 192.168.1.x   # your Pi-hole IP
# Should reply — LAN is reachable through tunnel

nslookup doubleclick.net
# Should return 0.0.0.0 — Pi-hole filtering works through VPN
```

In OPNsense: **VPN → WireGuard → Status** should show your peer with a recent handshake time and bytes transferred.

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| Peer not saving | Didn't click Save at bottom of Peer Generator | Scroll to bottom and Save; verify in Peers tab |
| Peer not appearing in instance | Peer saved but not linked to instance | Edit Instance → select peer in Peers dropdown → Apply |
| DNS not working through VPN | Missing LAN NAT rule | Add NAT Rule 2 (Tunnel to LAN) |
| Internet not working through full tunnel | Missing WAN NAT rule | Add NAT Rule 1 (Tunnel to WAN) |
| Can't connect from outside | WAN firewall rule missing | Add UDP 51820 pass rule on WAN |

---

## Related Pages

- [OPNsense on Zimaboard 2](opnsense-zimaboard.md) — router setup prerequisite
- [Pi-hole + Unbound DNS](dns-stack.md) — Pi-hole DNS filtering extends through the VPN with the LAN NAT rule

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
