---
title: Migrating Email to Proton Mail with Custom Domain
description: Step-by-step guide to migrating your email from any provider to Proton Mail with a custom domain, including MX, SPF, DKIM, DMARC setup and importing historical mail.
---

# Migrating Email to Proton Mail with Custom Domain

Moving email to Proton Mail with your own domain means your email address isn't tied to any provider — you can move again later without changing your address. This guide covers the full migration: domain verification, MX cutover, SPF/DKIM/DMARC, and importing historical mail.

## Prerequisites

- [Proton Mail Plus](https://proton.me/mail/pricing) or higher (free plan doesn't support custom domains)
- A domain with DNS managed through Cloudflare (examples use Cloudflare, but the records are the same on any provider)
- Access to your current email provider to export/import mail
- 15–30 minutes of DNS propagation time

---

## Pre-Migration Assessment

Before touching DNS, inventory what's already there. Log into your Cloudflare DNS panel and note every record related to email:

- **MX records** — pointing to your current mail provider
- **TXT records** — SPF (`v=spf1 ...`) and possibly DMARC (`v=DMARC1 ...`)
- **CNAME records** — DKIM keys for your current provider
- **Domain verification TXTs** — may be required by your current provider

!!! tip
    If you use transactional email services (e.g., Mailgun, SendGrid, Zendesk) on **subdomains** (e.g., `mail.yourdomain.com`), these are separate from your root domain's email and won't be affected by this migration. Only touch records at the root (`@`).

---

## Step 1: Verify Domain Ownership with Proton

1. Log into Proton Mail → **Settings → Domain names → Add custom domain**
2. Enter your domain
3. Proton will provide a verification TXT record:

```text
Type: TXT
Name: @
Value: protonmail-verification=<your-unique-string>
```

Add this to your Cloudflare DNS (do **not** wrap the value in quotes — Cloudflare adds them automatically).

4. Click **Verify** in Proton. Propagation usually takes under 5 minutes with Cloudflare.

---

## Step 2: Add Email Addresses

Before cutting over MX, add the addresses you want in Proton:

1. In Proton domain settings → **Addresses tab**
2. Add your primary address (e.g., `you@yourdomain.com`)
3. Add any aliases you need

---

## Step 3: MX Cutover

This is the step that switches inbound mail delivery from your old provider to Proton.

**Remove** your current MX records (e.g., the ones pointing to iCloud, Google, or wherever).

**Add** Proton's MX records:

```text
Type: MX  Name: @  Priority: 10  Value: mail.protonmail.ch
Type: MX  Name: @  Priority: 20  Value: mailsec.protonmail.ch
```

!!! warning "Brief delivery gap"
    There may be a short window (minutes, not hours with Cloudflare) where some mail goes to the old provider and some to Proton. If zero-gap migration matters, do the cutover late at night and import any straggler mail from the old provider afterward. Keep your old email provider account active and **check it for at least 48 hours** after cutover — some senders cache MX records beyond the TTL and deliveries may still arrive at your old address during this window.

---

## Step 4: SPF

SPF tells receiving servers which hosts are authorised to send mail for your domain.

**Remove** your existing SPF TXT record (there must only be one SPF record per domain).

**Add** Proton's:

```text
Type: TXT  Name: @  Value: v=spf1 include:_spf.protonmail.ch ~all
```

!!! warning "Only one SPF record allowed"
    Multiple SPF records cause authentication failures. If you have an existing SPF record, replace it entirely — don't add a second one.

---

## Step 5: DKIM

DKIM lets receiving servers verify that outbound mail actually came from Proton and wasn't tampered with. Proton uses three CNAME records for key rotation:

```text
Type: CNAME  Name: protonmail._domainkey
Value: protonmail.domainkey.<your-id>.domains.proton.ch

Type: CNAME  Name: protonmail2._domainkey
Value: protonmail2.domainkey.<your-id>.domains.proton.ch

Type: CNAME  Name: protonmail3._domainkey
Value: protonmail3.domainkey.<your-id>.domains.proton.ch
```

The exact values are shown in your Proton domain settings — copy them directly.

!!! warning "Set DKIM CNAMEs to DNS-only in Cloudflare"
    Make sure the orange Cloudflare proxy cloud is **off** (grey/DNS-only) for these CNAME records. Proxying DKIM records breaks validation.

---

## Step 6: DMARC

DMARC tells receiving servers what to do with mail that fails SPF or DKIM checks, and optionally sends you reports.

```text
Type: TXT  Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
```

- `p=quarantine` — suspicious mail goes to spam rather than being rejected outright. Switch to `p=reject` once you're confident everything is working.
- `rua=` — address for aggregate reports (optional but useful for spotting misconfiguration)

---

## Verification

Once all records are in place, verify from the command line:

```bash
# MX records
dig MX yourdomain.com +short
# Should show: mail.protonmail.ch and mailsec.protonmail.ch

# SPF
dig TXT yourdomain.com +short
# Should include: v=spf1 include:_spf.protonmail.ch ~all

# DKIM
dig CNAME protonmail._domainkey.yourdomain.com +short
# Should return a protonmail.domainkey.*.domains.proton.ch value

# DMARC
dig TXT _dmarc.yourdomain.com +short
# Should return your DMARC policy
```

You can also use [MXToolbox](https://mxtoolbox.com/) or [mail-tester.com](https://www.mail-tester.com/) for a visual check.

---

## Set Up a Catch-All

A catch-all forwards any `*@yourdomain.com` address to your inbox — useful so you never miss mail sent to old addresses or aliases you've used over the years.

1. Proton domain settings → **Catch-all**
2. Point it at your primary address

---

## Import Historical Mail

If you're migrating from another provider, you can import your existing mail into Proton:

1. **Settings → Import via Easy Switch**
2. Select your current provider
3. For Apple iCloud: generate an app-specific password at [appleid.apple.com](https://appleid.apple.com) (iCloud doesn't allow regular passwords for third-party access)
4. Enter your email + app-specific password
5. Select folders/labels to import
6. The import runs in the background — large mailboxes can take hours

---

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Verification TXT fails | Added quotes around value | Remove manual quotes — Cloudflare adds them |
| SPF fails | Two SPF records exist | Delete old SPF, keep only the Proton one |
| DKIM fails | CNAMEs proxied through Cloudflare | Set to DNS-only (grey cloud) |
| Mail going to old provider | MX records not updated | Verify MX with `dig MX yourdomain.com` |
| `p=reject` DMARC drops mail | DKIM/SPF not fully propagated | Use `p=quarantine` first, move to `p=reject` after a week |

---

## Related Pages

- [macOS Hardening](macos-hardening.md) — full device security posture to pair with privacy-focused email

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
