---
title: macOS Security Hardening
description: Practical macOS hardening using native protections and the Objective-See free toolkit. No third-party antivirus required.
---

# macOS Security Hardening

macOS has strong built-in security features that most users leave misconfigured, plus a set of free tools from [Objective-See](https://objective-see.org/) that add meaningful protection without the bloat of commercial antivirus. This guide covers both — what to enable natively and what to add on top.

## Prerequisites

- macOS Ventura or later (Sonoma/Sequoia recommended)
- Admin access to your Mac
- Apple Account with two-factor authentication enabled

---

## Native macOS Protections

Work through each of these. Most are off or misconfigured on a fresh Mac.

### FileVault (Full Disk Encryption)

**System Settings → Privacy & Security → FileVault**

Turn on FileVault. This encrypts your entire disk — if your Mac is stolen or powered off, the data is unreadable without your login password.

!!! warning "Save your recovery key securely"
    macOS offers to store your FileVault recovery key with Apple or give you a local key. Store the local key in your password manager (e.g., Proton Pass). If you forget your password and don't have the recovery key, the data is gone.

### Application Firewall

**System Settings → Network → Firewall → Turn On**

Then click **Options** and enable **Block all incoming connections** except the services you explicitly need. The application firewall blocks inbound connections app-by-app — it's a different layer to LuLu (which handles outbound).

!!! note
    macOS's built-in firewall only handles inbound. For outbound control (which apps can phone home), use LuLu — see below.

### Find My Mac + Remote Wipe

**Apple Account → iCloud → Find My Mac** — enable this.

If your Mac is lost or stolen:
1. Sign into [icloud.com](https://icloud.com) from another device
2. Go to **Find My → All Devices**
3. Erase the device remotely before someone can brute-force the login

### Screen Lock

**System Settings → Lock Screen**

- **Require password after screen saver begins**: Immediately
- **Require password after sleep begins**: Immediately

A screen that locks after 5 minutes is an open door if you step away.

### iCloud Advanced Data Protection (ADP)

**Apple Account → iCloud → Advanced Data Protection**

When enabled, your iCloud data (backups, photos, notes, etc.) is end-to-end encrypted — even Apple can't access it. This is off by default.

!!! warning "Set up a recovery contact or key before enabling"
    With ADP on, Apple cannot help you recover your account. Set up an account recovery contact (trusted person) or recovery key before enabling, otherwise you risk permanent lockout.

---

## Objective-See Tools

These are free, open-source tools from Patrick Wardle's [Objective-See](https://objective-see.org/). Unlike commercial antivirus, they add specific controls rather than scanning for signatures of already-known malware.

### LuLu — Outbound Application Firewall

[Download LuLu](https://objective-see.org/products/lulu.html)

LuLu prompts you every time a new application attempts an outbound network connection. You can allow or deny it permanently. This lets you:

- See which apps are phoning home
- Block apps from making unexpected connections
- Catch new apps that attempt network access before you've reviewed them

On first install, you'll get a flurry of prompts as LuLu learns your existing apps. After the initial approval phase, it's quiet.

!!! tip "What to approve during LuLu's learning phase"
    During the initial learning phase, **allow everything you recognise**. It is much easier to tighten rules later than to diagnose a broken app you accidentally blocked. Focus on blocking items you don't recognise.

### BlockBlock — Persistence Monitor

[Download BlockBlock](https://objective-see.org/products/blockblock.html)

Malware often survives reboots by installing persistence mechanisms (launch agents, login items, browser extensions). BlockBlock alerts you whenever anything tries to add a persistent item to your Mac.

### KnockKnock — Startup Item Auditor

[Download KnockKnock](https://objective-see.org/products/knockknock.html)

Run this quarterly as an audit tool (it's not a background daemon). It scans all persistence locations and shows everything that runs at startup, with VirusTotal ratings for unknown items.

!!! tip "Most KnockKnock findings are legitimate"
    Most items KnockKnock lists are **legitimate macOS system components or app launch agents**. Focus on entries you don't recognise or those with no code signature. Don't delete anything unless you're certain it's malicious.

### OverSight — Mic and Camera Monitor

[Download OverSight](https://objective-see.org/products/oversight.html)

OverSight sits in the menu bar and alerts you when any process activates the microphone or camera. Useful for catching apps that listen when they shouldn't.

---

## App Privacy Report

**System Settings → Privacy & Security → App Privacy Report → Turn On**

After a week of use, this shows you which apps accessed your location, contacts, camera, microphone, and — most usefully — which domains they connected to. It's the built-in equivalent of LuLu's connection log.

---

## What to Avoid

| Product / Action | Why |
|-----------------|-----|
| Traditional antivirus (Norton, McAfee, Kaspersky) | macOS has XProtect built in. Third-party AV adds attack surface and system extension access without meaningful protection gain |
| CleanMyMac and similar "optimizers" | Deep system access, questionable benefit, often flagged by security researchers |
| Disabling SIP (System Integrity Protection) | SIP prevents malware from modifying core OS files. Never disable this in production |
| Running daily tasks as an admin user | Create a standard user account for daily use, use admin only for installs and settings changes |

---

## Account Setup Best Practice

macOS lets you have multiple user accounts. The recommended setup:

1. **Admin account** — used only for system changes, software installs, System Settings. Not your day-to-day login.
2. **Standard account** — your daily driver. Apps run with limited permissions.

This limits the blast radius of any compromised app or browser exploit — it runs as a standard user, not an admin.

To create a Standard account: go to **System Settings → Users & Groups → Add Account**, set the account type to **Standard**, and use that account for daily work. Keep your admin account for system changes only.

---

## Verification Checklist

- [ ] FileVault: **On**, recovery key saved in password manager
- [ ] Application Firewall: **On**
- [ ] Screen lock: **Immediately**
- [ ] Find My Mac: **On**
- [ ] iCloud Advanced Data Protection: **On**
- [ ] LuLu: installed and active (menu bar icon visible)
- [ ] BlockBlock: installed and active
- [ ] OverSight: installed and active
- [ ] App Privacy Report: **On**
- [ ] Daily user account is a **Standard** account, not Admin

---

## Related Pages

- [YubiKey SSH](yubikey-ssh.md) — hardware-bound SSH authentication for your servers
- [Proton Mail Migration](proton-mail-custom-domain.md) — privacy-focused email to pair with device hardening

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
