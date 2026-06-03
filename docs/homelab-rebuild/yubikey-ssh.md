---
title: YubiKey FIDO2 SSH Authentication
description: Set up hardware-bound SSH authentication using a YubiKey and FIDO2 ed25519-sk keys. Works on macOS with Homebrew OpenSSH, requires physical key presence for every login.
---

# YubiKey FIDO2 SSH Authentication

Password SSH is a liability. Key-based SSH is better, but a private key file on disk can still be copied. FIDO2 SSH binds the key to the physical YubiKey — even if someone copies your entire filesystem, they can't SSH without the hardware token. This guide sets up `ed25519-sk` keys with PIN + touch required for every authentication.

## Prerequisites

- YubiKey 5 series (any form factor) — [YubiKey 5 NFC](https://www.yubico.com/au/product/yubikey-5-nfc/) recommended for iPhone NFC use
- macOS with [Homebrew](https://brew.sh/) installed
- Servers running OpenSSH 8.2+ (Ubuntu 20.04+, Debian 11+)
- A second YubiKey for backup (strongly recommended — see [Backup](#backup-yubikey))

---

## Why FIDO2 (`ed25519-sk`) Over PIV/GPG?

| Approach | Setup complexity | Key storage | Touch required |
|----------|-----------------|-------------|----------------|
| Regular `ed25519` | Simple | File on disk | ❌ |
| PIV (SmartCard) | Complex | On YubiKey | Optional |
| GPG subkey | Very complex | On YubiKey | Optional |
| FIDO2 `ed25519-sk` | Simple | On YubiKey | ✅ mandatory |

FIDO2 is the modern approach — simple to set up, well-supported in OpenSSH 8.2+, and the key physically cannot be used without the YubiKey present.

---

## macOS: Install Homebrew OpenSSH

macOS ships with Apple's fork of OpenSSH, which doesn't include FIDO middleware support. You need Homebrew's OpenSSH.

```bash
brew install openssh libfido2
```

Add Homebrew's SSH to your PATH so it takes precedence over the system version. Add this to `~/.zshrc`:

```bash
export PATH="/opt/homebrew/opt/openssh/bin:$PATH"
```

Apply it:

```bash
source ~/.zshrc
```

Verify you're using the Homebrew version:

```bash
which ssh
# Should output: /opt/homebrew/opt/openssh/bin/ssh

ssh -V
# Should show OpenSSH_9.x or 10.x
```

!!! warning
    If `which ssh` still shows `/usr/bin/ssh`, the PATH change hasn't applied. Make sure you added it to `~/.zshrc` (not `~/.bash_profile`) and that you're using zsh (default on modern macOS).

---

## Set a FIDO2 PIN (First Time)

If your YubiKey doesn't have a FIDO2 PIN set, you must set one before generating resident keys. The PIN is required to generate keys and to use `verify-required` keys.

```bash
brew install ykman
ykman fido access change-pin
```

You'll be prompted to enter a new PIN (minimum 4 characters, 8+ recommended). This PIN is separate from your YubiKey's management key — it's specifically for FIDO2 operations.

!!! tip
    If you forget the FIDO2 PIN, you'll need to reset the FIDO2 application on the YubiKey with `ykman fido reset`. This **deletes all resident keys** stored on the key, so keep a backup.

---

## Generate the Key

```bash
ssh-keygen -t ed25519-sk \
  -O resident \
  -O verify-required \
  -f ~/.ssh/id_ed25519_yubikey \
  -C "yubikey-$(date +%Y%m%d)"
```

**Flag explanation:**

| Flag | What it does |
|------|--------------|
| `-t ed25519-sk` | FIDO2 key type using Ed25519 curve |
| `-O resident` | Stores the key handle on the YubiKey itself (re-derivable on new machines) |
| `-O verify-required` | Requires PIN + touch for every use |
| `-f ~/.ssh/id_ed25519_yubikey` | Output file for the local key handle |
| `-C "yubikey-..."` | Comment to identify the key |

You'll be prompted to:
1. Touch your YubiKey (to confirm key generation)
2. Enter your FIDO2 PIN

Two files are created:
- `~/.ssh/id_ed25519_yubikey` — local key handle (not the private key — the private key is on the YubiKey)
- `~/.ssh/id_ed25519_yubikey.pub` — public key to deploy to servers

---

## Deploy the Public Key to Servers

```bash
ssh-copy-id -i ~/.ssh/id_ed25519_yubikey.pub user@server.local
```

Or manually: append the contents of `~/.ssh/id_ed25519_yubikey.pub` to `~/.ssh/authorized_keys` on the target server.

### For OPNsense

Navigate to **System → Access → Users**, edit your user, and paste the public key content into the **Authorized keys** field.

---

## SSH Config

Create or update `~/.ssh/config` to make connections convenient:

```
Host *
    IdentityFile ~/.ssh/id_ed25519_yubikey
    IdentitiesOnly yes

Host pihole-host
    HostName 192.168.1.x
    User your-username

Host opnsense
    HostName 192.168.1.1
    User root
```

Replace `192.168.1.x` with your actual server IPs.

Now `ssh pihole-host` will prompt for your YubiKey touch and PIN, then connect.

---

## Using the Resident Key on a New Machine

The `-O resident` flag stores the key handle on the YubiKey itself. On a new Mac or after reinstalling:

```bash
# Plug in YubiKey and derive the local key handle
ssh-keygen -K
```

This writes `id_ed25519_sk_rk` and `id_ed25519_sk_rk.pub` to `~/.ssh/`. You can rename these to match your config.

---

## Backup YubiKey

!!! warning "Always register a second YubiKey before disabling password auth"
    If you lose your only YubiKey and have disabled password SSH, you're locked out. Always:

    1. Buy a second YubiKey
    2. Generate a separate FIDO2 key on it: `ssh-keygen -t ed25519-sk -O resident -O verify-required -f ~/.ssh/id_ed25519_yubikey_backup -C "yubikey-backup-$(date +%Y%m%d)"`
    3. Deploy the backup public key to every server
    4. Store the backup YubiKey in a physically safe location
    5. Only disable password auth after both keys are deployed and tested

---

## Disable Password SSH (After Backup is Set Up)

Once both YubiKeys are deployed and tested, disable password authentication on each server:

```bash
sudo nano /etc/ssh/sshd_config
```

Set:

```
PasswordAuthentication no
PubkeyAuthentication yes
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

Test from a new terminal (don't close your current session) to confirm key auth works before fully committing.

---

## Verification

```bash
# Test connection — you should be prompted for touch + PIN
ssh pihole-host

# Confirm which key was used
ssh -v pihole-host 2>&1 | grep "Offering"
# Should show: Offering public key: ... sk-ssh-ed25519@openssh.com
```

---

## Common Gotchas

| Problem | Cause | Fix |
|---------|-------|-----|
| `sign_and_send_pubkey: signing failed` | YubiKey not plugged in | Insert YubiKey and retry |
| Key generation fails with FIDO error | No FIDO2 PIN set | Run `ykman fido access change-pin` first |
| `which ssh` returns `/usr/bin/ssh` | Homebrew PATH not set | Add to `~/.zshrc`, source it |
| `verify-required` not prompting for PIN | Using system OpenSSH | Confirm Homebrew SSH is in PATH |
| Locked out after disabling password auth | Lost YubiKey, no backup | Physical console access to re-enable password auth |

---

## Related Pages

- [OPNsense on Zimaboard 2](opnsense-zimaboard.md) — add your YubiKey public key to OPNsense's SSH access

<a href="https://www.buymeacoffee.com/techdox"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a cup of tea&emoji=🍵&slug=techdox&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" /></a>

---

If there is an issue with this guide or you wish to suggest changes, please raise an issue on [GitHub](https://github.com/Techdox/techdox-docs).
