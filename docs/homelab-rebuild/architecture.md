---
title: Full Stack Architecture Diagram
description: Complete architecture diagram of the homelab rebuild stack, showing all layers from network to identity.
---

# Full Stack Architecture

This page shows the complete picture of how all the layers in the [Homelab Rebuild](index.md) connect to each other.

---

## Network & DNS Layer

The arrows show the direction of network traffic and DNS query flow between components, from the internet edge down to recursive resolution.

```mermaid
flowchart TD
    Internet([Internet]) --> ISP[ISP Modem / ONT]
    ISP -->|WAN / DHCP| OPN["OPNsense\n(Zimaboard 2)\nFirewall · DHCP · NAT"]

    OPN -->|LAN 192.168.1.0/24| SW[Switch / AP]
    SW --> Devices([LAN devices\nDesktops · Phones · IoT])

    OPN -->|Inline traffic inspection| IDS[Suricata IDS]

    OPN -->|DHCP Option 6 → Pi-hole IP| PIHOLE["Pi-hole\nAd blocking · Local DNS"]
    PIHOLE -->|Upstream: router LAN IP:53| UNB["Unbound\n(on OPNsense)\nRecursive + DNSSEC"]
    UNB -->|Iterative queries| ROOT([Root · TLD · Auth DNS])
```

---

## Remote Access Layer

The arrows show the direction of network traffic between remote clients and the internal network via WireGuard tunnels.

```mermaid
flowchart LR
    Phone([iPhone\nFull tunnel]) -->|WireGuard UDP 51820| WG
    Laptop([MacBook\nSplit tunnel]) -->|WireGuard UDP 51820| WG

    WG["WireGuard\n(on OPNsense)\n10.10.10.0/24"] -->|Tunnel traffic| OPN[OPNsense]
    OPN --> LAN([LAN services])

    subgraph NAT Rules
        NAT1[WireGuard → WAN\nInternet access]
        NAT2[WireGuard → LAN\nPi-hole DNS replies]
    end
```

---

## Public Services Layer

The arrows show the direction of network traffic from external users through Cloudflare's edge and the internal tunnel daemon to the self-hosted service, as well as the parallel path taken by LAN clients via Nginx Proxy Manager.

```mermaid
flowchart LR
    User([External user]) -->|HTTPS| CF[Cloudflare Edge\nDDoS protection · TLS]
    CF -->|Tunnel QUIC/HTTP2| CFD[cloudflared daemon\non service host]
    CFD --> SVC([Self-hosted service\nport on localhost])

    subgraph Internal path
        LAN([LAN client]) -->|DNS: Pi-hole local record| NPM[Nginx Proxy Manager\nInternal TLS · Let's Encrypt]
        NPM --> SVC2([Same service\ndifferent path])
    end
```

---

## Identity & Authentication Layer

The arrows show which components depend on or are authenticated by the hardware keys — SSH sessions and online accounts both route through a physical YubiKey for second-factor verification.

```mermaid
flowchart TD
    subgraph Identity Stack
        PM["Proton Mail\nCustom domain email"]
        PW["Proton Pass\nPassword manager"]
        PA["Proton Authenticator\nTOTP 2FA"]
    end

    subgraph Hardware Auth
        YK1["YubiKey (primary)\nFIDO2 SSH · Account 2FA"]
        YK2["YubiKey (backup)\nIdentical setup\nStored separately"]
    end

    SSH[SSH to servers] -->|ed25519-sk key| YK1
    Accounts[Online accounts] -->|FIDO2 hardware key| YK1
```

---

## Device Security Layer

The diagram shows the security controls that operate in parallel on the macOS host, each covering a distinct protection layer — from disk encryption and network access control through to persistence and peripheral monitoring.

```mermaid
flowchart TD
    subgraph macOS Hardening
        FV[FileVault\nFull disk encryption]
        FW[Application Firewall\nInbound blocking]
        LULU[LuLu\nOutbound app firewall]
        BB[BlockBlock\nPersistence monitor]
        OS[OverSight\nMic · Camera alerts]
        ADP[iCloud ADP\nEnd-to-end encrypted backups]
    end
```

---

## Full Stack Summary

| Layer | Components | Guides |
|-------|-----------|--------|
| Network | OPNsense, Zimaboard 2, TP-Link Deco (AP mode) | [OPNsense](opnsense-zimaboard.md) |
| Intrusion Detection | Suricata IDS | [OPNsense](opnsense-zimaboard.md) |
| DNS | Pi-hole + Unbound + DNSSEC | [DNS Stack](dns-stack.md) |
| DHCP + Local DNS | Dnsmasq (on OPNsense) | [OPNsense](opnsense-zimaboard.md) |
| Remote Access | WireGuard on OPNsense | [WireGuard VPN](wireguard-vpn.md) |
| Public Services | Cloudflare Tunnels | [Cloudflare Tunnels](cloudflare-tunnels.md) |
| Internal TLS | Nginx Proxy Manager + Pi-hole local DNS | [Internal Hostnames](internal-hostnames.md) |
| Email | Proton Mail with custom domain | [Proton Mail](proton-mail-custom-domain.md) |
| Authentication | YubiKey FIDO2 SSH | [YubiKey SSH](yubikey-ssh.md) |
| Device | macOS + Objective-See tools | [macOS Hardening](macos-hardening.md) |

---

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
